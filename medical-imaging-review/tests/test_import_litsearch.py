"""import_litsearch.py: lit-search delivery → immutable search export + one search_log row."""

from __future__ import annotations

import csv
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INIT = _load("init_review_project", "init_review_project.py")
IMPORT = _load("import_litsearch", "import_litsearch.py")
from mir_audit.checks_artifacts import validate_search_log  # noqa: E402

PROJECT_ID = "ccta-review-20260723-120000-1234abcd"
RUN_ID = "20261020T101500Z"
PRISMA = """# PRISMA 流程计数 — CCTA

## 识别（Identification）

数据库检索：**1,180** 条
  - openalex：900
  - pubmed：280

其他途径（引文闭包 / 会议录 / 灰色文献）：**54** 条
  - snowball：54

合计识别：**1,234** 条

## 去重（Screening — duplicates）

去除重复：**234** 条
去重后规范记录：**1,000** 条
"""
TOPIC = """id: ccta
window:
  start: 2021-01-01
  end: 2025-12-31
concepts: []
"""


class ImportLitsearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.project = INIT.initialize_project(root, "ccta-review", "systematic", project_id=PROJECT_ID)
        self.run = root / "runs" / "ccta" / RUN_ID
        self.run.mkdir(parents=True)
        (self.run / "manifest.json").write_text(json.dumps({"run_id": RUN_ID}), encoding="utf-8")
        (self.run / "PRISMA.md").write_text(PRISMA, encoding="utf-8")
        (self.run / "topic.yaml").write_text(TOPIC, encoding="utf-8")
        (self.run / "dois.md").write_text("# DOI\n\n- 10.1000/a\n", encoding="utf-8")
        (self.run / "references.md").write_text("1. A. (2024).\n", encoding="utf-8")

    def tearDown(self) -> None:
        for path in self.project.rglob("*"):  # 导入的文件是只读的，清理前恢复写权限
            path.chmod(0o755 if path.is_dir() else 0o644)
        self._tmp.cleanup()

    def run_import(self, *extra: str) -> tuple[int, str]:
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(out):
            code = IMPORT.main(["--project-dir", str(self.project), "--run-dir", str(self.run),
                                "--searcher-id", "reviewer-a", "--search-date", "2026-10-20", *extra])
        return code, out.getvalue()

    def rows(self) -> list[dict[str, str]]:
        with (self.project / "search/search_log.csv").open(encoding="utf-8", newline="") as handle:
            return [row for row in csv.DictReader(handle) if any(row.values())]

    def snapshot(self) -> dict[str, bytes | None]:
        """Every file's bytes and every directory (None) — an empty leftover folder counts."""
        return {p.relative_to(self.project).as_posix(): (p.read_bytes() if p.is_file() else None)
                for p in self.project.rglob("*")}

    def test_import_copies_files_and_appends_one_matching_row(self):
        before = len(self.rows())
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
        self.assertEqual(sorted(p.name for p in target.iterdir()),
                         ["PRISMA.md", "dois.md", "references.md", "topic.yaml"])
        self.assertEqual((target / "PRISMA.md").read_text(encoding="utf-8"), PRISMA)
        rows = self.rows()
        self.assertEqual(len(rows), before + 1)
        row = rows[-1]
        self.assertEqual(row["result_count"], "1234")
        self.assertEqual(row["strategy_file"], f"search/exports/litsearch-{RUN_ID}/topic.yaml")
        self.assertEqual(row["export_file"], f"search/exports/litsearch-{RUN_ID}/dois.md")
        self.assertEqual(row["coverage"], "2021-01-01..2025-12-31")
        self.assertEqual(row["searcher_id"], "reviewer-a")
        self.assertIn(RUN_ID, row["platform"])

    def test_the_audit_accepts_the_imported_row(self):
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        problems, valid, total, error = validate_search_log(self.project)
        self.assertIsNone(error)
        self.assertEqual(problems, [])
        self.assertEqual((valid, total), (1, 1234))

    def test_imported_files_are_read_only(self):
        self.run_import()
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
        for path in target.iterdir():
            self.assertFalse(path.stat().st_mode & 0o222, path.name)

    def test_second_import_of_the_same_run_is_refused_and_writes_nothing(self):
        self.assertEqual(self.run_import()[0], 0)
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("already exists", out)
        self.assertEqual(self.snapshot(), before)

    def test_missing_prisma_total_is_refused_and_writes_nothing(self):
        (self.run / "PRISMA.md").write_text(PRISMA.replace("合计识别：**1,234** 条", ""), encoding="utf-8")
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("total-identified", out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / "search/exports" / f"litsearch-{RUN_ID}").exists())

    def test_missing_required_delivery_file_is_refused(self):
        (self.run / "topic.yaml").unlink()
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("topic.yaml", out)
        self.assertEqual(self.snapshot(), before)

    # --- regressions: stage-6 adversary findings ---------------------------------------------

    def test_unparseable_prisma_total_is_refused(self):
        for bad in ("合计识别：**N/A** 条", "合计识别：**,** 条"):
            with self.subTest(bad=bad):
                (self.run / "PRISMA.md").write_text(PRISMA.replace("合计识别：**1,234** 条", bad), encoding="utf-8")
                before = self.snapshot()
                code, out = self.run_import()
                self.assertEqual(code, 2, out)
                self.assertEqual(self.snapshot(), before)

    def test_optional_delivery_files_are_copied(self):
        (self.run / "coverage_report.md").write_text("# coverage\n", encoding="utf-8")
        (self.run / "references.bib").write_text("@article{a,}\n", encoding="utf-8")
        self.assertEqual(self.run_import()[0], 0)
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
        self.assertTrue((target / "coverage_report.md").is_file())
        self.assertTrue((target / "references.bib").is_file())

    def test_unsafe_run_id_is_refused(self):
        for run_id in ("../escape", "20261020\n", ".hidden"):
            with self.subTest(run_id=run_id):
                (self.run / "manifest.json").write_text(json.dumps({"run_id": run_id}), encoding="utf-8")
                before = self.snapshot()
                code, out = self.run_import()
                self.assertEqual(code, 2, out)
                self.assertIn("safe directory name", out)
                self.assertEqual(self.snapshot(), before)

    def test_foreign_search_log_header_is_refused_before_writing(self):
        log = self.project / "search/search_log.csv"
        log.write_text("database,date,hits\n", encoding="utf-8")
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("header", out)
        self.assertEqual(self.snapshot(), before)

    def test_failed_log_append_rolls_back_the_export(self):
        log = self.project / "search/search_log.csv"
        log.chmod(0o444)
        before = self.snapshot()
        try:
            code, out = self.run_import()
        finally:
            log.chmod(0o644)
        self.assertEqual(code, 2, out)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.run_import()[0], 0)  # retry works: no half-finished import left behind

    def test_audit_rejecting_the_new_row_rolls_back_after_an_earlier_valid_row(self):
        self.assertEqual(self.run_import()[0], 0)  # row 2: a valid earlier import
        (self.run / "manifest.json").write_text(json.dumps({"run_id": "second-run"}), encoding="utf-8")
        before = self.snapshot()

        def rejects_row_3(project_dir):
            problems, valid, total, error = validate_search_log(project_dir)
            return problems + ["search/search_log.csv row 3 is incomplete"], valid, total, error

        with mock.patch.object(IMPORT, "validate_search_log", rejects_row_3):
            code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("row 3", out)
        self.assertEqual(self.snapshot(), before)

    def test_empty_preexisting_export_dir_is_refused(self):
        (self.project / "search/exports" / f"litsearch-{RUN_ID}").mkdir(parents=True)
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("already exists", out)
        self.assertEqual(self.snapshot(), before)

    def test_dangling_symlink_at_the_export_path_is_refused(self):
        exports = self.project / "search/exports"
        exports.mkdir(parents=True, exist_ok=True)
        (exports / f"litsearch-{RUN_ID}").symlink_to(self.project / "nowhere")
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("already exists", out)
        self.assertEqual(self.snapshot(), before)

    def test_not_a_review_project_is_refused(self):
        code, out = self.run_import("--project-dir", str(self.run))
        self.assertEqual(code, 2, out)


