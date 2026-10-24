"""Shared mechanical-gate core for the writing skills (citation-integrity core, executable form).

本文件在 research-paper/scripts/ 与 research-proposal/scripts/ 各有一份**逐字节相同**的副本
（skill 目录被单独复制安装，不能跨目录 import）。仓库级测试
tests/test_vendored_gate_core.py 在两份副本出现任何差异时变红——改一份就必须同步另一份。

只放与具体 skill 无关的机制：文本扫描、引用解析、对账、报告与退出码。
各 skill 的门禁模式（占位符、AI-tell 正则）留在各自的 check_*.py 里，并由文档契约测试
锁定为与 SKILL.md 中的 grep 模式逐字相同。
"""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

#: 退出码：0 干净；1 有门禁失败；2 用法或输入文件错误（门禁没能运行，不是「通过」）
EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE = 0, 1, 2

#: 参考文献节的标题——数字门禁与引文正文扫描到此为止（年份、卷期、页码不是结果数字）
REFERENCES_HEADING_RE = re.compile(
    r"^#{1,6}\s*(?:\d+[.、]?\s*)?(references|bibliography|参考文献)\s*$", re.I
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#{1,6}\s")


@dataclass(frozen=True)
class Finding:
    kind: str
    location: str
    detail: str

    def render(self, level: str) -> str:
        return f"{level} [{self.kind}] {self.location}: {self.detail}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_body(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """把文稿切成 (正文行, 参考文献节行)，跳过围栏代码块。行号从 1 开始。"""
    body: list[tuple[int, str]] = []
    refs: list[tuple[int, str]] = []
    in_fence = False
    in_refs = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if REFERENCES_HEADING_RE.match(line.strip()):
            in_refs = True
            continue
        if in_refs and HEADING_RE.match(line) and not REFERENCES_HEADING_RE.match(line.strip()):
            # 参考文献节之后的附录等仍属正文
            in_refs = False
        (refs if in_refs else body).append((number, line))
    return body, refs


def pattern_hits(
    text: str, pattern: str, *, ignore_case: bool = False
) -> list[tuple[int, str, str]]:
    """逐行匹配门禁模式（与 SKILL.md 的 `grep -nE`/`-nEi` 同一模式），返回 (行号, 命中, 行)。"""
    compiled = re.compile(pattern, re.I if ignore_case else 0)
    hits: list[tuple[int, str, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for match in compiled.finditer(line):
            hits.append((number, match.group(0), line.strip()))
    return hits


# --- 引用解析 -------------------------------------------------------------------------------

#: pandoc citekey：`[@smith2024; @lee2023, p. 4]` 里的每个 `@key`，以及叙述式 `@smith2024 shows`
CITEKEY_RE = re.compile(r"(?<![\w.@/-])@([A-Za-z0-9_][A-Za-z0-9_:.#$%&+?<>~/-]*[A-Za-z0-9_])")
BIB_ENTRY_RE = re.compile(r"^\s*@(?!comment|string|preamble)\w+\s*\{\s*([^,\s]+)\s*,", re.I | re.M)


def citekeys_in(lines: list[tuple[int, str]]) -> dict[str, int]:
    """正文里出现的 citekey → 首次出现的行号。"""
    found: dict[str, int] = {}
    for number, line in lines:
        for match in CITEKEY_RE.finditer(line):
            found.setdefault(match.group(1), number)
    return found


def bib_keys(text: str) -> list[str]:
    return BIB_ENTRY_RE.findall(text)


def reconcile(cited: dict[str, int], listed: dict[str, str], where: str, listing: str) -> list[Finding]:
    """引用 ↔ 文献表双向对账。cited: key→行号；listed: key→位置描述。"""
    findings = [
        Finding("citation-without-entry", f"{where}:{line}", f"{key} has no entry in {listing}")
        for key, line in sorted(cited.items(), key=lambda item: item[1])
        if key not in listed
    ]
    findings += [
        Finding("entry-never-cited", position, f"{key} is listed but never cited in the text")
        for key, position in listed.items()
        if key not in cited
    ]
    return findings


# --- 数字对账 -------------------------------------------------------------------------------

#: 结果型数字：小数、百分数、样本量 n=/N=。整数年份、章节号、Table 1 不在此列。
METRIC_RE = re.compile(
    r"(?<![\w.])(?:[nN]\s*=\s*(\d[\d,]*)|(\d+(?:\.\d+)?)\s*%|(\d+\.\d+))(?![\w])"
)
_STRIP_INLINE = (
    re.compile(r"\[[^\]]*\]"),  # 引文 / 旗标 / 链接文字——[PENDING: 0.91] 里的数字不算
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"https?://\S+"),
    re.compile(r"\b(?:doi:\s*)?10\.\d{4,9}/\S+", re.I),
    re.compile(r"`[^`]*`"),
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def normalize_number(raw: str) -> str:
    value = raw.replace(",", "")
    if "." in value:
        value = value.rstrip("0").rstrip(".") or "0"
    return value


def metric_numbers(lines: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    """正文里的结果型数字 → (行号, 原文, 规范化值)。标题行不计。"""
    found: list[tuple[int, str, str]] = []
    for number, line in lines:
        if HEADING_RE.match(line):
            continue
        cleaned = line
        for pattern in _STRIP_INLINE:
            cleaned = pattern.sub(" ", cleaned)
        for match in METRIC_RE.finditer(cleaned):
            raw = next(group for group in match.groups() if group)
            found.append((number, match.group(0).strip(), normalize_number(raw)))
    return found


def ledger_numbers(path: Path, columns: tuple[str, ...]) -> set[str]:
    values: set[str] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in columns[:1] if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path.name} has no '{missing[0]}' column")
        for row in reader:
            for column in columns:
                for raw in NUMBER_RE.findall(row.get(column) or ""):
                    values.add(normalize_number(raw))
    return values


# --- 报告 -----------------------------------------------------------------------------------


def finish(findings: list[Finding], warnings: list[Finding], gate: str) -> int:
    for item in warnings:
        print(item.render("WARN"))
    for item in findings:
        print(item.render("FAIL"))
    if findings:
        print(f"{gate}: FAIL ({len(findings)} finding(s), {len(warnings)} warning(s))")
        return EXIT_FINDINGS
    # 零命中只说明这些机械检查没发现问题，不说明文稿正确
    print(f"{gate}: no mechanical findings ({len(warnings)} warning(s)) — judgment items still apply")
    return EXIT_CLEAN


def usage_error(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return EXIT_USAGE
