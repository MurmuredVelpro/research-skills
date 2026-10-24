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
3. re-checks that row with the audit's own rule (``validate_search_log``).

It refuses — exit 2, nothing written — when the export directory already exists (an import is
never redone in place: a new lit-search run gets its own run id), when the PRISMA total cannot
be read, or when an existing search_log.csv does not carry the audit's header. If appending the
row fails or the audit rejects it, the copied export is removed again, so a retry is possible.
It uses only the Python standard library.
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
IDENTIFIED_RE = re.compile(r"合计识别：\*\*(\d[\d,]*)\*\*")
CANONICAL_RE = re.compile(r"去重后规范记录：\*\*(\d[\d,]*)\*\*")
SAFE_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


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
    if not SAFE_RUN_ID.fullmatch(run_id):
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


def remove_export(target: Path) -> None:
    for path in target.iterdir():
        path.chmod(path.stat().st_mode | stat.S_IWUSR)
    shutil.rmtree(target)


def read_log(log: Path) -> str:
    """Current search_log.csv text ('' if absent); refuses a header that is not the audit's."""
    if not log.exists():
        return ""
    text = log.read_text(encoding="utf-8")
    header = next(csv.reader(StringIO(text)), [])
    if tuple(header) != SEARCH_LOG_COLUMNS:
        raise ImportRefused(f"{log.name} header is not the audit schema ({', '.join(SEARCH_LOG_COLUMNS)})")
    return text


def render_row(row: dict[str, str]) -> str:
    buffer = StringIO()
    csv.DictWriter(buffer, fieldnames=SEARCH_LOG_COLUMNS, lineterminator="\n").writerow(row)
    return buffer.getvalue()


def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date: str | None) -> Path:
    # 1. Everything that can refuse runs before anything is written.
    if not (project_dir / "review_config.yaml").is_file():
        raise ImportRefused(f"{project_dir} is not a review project (no review_config.yaml)")
    missing = [name for name in REQUIRED if not (run_dir / name).is_file()]
    if missing:
        raise ImportRefused(f"{run_dir} lacks {', '.join(missing)} — run `lit report` / `lit deliver` first")
    identified, canonical = read_identified(run_dir / "PRISMA.md")
    run_id = read_run_id(run_dir)
    coverage = read_window(run_dir / "topic.yaml")
    log = project_dir / "search" / "search_log.csv"
    log_before = read_log(log)

    exports = project_dir / "search" / "exports"
    target = exports / f"litsearch-{run_id}"
    if target.exists() or target.is_symlink():
        raise ImportRefused(f"{target.relative_to(project_dir)} already exists — an import is never redone in place")
    relative = target.relative_to(project_dir).as_posix()
    row = render_row({
        "source": "lit-search",
        "platform": f"lit-search run {run_id} (sources and per-source counts: {relative}/PRISMA.md)",
        "coverage": coverage,
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

    # 2. Copy into a staging directory, then rename into place.
    created_exports = not exports.exists()
    exports.mkdir(parents=True, exist_ok=True)
    staging = exports / f".litsearch-{run_id}.staging-{os.getpid()}"
    try:
        staging.mkdir()
        for name in REQUIRED + OPTIONAL:
            if (run_dir / name).is_file():
                shutil.copy2(run_dir / name, staging / name)
        make_read_only(staging)
        staging.rename(target)
    except BaseException:
        if staging.exists():
            remove_export(staging)
        if created_exports:
            shutil.rmtree(exports, ignore_errors=True)
        raise

    # 3. Append the row; if that fails or the audit rejects it, undo the whole import.
    try:
        prefix = log_before or ",".join(SEARCH_LOG_COLUMNS) + "\n"
        if not prefix.endswith("\n"):
            prefix += "\n"
        log.write_text(prefix + row, encoding="utf-8")
        new_index = sum(1 for _ in csv.DictReader(StringIO(prefix + row))) + 1
        problems, _valid, _total, error = validate_search_log(project_dir)
        rejected = [p for p in problems if f"row {new_index} " in p] + ([error] if error else [])
        if rejected:
            raise ImportRefused("the audit rejects the imported search_log row: " + "; ".join(rejected))
    except BaseException:
        # Export first: restoring the log can fail for the same reason the append did.
        remove_export(target)
        if created_exports:
            shutil.rmtree(exports, ignore_errors=True)
        try:
            if log.exists() and log.read_text(encoding="utf-8") != log_before:
                if log_before:
                    log.write_text(log_before, encoding="utf-8")
                else:
                    log.unlink()
        except OSError:
            pass  # the original error below says why the log could not be written
        raise
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