class ValidateSearchLogBranches(unittest.TestCase):
    """The refactor moved this rule out of the formal audit; every branch keeps its message."""

    HEADER = ",".join(IMPORT.SEARCH_LOG_COLUMNS)

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        (self.project / "search/exports").mkdir(parents=True)
        (self.project / "search/strategy.txt").write_text("q", encoding="utf-8")
        (self.project / "search/exports/x.ris").write_text("r", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def problems(self, *rows: str) -> list[str]:
        (self.project / "search/search_log.csv").write_text(
            "\n".join((self.HEADER, *rows)) + "\n", encoding="utf-8")
        return validate_search_log(self.project)[0]

    def row(self, **change: str) -> str:
        values = dict(source="PubMed", platform="NCBI", coverage="2020..2024", search_date="2024-01-01",
                      strategy_file="search/strategy.txt", filters="none", result_count="10",
                      export_file="search/exports/x.ris", searcher_id="r1", notes="")
        values.update(change)
        return ",".join(values[c] for c in IMPORT.SEARCH_LOG_COLUMNS)

    def test_a_valid_row_has_no_problem(self):
        self.assertEqual(self.problems(self.row()), [])

    def test_each_branch_reports_its_problem(self):
        cases = {
            "is incomplete": self.row(platform=""),
            "result_count is not an integer": self.row(result_count="ten"),
            "has no preserved strategy file": self.row(strategy_file="search/missing.txt"),
            "has no immutable source export": self.row(export_file="search/exports/missing.ris"),
        }
        for message, row in cases.items():
            with self.subTest(message=message):
                problems = self.problems(row)
                self.assertTrue(any(message in p for p in problems), problems)
                self.assertTrue(any("at least one reproducible" in p for p in problems), problems)

    def test_negative_count_is_rejected(self):
        problems = self.problems(self.row(result_count="-1"))
        self.assertTrue(any("has no preserved strategy file" in p for p in problems), problems)

    def test_header_error_is_returned_as_the_read_error(self):
        (self.project / "search/search_log.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        problems, valid, total, error = validate_search_log(self.project)
        self.assertIsNotNone(error)
        self.assertEqual((problems, valid, total), ([error], 0, 0))


if __name__ == "__main__":
    unittest.main()


class ForeignHeaderRefusedUpFront(unittest.TestCase):
    """The audit would also reject a foreign header after writing; the import must refuse first."""

    setUp = ImportLitsearchTest.setUp
    tearDown = ImportLitsearchTest.tearDown
    run_import = ImportLitsearchTest.run_import

    def test_foreign_header_is_refused_by_the_precheck_not_by_rollback(self):
        (self.project / "search/search_log.csv").write_text("database,date,hits\n", encoding="utf-8")
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("header is not the audit schema", out)
        self.assertNotIn("audit rejects", out)
