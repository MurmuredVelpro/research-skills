#!/usr/bin/env python3
"""Import a lit-search delivery into a review project as an immutable search export.

    python3 scripts/import_litsearch.py --project-dir <project_dir> \\
        --run-dir <lit-search runs root>/<topic>/<run_id> --searcher-id <named human>

The lit-search skill owns retrieval (multi-source, citation closure, measured recall); this
skill takes its corpus as the candidate pool and hands it to the human screening gates. The
import:

1. copies the delivery files the run has — ``dois.md``, ``PRISMA.md`` and ``topic.yaml`` are
   required; ``references.md``, ``coverage_report.md``, ``references.bib`` when present — into
   ``search/exports/litsearch-<run_id>/`` (staged, then renamed; files made read-only);
2. appends exactly one ``search/search_log.csv`` row whose ``result_count`` is PRISMA's total
   identified count and whose strategy/export paths point at the copied files;
3. re-checks the project's search log with the audit's own rule.

It refuses — exit 2, nothing written — when the export directory already exists (an import is
never redone in place: a new lit-search run gets its own run id) or when the PRISMA total cannot
be read. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import stat
import sys
from datetime import date
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mir_audit.checks_artifacts import validate_search_log  # noqa: E402
from mir_audit.constants import SEARCH_LOG_COLUMNS  # noqa: E402

REQUIRED = ("dois.md", "PRISMA.md", "topic.yaml")
OPTIONAL = ("references.md", "coverage_report.md", "references.bib")
#: lit-search 的 PRISMA.md 渲染行：「合计识别：**1,234** 条」（report.py prisma_markdown）
IDENTIFIED_RE = re.compile(r"合计识别：\*\*([\d,]+)\*\*")
CANONICAL_RE = re.compile(r"去重后规范记录：\*\*([\d,]+)\*\*")
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ImportRefused(Exception):
    pass


def read_identified(prisma: Path) -> tuple[int, int | None]:
    text = prisma.read_text(encoding="utf-8")
    match = IDENTIFIED_RE.search(text)
    if not match:
        raise ImportRefused(
            f"{prisma.name} has no total-identified count ('合计识别：**N** 条') — "
            "re-run `lit report` so the PRISMA counts reconcile, then import"
        )
    canonical = CANONICAL_RE.search(text)
    return (int(match.group(1).replace(",", "")),
            int(canonical.group(1).replace(",", "")) if canonical else None)


def read_run_id(run_dir: Path) -> str:
    manifest = run_dir / "manifest.json"
    run_id = run_dir.name
    if manifest.is_file():
        run_id = str(json.loads(manifest.read_text(encoding="utf-8")).get("run_id") or run_id)
    if not SAFE_RUN_ID.match(run_id):
        raise ImportRefused(f"run id {run_id!r} is not a safe directory name")
    return run_id


def read_window(topic: Path) -> str:
    """`window: {start, end}` from the frozen protocol, as 'YYYY-MM-DD..YYYY-MM-DD'."""
    text = topic.read_text(encoding="utf-8")
    block = re.search(r"^window:\s*\n((?:[ \t]+.*\n?)+)", text, re.M)
    if block:
        start = re.search(r"^\s+start:\s*['\"]?([\w-]+)", block.group(1), re.M)
        end = re.search(r"^\s+end:\s*['\"]?([\w-]+)", block.group(1), re.M)
        if start and end:
            return f"{start.group(1)}..{end.group(1)}"
    return "time window: see topic.yaml"


def make_read_only(directory: Path) -> None:
    for path in directory.iterdir():
        path.chmod(path.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def append_row(log: Path, row: dict[str, str]) -> None:
    if not log.exists():
        log.write_text(",".join(SEARCH_LOG_COLUMNS) + "\n", encoding="utf-8")
    existing = log.read_text(encoding="utf-8")
    buffer = StringIO()
    csv.DictWriter(buffer, fieldnames=SEARCH_LOG_COLUMNS, lineterminator="\n").writerow(row)
    separator = "" if existing.endswith("\n") or not existing else "\n"
    with log.open("a", encoding="utf-8", newline="") as handle:
        handle.write(separator + buffer.getvalue())


def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date: str | None) -> Path:
    if not (project_dir / "review_config.yaml").is_file():
        raise ImportRefused(f"{project_dir} is not a review project (no review_config.yaml)")
    missing = [name for name in REQUIRED if not (run_dir / name).is_file()]
    if missing:
        raise ImportRefused(f"{run_dir} lacks {', '.join(missing)} — run `lit report` / `lit deliver` first")
    identified, canonical = read_identified(run_dir / "PRISMA.md")
    run_id = read_run_id(run_dir)

    exports = project_dir / "search" / "exports"
    target = exports / f"litsearch-{run_id}"
    if target.exists() or target.is_symlink():
        raise ImportRefused(f"{target.relative_to(project_dir)} already exists — an import is never redone in place")
    exports.mkdir(parents=True, exist_ok=True)
    staging = exports / f".litsearch-{run_id}.staging-{os.getpid()}"
    staging.mkdir()
    try:
        for name in REQUIRED + OPTIONAL:
            if (run_dir / name).is_file():
                shutil.copy2(run_dir / name, staging / name)
        make_read_only(staging)
        staging.rename(target)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    relative = target.relative_to(project_dir).as_posix()
    append_row(project_dir / "search" / "search_log.csv", {
        "source": "lit-search",
        "platform": f"lit-search run {run_id} (sources and per-source counts: {relative}/PRISMA.md)",
        "coverage": read_window(run_dir / "topic.yaml"),
        "search_date": search_date or date.today().isoformat(),
        "strategy_file": f"{relative}/topic.yaml",
        "filters": "frozen lit-search protocol (concept blocks, window, languages) in topic.yaml",
        "result_count": str(identified),
        "export_file": f"{relative}/dois.md",
        "searcher_id": searcher_id,
        "notes": (f"imported by import_litsearch.py; PRISMA identified {identified:,}"
                  + (f", after deduplication {canonical:,}" if canonical is not None else "")
                  + "; screening continues under this project's human gates"),
    })
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True, help="the lit-search run directory")
    parser.add_argument("--searcher-id", required=True, help="named human responsible for the search")
    parser.add_argument("--search-date", help="ISO date the search ran (default: today)")
    args = parser.parse_args(argv)
    if not args.searcher_id.strip():
        print("ERROR: --searcher-id must name a person", file=sys.stderr)
        return 2
    try:
        target = import_run(args.project_dir, args.run_dir, args.searcher_id.strip(), args.search_date)
    except (ImportRefused, OSError, UnicodeDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    problems, _valid, _total, _error = validate_search_log(args.project_dir)
    print(f"Imported lit-search run into {target}")
    for problem in problems:
        print(f"WARN search log: {problem}")
    print("Next: screening/deduplication stay with the named human reviewers; "
          "flow_counts identified must equal the summed search_log result_count.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
