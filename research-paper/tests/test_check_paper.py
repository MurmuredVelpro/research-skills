"""check_paper.py 的行为测试：每个门禁各有一个能让它失败的输入，外加一份干净稿。"""

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

import check_paper  # noqa: E402

CLEAN_DRAFT = """# A Model for X

## Abstract

On the external test set (n=412) the model reached a mean Dice of 0.847
(95% CI 0.82-0.87), improving AUC by 4.1 points over the baseline [@smith2024model].

## 2. Methods

### 2.1 Data

We followed the split protocol of @lee2023split and trained for 200 epochs.

## 3. Results

Sensitivity was 91.5% on the internal set.

## References

Smith J. Model. Radiology. 2024;310(2):1-12. doi:10.1148/radiol.2024.0001
"""

LEDGER = """claim_id,section,claim_text,value,unit,dispersion,source_artifact,source_locator,status
R1,Abstract,external test n,412,,,results/split.csv,row 2,verified
R2,Abstract,mean Dice,0.847,,95% CI 0.82-0.87,results/external_test.csv,row 14,verified
R3,Abstract,AUC gain,4.1,points,,results/main_table.tex,Table 1,verified
R4,Results,sensitivity,91.5,%,,results/internal.csv,row 3,verified
"""

BIB = """@article{smith2024model,
  title = {Model},
  author = {Smith, J.},
  year = {2024},
}
@inproceedings{lee2023split,
  title = {Split},
  author = {Lee, K.},
  year = {2023},
}
"""

CHECKLIST = """# CLAIM 2024

| Item | Location / disposition |
|---|---|
| 1. Title identifies AI methodology | Title |
| 2. Abstract structured summary | Abstract |
"""


class CheckPaperTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.write(draft=CLEAN_DRAFT, ledger=LEDGER, bib=BIB, checklist=CHECKLIST)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, *, draft=None, ledger=None, bib=None, checklist=None) -> None:
        for name, content in (("paper_draft.md", draft), ("results_ledger.csv", ledger),
                              ("references.bib", bib), ("checklist_claim.md", checklist)):
            if content is not None:
                (self.dir / name).write_text(content, encoding="utf-8")

    def run_gate(self, *extra: str) -> tuple[int, str]:
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_paper.main([
                str(self.dir / "paper_draft.md"),
                "--ledger", str(self.dir / "results_ledger.csv"),
                "--bib", str(self.dir / "references.bib"),
                *extra,
            ])
        return code, out.getvalue()

    # --- clean -------------------------------------------------------------------------------

    def test_clean_fixture_passes(self):
        code, out = self.run_gate()
        self.assertEqual(code, 0, out)
        self.assertNotIn("FAIL", out)

    # --- (a) numbers ↔ ledger ----------------------------------------------------------------

    def test_untraced_decimal_fails_and_is_named(self):
        self.write(draft=CLEAN_DRAFT.replace("Sensitivity was 91.5%", "Specificity was 0.912"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[number-not-in-ledger\] paper_draft\.md:\d+: '0\.912'")

    def test_untraced_percentage_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("91.5%", "93.0%"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("'93.0%'", out)

    def test_untraced_sample_size_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("(n=412)", "(n=1,204)"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("'n=1,204'", out)

    def test_pending_flag_headings_and_references_are_not_numbers(self):
        draft = CLEAN_DRAFT.replace(
            "Sensitivity was 91.5% on the internal set.",
            "Sensitivity was 91.5% on the internal set; specificity [PENDING: 0.93 from rerun].",
        )
        self.write(draft=draft)
        code, out = self.run_gate("--allow-disclosed-flags")
        self.assertEqual(code, 0, out)
        self.assertNotIn("number-not-in-ledger", out)

    # --- (b) citekeys ↔ bib ------------------------------------------------------------------

    def test_citekey_without_bib_entry_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("[@smith2024model]", "[@smith2024model; @ghost2025]"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[citation-without-entry\] paper_draft\.md:\d+: ghost2025")

    def test_bib_entry_never_cited_fails(self):
        self.write(bib=BIB + "@article{orphan2022,\n  title = {Orphan},\n  year = {2022},\n}\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("[entry-never-cited]", out)
        self.assertIn("orphan2022", out)

    def test_allow_uncited_exempts_only_the_named_entry(self):
        self.write(bib=BIB + "@article{orphan2022,\n  title = {Orphan},\n  year = {2022},\n}\n")
        code, out = self.run_gate("--allow-uncited", "orphan2022")
        self.assertEqual(code, 0, out)

    def test_email_address_is_not_a_citekey(self):
        self.write(draft=CLEAN_DRAFT + "\nContact: author@example.org\n")
        code, out = self.run_gate()
        self.assertEqual(code, 0, out)

    # --- (c) placeholder / AI-tell -----------------------------------------------------------

    def test_fake_doi_placeholder_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("doi:10.1148/radiol.2024.0001", "doi:10.xxxx/abc"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("[placeholder]", out)

    def test_pending_flag_fails_unless_disclosed(self):
        self.write(draft=CLEAN_DRAFT + "\nExternal AUC [PENDING: user to supply].\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL [placeholder]", out)
        code, out = self.run_gate("--allow-disclosed-flags")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN [placeholder]", out)

    def test_ai_tell_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("## 2. Methods", "In recent years, X grew.\n\n## 2. Methods"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("[ai-tell]", out)

    # --- (d) checklist -----------------------------------------------------------------------

    def test_checklist_row_without_disposition_fails(self):
        self.write(checklist=CHECKLIST + "| 3. Data sources |  |\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[checklist-undisposed\] checklist_claim\.md:\d+: .*3\. Data sources")

    def test_missing_checklist_fails_unless_skipped(self):
        (self.dir / "checklist_claim.md").unlink()
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("[checklist-missing]", out)
        code, out = self.run_gate("--skip-checklist")
        self.assertEqual(code, 0, out)

    # --- usage -------------------------------------------------------------------------------

    def test_missing_input_is_usage_error_not_pass(self):
        (self.dir / "references.bib").unlink()
        code, _ = self.run_gate()
        self.assertEqual(code, 2)


class GatePatternsMatchSkillDoc(unittest.TestCase):
    """脚本里的模式必须与 SKILL.md Phase 5 的 grep 逐字相同——两套门禁不许漂移。"""

    def test_placeholder_pattern_is_the_documented_grep(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        documented = re.search(r'grep -nE "([^"]+)" paper_draft\.md', text).group(1)
        self.assertEqual(check_paper.PLACEHOLDER_PATTERN, documented)

    def test_ai_tell_pattern_is_the_documented_grep(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        documented = re.search(r'grep -nEi "([^"]+)" paper_draft\.md', text).group(1)
        self.assertEqual(check_paper.AI_TELL_PATTERN, documented)


if __name__ == "__main__":
    unittest.main()
