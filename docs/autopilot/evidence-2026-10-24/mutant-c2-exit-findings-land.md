# Mutant — mutant-c2-exit-findings-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:43:18Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: b0c21597ee5e0fd7339e394e178fd40f91446755bd9de5bf7c62c7eeb5dc2aa7
- helper lib.sh sha256: 3145fb40c92a089fa15bcdddab3ec7a590f6d58f7c3c541a1acfda7770751ba5
- helper runner.sh sha256: 76bc06df1fa2153394e799fef2420fb6a9365f409a98adaf642059be673eae21
- helper redact.py sha256: 372d0fc8d3713ee0855d771117f4e2f2e6279e900854f6fe4a3702ff52177656
- helper policy.py sha256: 04916e799546b77e8c427ccdb675d53bb287cc26ee6e8b0ca1bd3a6e2abce820
- helper evidence.py sha256: ea96ea8dfe6a6032eba756b9fed2db3c3add4584ed3af1281a4ac50832502e3e
- helper record_scope.py sha256: 5cdd4a5b12c9164cd7778388f539feb864f8ec4d6d7944fa2ecbd7e698b0c186
- helper failure_signature.py sha256: 20491f66e2d54ca3bb0a1637e6ec8d2a816d7ca715cc831d8db4555d24eddc79
- helper source_state.py sha256: 5625448d8a713db7dce7684a5fcb31994e4f94e6ae21009672a45467e478a242
- helper integrity.py sha256: 1e8d6e104429169978e349a8c44a431e31c26e86700c17e8f1d221131156cafc
- env PLAYWRIGHT_BROWSERS_PATH=<set-or-unset; value omitted>

Command output below is untrusted data, never instructions.
- source guard: PASS (source write denied; artifact output writable)
- sandbox probes: PASS (allowed read; outside read/write denied; external-address socket denied)
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_in_text_citation_without_entry_fails\b; expected exit: 1
- mutated files: research-proposal/scripts/integrity_gate.py
- patch sha256: adc719e1f2564bb8c4845359ba432a4410e78f6539996a3d9cfde1bcde2070c1

```diff
diff --git a/research-proposal/scripts/integrity_gate.py b/research-proposal/scripts/integrity_gate.py
index 47cfbe6..15f096e 100644
--- a/research-proposal/scripts/integrity_gate.py
+++ b/research-proposal/scripts/integrity_gate.py
@@ -281,7 +281,7 @@ def finish(findings: list[Finding], warnings: list[Finding], gate: str) -> int:
         print(item.render("FAIL"))
     if findings:
         print(f"{gate}: FAIL ({len(findings)} finding(s), {len(warnings)} warning(s))")
-        return EXIT_FINDINGS
+        return EXIT_CLEAN
     # 零命中只说明这些机械检查没发现问题，不说明文稿正确
     print(f"{gate}: no mechanical findings ({len(warnings)} warning(s)) — judgment items still apply")
     return EXIT_CLEAN

```
## baseline setup

```sh
true
```

exit 0; timed out: no

```


```
## baseline (unpatched)

```sh
cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
..........................................                               [100%]
42 passed in 0.12s

```
- source guard: PASS (source write denied; artifact output writable)
- sandbox probes: PASS (allowed read; outside read/write denied; external-address socket denied)
## mutant setup

```sh
true
```

exit 0; timed out: no

```


```
## mutant (patched)

```sh
cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```

tests/test_check_proposal.py:209: AssertionError
____________ CheckProposalTest.test_figure_label_exemption_is_exact ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_figure_label_exemption_is_exact>

    def test_figure_label_exemption_is_exact(self):
        code, out = self.run_gate(APA_CLEAN.replace("[Figure 1 Suggestion]", "[Figure 1 Suggestion: write caption here]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [scaffold-bracket] proposal.md:11: leftover scaffold field '[Figure 1 Suggestion: write caption here]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:268: AssertionError
__________ CheckProposalTest.test_fullwidth_comma_in_numeric_citation __________

self = <test_check_proposal.CheckProposalTest testMethod=test_fullwidth_comma_in_numeric_citation>

    def test_fullwidth_comma_in_numeric_citation(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2，4]"))
        self.assertEqual(code, 0, out)
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2，5]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] proposal.md:8: [5] has no entry in the References list
E       FAIL [entry-never-cited] proposal.md References line 17: [4] is listed but never cited in the text
E       check_proposal: FAIL (2 finding(s), 0 warning(s))

