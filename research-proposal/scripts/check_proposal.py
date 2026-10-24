#!/usr/bin/env python3
"""research-proposal Phase 5 citation gate.

    python3 scripts/check_proposal.py proposal_<slug>_<date>.md [--style auto|apa|numeric]

Checks, each a FAIL line naming the offending item:

1. citation-without-entry / entry-never-cited — in-text citations ↔ the References list,
   both directions. `apa`: (Smith, 2024) / (Smith et al., 2024a) / Smith and Lee (2024)
   keyed by first-author surname + year. `numeric` (GB/T 7714 顺序编码制): [1], [2-4] ↔ `[N]`
   entries. `auto` picks numeric when the References entries start with `[N]`.
2. placeholder / ai-tell — the SKILL.md Phase 5 grep patterns, same regex (AI-tell: body only).
3. scaffold-bracket — a leftover `[instruction]` from the scaffold. The applicant-specific
   personalization fields and figure-suggestion labels SKILL.md exempts are allowed.

Exit 0: no mechanical findings (not proof the proposal is right). 1: findings. 2: bad input.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from integrity_gate import (  # noqa: E402
    Finding,
    apa_citations,
    apa_entries,
    finish,
    numeric_citations,
    numeric_entries,
    pattern_hits,
    read_text,
    reconcile,
    split_body,
    usage_error,
)

#: 与 SKILL.md Phase 5 的 canonical 占位符 grep 逐字相同（tests/test_check_proposal.py 锁定）
PLACEHOLDER_PATTERN = (
    r"xxx|XXXX|\[TBD\]|\[UNVERIFIED[^]]*\]|10\.xxxx|doi:10\.[a-z]+/x|forthcoming DOI|\[.*占位.*\]"
)
#: 与 SKILL.md Phase 5 的 AI-tell grep -nEi 逐字相同
AI_TELL_PATTERN = (
    r"over the past ((few|several|two|three) )?(decades?|years)|in recent years,|it is worth noting"
    r"|plays a (crucial|pivotal|vital) role|sheds light on|paves the way|ever-evolving"
    r"|has garnered significant attention|delves into|a testament to|众所周知|近年来，?随着|日益受到(广泛)?关注"
)
DISCLOSED_FLAG_RE = re.compile(r"^\[UNVERIFIED")
#: SKILL.md Phase 5 豁免的申请人个性化字段与配图建议标签——用户自己填，允许留在交付稿里
EXEMPT_BRACKETS = {
    "University/Institution Name", "Your Field", "Month Year",
    "所属学科", "大学/研究机构名称", "年月",
}
EXEMPT_BRACKET_RE = re.compile(r"^(Figure \d+ Suggestion|图\s*\d+\s*建议)$")
BRACKET_RE = re.compile(r"(?<!!)\[([^\]\n]+)\](?![(\[:])")
NOT_SCAFFOLD_RE = re.compile(r"^(\d+(\s*[-–—,，]\s*\d+)*|[ xX]|\^.*|@.*|UNVERIFIED.*|TBD)$")


def check_citations(path: Path, body, refs, style: str) -> list[Finding]:
    if not refs:
        # 没有文献表时无从判断制式——两种都数，任何一处引用都说明文献表丢了
        count = len(numeric_citations(body)) + len(apa_citations(body))
        return [Finding("no-references-section", path.name,
                        f"{count} in-text citation(s) but no '## References' / '## 参考文献' section")
                ] if count else []
    if style == "auto":
        style = "numeric" if numeric_entries(refs) else "apa"
    if style == "numeric":
        cited, listed = numeric_citations(body), numeric_entries(refs)
        cited = {f"[{key}]": line for key, line in cited.items()}
        listed = {f"[{key}]": f"{path.name} References {where}" for key, where in listed.items()}
    else:
        cited, listed = apa_citations(body), apa_entries(refs)
        listed = {key: f"{path.name} References {where}" for key, where in listed.items()}
    return reconcile(cited, listed, path.name, "the References list")


def check_patterns(path: Path, text: str, body, allow_flags: bool):
    findings: list[Finding] = []
    warnings: list[Finding] = []
    for line, hit, context in pattern_hits(text, PLACEHOLDER_PATTERN):
        item = Finding("placeholder", f"{path.name}:{line}", f"'{hit}' in: {context[:80]}")
        (warnings if allow_flags and DISCLOSED_FLAG_RE.match(hit) else findings).append(item)
    body_text = "\n".join(line for _, line in body)
    body_numbers = [number for number, _ in body]
    for index, hit, context in pattern_hits(body_text, AI_TELL_PATTERN, ignore_case=True):
        findings.append(Finding("ai-tell", f"{path.name}:{body_numbers[index - 1]}",
                                f"'{hit}' in: {context[:80]}"))
    return findings, warnings


def check_scaffold_brackets(path: Path, body) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in body:
        for match in BRACKET_RE.finditer(line):
            content = match.group(1).strip()
            if (content in EXEMPT_BRACKETS or EXEMPT_BRACKET_RE.match(content)
                    or NOT_SCAFFOLD_RE.match(content)):
                continue
            findings.append(Finding("scaffold-bracket", f"{path.name}:{number}",
                                    f"leftover scaffold field '[{content[:60]}]'"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("proposal", type=Path)
    parser.add_argument("--style", choices=("auto", "apa", "numeric"), default="auto")
    parser.add_argument("--allow-disclosed-flags", action="store_true",
                        help="[UNVERIFIED…] already disclosed to the user: warn, don't fail")
    args = parser.parse_args(argv)
    if not args.proposal.is_file():
        return usage_error(f"proposal not found: {args.proposal}")

    text = read_text(args.proposal)
    body, refs = split_body(text)
    findings = check_citations(args.proposal, body, refs, args.style)
    pattern_findings, warnings = check_patterns(args.proposal, text, body, args.allow_disclosed_flags)
    findings += pattern_findings
    findings += check_scaffold_brackets(args.proposal, body)
    return finish(findings, warnings, "check_proposal")


if __name__ == "__main__":
    sys.exit(main())
