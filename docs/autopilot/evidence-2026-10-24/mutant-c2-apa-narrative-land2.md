# Mutant — mutant-c2-apa-narrative-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:06:51Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 1aa6cbe444c8881dcc9234ada6d408a8d8bc455838a8ceae8ec5aa6a9dfd5a18
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
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_narrative_citation_is_reconciled\b; expected exit: 1
- mutated files: research-proposal/scripts/integrity_gate.py
- patch sha256: 7a46ec65aca188b51cc1eb63eac4b989a9427e5e0ad3cdfaab931fb3de122a6a

```diff
diff --git a/research-proposal/scripts/integrity_gate.py b/research-proposal/scripts/integrity_gate.py
index 5a48db2..042b705 100644
--- a/research-proposal/scripts/integrity_gate.py
+++ b/research-proposal/scripts/integrity_gate.py
@@ -183,7 +183,7 @@ def apa_citations(lines: list[tuple[int, str]]) -> dict[str, int]:
                 if match := APA_PART_RE.match(part.strip()):
                     for year in re.findall(_YEAR, match.group(2)):  # (Smith, 2020, 2022) 是两条
                         found.setdefault(apa_key(match.group(1), year), number)
-        for match in APA_NARRATIVE_RE.finditer(line):
+        for match in []:
             for year in re.findall(_YEAR, match.group(2)):
                 found.setdefault(apa_key(match.group(1), year), number)
     return found

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
42 passed in 0.11s

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
.F..F.F.F.F...F....FF...........F.........                               [100%]
=================================== FAILURES ===================================
_____ CheckProposalTest.test_ai_tell_inside_references_titles_is_not_body ______

self = <test_check_proposal.CheckProposalTest testMethod=test_ai_tell_inside_references_titles_is_not_body>

    def test_ai_tell_inside_references_titles_is_not_body(self):
        text = APA_CLEAN.replace("Costs of rare-event detection", "A study that sheds light on costs")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:264: AssertionError
_________ CheckProposalTest.test_apa_narrative_citation_is_reconciled __________

self = <test_check_proposal.CheckProposalTest testMethod=test_apa_narrative_citation_is_reconciled>

    def test_apa_narrative_citation_is_reconciled(self):
        code, out = self.run_gate(APA_CLEAN.replace("Okafor et al. (2021)", "Okafor et al. (2020)"))
        self.assertEqual(code, 1, out)
>       self.assertIn("okafor, 2020 has no entry", out)
E       AssertionError: 'okafor, 2020 has no entry' not found in 'FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:113: AssertionError
___________ CheckProposalTest.test_auto_detects_numeric_from_entries ___________

self = <test_check_proposal.CheckProposalTest testMethod=test_auto_detects_numeric_from_entries>

    def test_auto_detects_numeric_from_entries(self):
        code, out = self.run_gate(NUMERIC_CLEAN, "--style", "numeric")
        self.assertEqual(code, 0, out)
        code, out = self.run_gate(APA_CLEAN, "--style", "apa")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:88: AssertionError
_________ CheckProposalTest.test_chinese_et_al_is_keyed_by_the_surname _________

self = <test_check_proposal.CheckProposalTest testMethod=test_chinese_et_al_is_keyed_by_the_surname>

    def test_chinese_et_al_is_keyed_by_the_surname(self):
        text = APA_CLEAN.replace("(Smith, 2024)", "（张伟等，2024）").replace(
            "Smith, J. (2024). Costs", "张伟, 李四. (2024). Costs")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:224: AssertionError
_______________ CheckProposalTest.test_clean_apa_proposal_passes _______________

self = <test_check_proposal.CheckProposalTest testMethod=test_clean_apa_proposal_passes>

    def test_clean_apa_proposal_passes(self):
        code, out = self.run_gate(APA_CLEAN)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:78: AssertionError
_____ CheckProposalTest.test_exempt_personalization_fields_are_not_flagged _____

self = <test_check_proposal.CheckProposalTest testMethod=test_exempt_personalization_fields_are_not_flagged>

    def test_exempt_personalization_fields_are_not_flagged(self):
        for text in (APA_CLEAN, NUMERIC_CLEAN):
            with self.subTest(style="apa" if text is APA_CLEAN else "numeric"):
                code, out = self.run_gate(text)
                self.assertNotIn("scaffold-bracket", out)
>               self.assertEqual(code, 0, out)
E               AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E               check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:175: AssertionError
___ CheckProposalTest.test_latin_narrative_after_cjk_and_diacritic_surnames ____

self = <test_check_proposal.CheckProposalTest testMethod=test_latin_narrative_after_cjk_and_diacritic_surnames>

    def test_latin_narrative_after_cjk_and_diacritic_surnames(self):
        text = APA_CLEAN + "\n## 补充\n\n根据Okafor et al. (2019)，又见 (Müller, 2020)。\n"
        # 新段落在 References 之后但是同级标题 → 回到正文；两处都是孤儿引用
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
>       self.assertIn("okafor, 2019 has no entry", out)
E       AssertionError: 'okafor, 2019 has no entry' not found in 'FAIL [citation-without-entry] proposal.md:22: müller, 2020 has no entry in the References list\nFAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text\ncheck_proposal: FAIL (2 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:217: AssertionError
_ CheckProposalTest.test_leftover_instruction_in_references_fails_but_apa_descriptors_pass _

self = <test_check_proposal.CheckProposalTest testMethod=test_leftover_instruction_in_references_fails_but_apa_descriptors_pass>

    def test_leftover_instruction_in_references_fails_but_apa_descriptors_pass(self):
        code, out = self.run_gate(APA_CLEAN + "\n[Follow appropriate citation style: APA, MLA, or Chicago]\n")
        self.assertEqual(code, 1, out)
        self.assertIn("[scaffold-bracket]", out)
        code, out = self.run_gate(NUMERIC_CLEAN + "\n*总字数：[约5,000字，不含参考文献]*\n")
        self.assertEqual(code, 1, out)
        self.assertIn("[scaffold-bracket]", out)
        code, out = self.run_gate(APA_CLEAN.replace("*Sensors*, 24(3), 77-90.",
                                                   "*Sensors*, 24(3), 77-90. [Data set]"))
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:249: AssertionError
________ CheckProposalTest.test_unverified_flag_fails_unless_disclosed _________

self = <test_check_proposal.CheckProposalTest testMethod=test_unverified_flag_fails_unless_disclosed>

    def test_unverified_flag_fails_unless_disclosed(self):
        text = APA_CLEAN.replace("costly (Smith, 2024).", "costly (Smith, 2024) [UNVERIFIED: Ito 2019].")
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
        code, out = self.run_gate(text, "--allow-disclosed-flags")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : WARN [placeholder] proposal.md:7: '[UNVERIFIED: Ito 2019]' in: Rare-event detection in streaming sensor data remains costly (Smith, 2024) [UNVE
E       FAIL [entry-never-cited] proposal.md References line 16: okafor, 2021 is listed but never cited in the text
E       check_proposal: FAIL (1 finding(s), 1 warning(s))

tests/test_check_proposal.py:152: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_ai_tell_inside_references_titles_is_not_body
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_narrative_citation_is_reconciled
FAILED tests/test_check_proposal.py::CheckProposalTest::test_auto_detects_numeric_from_entries
FAILED tests/test_check_proposal.py::CheckProposalTest::test_chinese_et_al_is_keyed_by_the_surname
FAILED tests/test_check_proposal.py::CheckProposalTest::test_clean_apa_proposal_passes
FAILED tests/test_check_proposal.py::CheckProposalTest::test_exempt_personalization_fields_are_not_flagged
FAILED tests/test_check_proposal.py::CheckProposalTest::test_latin_narrative_after_cjk_and_diacritic_surnames
FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_instruction_in_references_fails_but_apa_descriptors_pass
FAILED tests/test_check_proposal.py::CheckProposalTest::test_unverified_flag_fails_unless_disclosed
9 failed, 33 passed in 0.19s

```
- finished: 2026-10-24T16:06:56Z
- result: KILLED