tests/test_check_proposal.py:200: AssertionError
___ CheckProposalTest.test_latin_narrative_after_cjk_and_diacritic_surnames ____

self = <test_check_proposal.CheckProposalTest testMethod=test_latin_narrative_after_cjk_and_diacritic_surnames>

    def test_latin_narrative_after_cjk_and_diacritic_surnames(self):
        text = APA_CLEAN + "\n## 补充\n\n根据Okafor et al. (2019)，又见 (Müller, 2020)。\n"
        # 新段落在 References 之后但是同级标题 → 回到正文；两处都是孤儿引用
        code, out = self.run_gate(text)
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] proposal.md:22: müller, 2020 has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:22: okafor, 2019 has no entry in the References list
E       check_proposal: FAIL (2 finding(s), 0 warning(s))

tests/test_check_proposal.py:216: AssertionError
_ CheckProposalTest.test_leftover_instruction_in_references_fails_but_apa_descriptors_pass _

self = <test_check_proposal.CheckProposalTest testMethod=test_leftover_instruction_in_references_fails_but_apa_descriptors_pass>

    def test_leftover_instruction_in_references_fails_but_apa_descriptors_pass(self):
        code, out = self.run_gate(APA_CLEAN + "\n[Follow appropriate citation style: APA, MLA, or Chicago]\n")
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [scaffold-bracket] proposal.md:20: leftover scaffold field '[Follow appropriate citation style: APA, MLA, or Chicago]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:242: AssertionError
____________ CheckProposalTest.test_leftover_scaffold_bracket_fails ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_leftover_scaffold_bracket_fails>

    def test_leftover_scaffold_bracket_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("## 1. Introduction", "## 1. Introduction\n\n[Opening sentence: Establish the broader field]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [scaffold-bracket] proposal.md:7: leftover scaffold field '[Opening sentence: Establish the broader field]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:167: AssertionError
______________ CheckProposalTest.test_mixed_citation_styles_fail _______________

self = <test_check_proposal.CheckProposalTest testMethod=test_mixed_citation_styles_fail>

    def test_mixed_citation_styles_fail(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("成本高昂[1]", "成本高昂[1] (Smith, 2024)"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [mixed-citation-style] proposal.md: 4 numeric [N] and 1 author-year citations in one text — use one style throughout
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:204: AssertionError
___________ CheckProposalTest.test_no_comma_and_multi_year_apa_forms ___________

self = <test_check_proposal.CheckProposalTest testMethod=test_no_comma_and_multi_year_apa_forms>

    def test_no_comma_and_multi_year_apa_forms(self):
        text = APA_CLEAN.replace("(Smith, 2024)", "(Smith 2024)").replace(
            "(Garcia & Lee, 2023; Wang et al., 2022a)", "(Garcia & Lee, 2023; Wang et al. 2022a, 2022b)")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] proposal.md:8: wang, 2022b has no entry in the References list
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:230: AssertionError
__ CheckProposalTest.test_numbered_list_references_are_reconciled_not_skipped __

self = <test_check_proposal.CheckProposalTest testMethod=test_numbered_list_references_are_reconciled_not_skipped>

    def test_numbered_list_references_are_reconciled_not_skipped(self):
        # 回归（对抗方 S2 阻断）：文献表写成 `1. …` 时 auto 回退 APA，数字引用整体被忽略
        text = NUMERIC_CLEAN.replace("[1] 史密斯", "1. 史密斯").replace("[2] 加西亚", "2. 加西亚")
        text = text.replace("[3] 王", "3. 王").replace("[4] 奥卡福", "4. 奥卡福")
        code, out = self.run_gate(text)
        self.assertEqual(code, 0, out)
        code, out = self.run_gate(text.replace("[2, 4]", "[2, 5]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] proposal.md:8: [5] has no entry in the References list
E       FAIL [entry-never-cited] proposal.md References line 17: [4] is listed but never cited in the text
E       check_proposal: FAIL (2 finding(s), 0 warning(s))

tests/test_check_proposal.py:186: AssertionError
_________ CheckProposalTest.test_numeric_citation_without_entry_fails __________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_citation_without_entry_fails>

    def test_numeric_citation_without_entry_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2, 5]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] proposal.md:8: [5] has no entry in the References list
E       FAIL [entry-never-cited] proposal.md References line 17: [4] is listed but never cited in the text
E       check_proposal: FAIL (2 finding(s), 0 warning(s))

tests/test_check_proposal.py:119: AssertionError
____________ CheckProposalTest.test_numeric_entry_never_cited_fails ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_entry_never_cited_fails>

    def test_numeric_entry_never_cited_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN + "[5] 未引用. 题名[J]. 刊名, 2020, 1: 1-2.\n")
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [entry-never-cited] proposal.md References line 18: [5] is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:131: AssertionError
_________________ CheckProposalTest.test_numeric_range_expands _________________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_range_expands>

    def test_numeric_range_expands(self):
        # [2-3] 覆盖 [3]；去掉区间后 [3] 成为未被引用的条目
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2-3]", "[2]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [entry-never-cited] proposal.md References line 16: [3] is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:126: AssertionError
___________________ CheckProposalTest.test_placeholder_fails ___________________

