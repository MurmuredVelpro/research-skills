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

    def snapshot(self) -> dict[str, bytes]:
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob("*") if p.is_file()}

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

    def test_not_a_review_project_is_refused(self):
        code, out = self.run_import("--project-dir", str(self.run))
        self.assertEqual(code, 2, out)


if __name__ == "__main__":
    unittest.main()
