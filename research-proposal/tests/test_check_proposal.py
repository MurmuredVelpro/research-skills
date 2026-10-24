"""check_proposal.py 的行为测试：APA 与 GB/T 顺序编码两种引用制式的双向对账、占位符/AI-tell、
scaffold 残留与豁免字段。"""

from __future__ import annotations

import io
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_proposal  # noqa: E402

APA_CLEAN = """# Adaptive Sampling for Rare-Event Detection

**Field:** [Your Field] | **Institution:** [University/Institution Name] | **Date:** [Month Year]

## 1. Introduction

Rare-event detection in streaming sensor data remains costly (Smith, 2024). Prior work
reduced labeling effort by half (Garcia & Lee, 2023; Wang et al., 2022a), and Okafor et al. (2021)
showed that the gain depends on drift.

> **[Figure 1 Suggestion]** *Title: Conceptual overview of research scope*

## References

Garcia, M., & Lee, K. (2023). Active labeling for streams. *Journal of ML Systems*, 4(2), 1-20.
Okafor, C., Adeyemi, T., & Bello, S. (2021). Drift-aware sampling. *Proc. KDD*, 112-120.
Smith, J. (2024). Costs of rare-event detection. *Sensors*, 24(3), 77-90.
Wang, L., Chen, Y., & Zhou, H. (2022a). Halving annotation effort. *IEEE TKDE*, 34(1), 5-18.
"""

NUMERIC_CLEAN = """# 面向罕见事件检测的自适应采样研究

**所属学科：** [所属学科]　**单位：** [大学/研究机构名称]　**日期：** [年月]

## 一、研究背景

流式传感数据中的罕见事件检测成本高昂[1]。已有工作将标注量减少一半[2-3]，
但其增益依赖于数据漂移[2, 4]。

> **[图1建议]** *标题：研究范围概念图*

## 参考文献

[1] 史密斯. 罕见事件检测的成本[J]. 传感器, 2024, 24(3): 77-90.
[2] 加西亚, 李. 流数据主动标注[J]. 机器学习系统学报, 2023, 4(2): 1-20.
[3] 王, 陈, 周. 减半标注[J]. IEEE TKDE, 2022, 34(1): 5-18.
[4] 奥卡福. 漂移感知采样[C]// KDD, 2021: 112-120.
"""


class CheckProposalTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "proposal.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_gate(self, text: str, *extra: str) -> tuple[int, str]:
        self.path.write_text(text, encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_proposal.main([str(self.path), *extra])
        return code, out.getvalue()

    # --- clean, both styles ------------------------------------------------------------------

    def test_clean_apa_proposal_passes(self):
        code, out = self.run_gate(APA_CLEAN)
        self.assertEqual(code, 0, out)

    def test_clean_numeric_proposal_passes(self):
        code, out = self.run_gate(NUMERIC_CLEAN)
        self.assertEqual(code, 0, out)

    def test_auto_detects_numeric_from_entries(self):
        code, out = self.run_gate(NUMERIC_CLEAN, "--style", "numeric")
        self.assertEqual(code, 0, out)
        code, out = self.run_gate(APA_CLEAN, "--style", "apa")
        self.assertEqual(code, 0, out)

    # --- APA reconciliation ------------------------------------------------------------------

    def test_apa_in_text_citation_without_entry_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("(Smith, 2024)", "(Smith, 2024; Novak, 2020)"))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[citation-without-entry\] proposal\.md:\d+: novak, 2020")

    def test_apa_year_mismatch_is_an_orphan_both_ways(self):
        code, out = self.run_gate(APA_CLEAN.replace("(Smith, 2024)", "(Smith, 2023)"))
        self.assertEqual(code, 1, out)
        self.assertIn("smith, 2023 has no entry", out)
        self.assertIn("[entry-never-cited]", out)
        self.assertIn("smith, 2024 is listed but never cited", out)

    def test_apa_entry_never_cited_fails(self):
        extra = "Zhou, H. (2019). Unused paper. *Venue*, 1, 1-2.\n"
        code, out = self.run_gate(APA_CLEAN + extra)
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[entry-never-cited\] .*zhou, 2019")

    def test_apa_narrative_citation_is_reconciled(self):
        code, out = self.run_gate(APA_CLEAN.replace("Okafor et al. (2021)", "Okafor et al. (2020)"))
        self.assertEqual(code, 1, out)
        self.assertIn("okafor, 2020 has no entry", out)

    # --- numeric reconciliation --------------------------------------------------------------

    def test_numeric_citation_without_entry_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2, 5]"))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[citation-without-entry\] proposal\.md:\d+: \[5\]")
        self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[4\]")

    def test_numeric_range_expands(self):
        # [2-3] 覆盖 [3]；去掉区间后 [3] 成为未被引用的条目
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2-3]", "[2]"))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[3\]")

    def test_numeric_entry_never_cited_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN + "[5] 未引用. 题名[J]. 刊名, 2020, 1: 1-2.\n")
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[5\]")

    def test_citations_without_references_section_fail(self):
        body = NUMERIC_CLEAN.split("## 参考文献")[0]
        code, out = self.run_gate(body)
        self.assertEqual(code, 1, out)
        self.assertIn("[no-references-section]", out)

    # --- placeholder / AI-tell / scaffold ----------------------------------------------------

    def test_placeholder_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("4(2), 1-20.", "4(2), 1-20. doi:10.xxxx/abc"))
        self.assertEqual(code, 1, out)
        self.assertIn("[placeholder]", out)

    def test_unverified_flag_fails_unless_disclosed(self):
        text = APA_CLEAN.replace("costly (Smith, 2024).", "costly (Smith, 2024) [UNVERIFIED: Ito 2019].")
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
        code, out = self.run_gate(text, "--allow-disclosed-flags")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN [placeholder]", out)

    def test_ai_tell_in_body_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("Rare-event detection", "In recent years, rare-event detection"))
        self.assertEqual(code, 1, out)
        self.assertIn("[ai-tell]", out)

    def test_chinese_ai_tell_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("流式传感数据", "近年来，随着流式传感数据"))
        self.assertEqual(code, 1, out)
        self.assertIn("[ai-tell]", out)

    def test_leftover_scaffold_bracket_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("## 1. Introduction", "## 1. Introduction\n\n[Opening sentence: Establish the broader field]"))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[scaffold-bracket\] .*Opening sentence")

    def test_exempt_personalization_fields_are_not_flagged(self):
        for text in (APA_CLEAN, NUMERIC_CLEAN):
            with self.subTest(style="apa" if text is APA_CLEAN else "numeric"):
                code, out = self.run_gate(text)
                self.assertNotIn("scaffold-bracket", out)
                self.assertEqual(code, 0, out)

    def test_missing_file_is_usage_error(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_proposal.main([str(Path(self._tmp.name) / "nope.md")])
        self.assertEqual(code, 2)


class GatePatternsMatchSkillDoc(unittest.TestCase):
    def test_placeholder_pattern_is_the_documented_grep(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        documented = re.search(r'grep -nE "([^"]*UNVERIFIED[^"]*)"', text).group(1)
        self.assertEqual(check_proposal.PLACEHOLDER_PATTERN, documented)

    def test_ai_tell_pattern_is_the_documented_grep(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        documented = re.search(r'grep -nEi "([^"]*over the past[^"]*)"', text).group(1)
        self.assertEqual(check_proposal.AI_TELL_PATTERN, documented)

    def test_exempt_fields_are_the_documented_ones(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for field in check_proposal.EXEMPT_BRACKETS:
            with self.subTest(field=field):
                self.assertIn(f"`[{field}]`", text)


if __name__ == "__main__":
    unittest.main()