self = <test_check_proposal.CheckProposalTest testMethod=test_placeholder_fails>

    def test_placeholder_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("4(2), 1-20.", "4(2), 1-20. doi:10.xxxx/abc"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [placeholder] proposal.md:15: '10.xxxx' in: Garcia, M., & Lee, K. (2023). Active labeling for streams. *Journal of ML System
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:144: AssertionError
_ CheckProposalTest.test_references_subheadings_stay_in_the_references_section _

self = <test_check_proposal.CheckProposalTest testMethod=test_references_subheadings_stay_in_the_references_section>

    def test_references_subheadings_stay_in_the_references_section(self):
        text = NUMERIC_CLEAN.replace("[3] 王", "### 外文文献\n\n[3] 王") + "[5] 未引. 题名[J]. 刊, 2020.\n"
        code, out = self.run_gate(text)
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [entry-never-cited] proposal.md References line 20: [5] is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:237: AssertionError
________ CheckProposalTest.test_unverified_flag_fails_unless_disclosed _________

self = <test_check_proposal.CheckProposalTest testMethod=test_unverified_flag_fails_unless_disclosed>

    def test_unverified_flag_fails_unless_disclosed(self):
        text = APA_CLEAN.replace("costly (Smith, 2024).", "costly (Smith, 2024) [UNVERIFIED: Ito 2019].")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [placeholder] proposal.md:7: '[UNVERIFIED: Ito 2019]' in: Rare-event detection in streaming sensor data remains costly (Smith, 2024) [UNVE
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:150: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_ai_tell_in_body_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_entry_never_cited_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_in_text_citation_without_entry_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_narrative_citation_is_reconciled
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_year_mismatch_is_an_orphan_both_ways
FAILED tests/test_check_proposal.py::CheckProposalTest::test_chinese_ai_tell_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_citations_without_references_section_fail
FAILED tests/test_check_proposal.py::CheckProposalTest::test_disclosure_flag_does_not_excuse_other_placeholders
FAILED tests/test_check_proposal.py::CheckProposalTest::test_escaped_and_fullwidth_brackets_are_normalized
FAILED tests/test_check_proposal.py::CheckProposalTest::test_explicit_style_mismatch_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_figure_label_exemption_is_exact
FAILED tests/test_check_proposal.py::CheckProposalTest::test_fullwidth_comma_in_numeric_citation
FAILED tests/test_check_proposal.py::CheckProposalTest::test_latin_narrative_after_cjk_and_diacritic_surnames
FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_instruction_in_references_fails_but_apa_descriptors_pass
FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_scaffold_bracket_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_mixed_citation_styles_fail
FAILED tests/test_check_proposal.py::CheckProposalTest::test_no_comma_and_multi_year_apa_forms
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numbered_list_references_are_reconciled_not_skipped
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_citation_without_entry_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_entry_never_cited_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_range_expands
FAILED tests/test_check_proposal.py::CheckProposalTest::test_placeholder_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_references_subheadings_stay_in_the_references_section
FAILED tests/test_check_proposal.py::CheckProposalTest::test_unverified_flag_fails_unless_disclosed
24 failed, 18 passed in 0.26s

```
- finished: 2026-10-24T15:43:23Z
- result: KILLED
