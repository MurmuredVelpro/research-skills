# Mutant — mutant-c2-key-case-land2-r2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:26:45Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: e36fc5f509db3edf8f13351cf9270b29737eb14ec9c2fb5bfc294c44b2e1c4b5
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
- patch sha256: f8519c0cdf8cdb2687c391248e169d0572efdfd77b385c0e2bb47c0c2ec38c08

```diff
diff --git a/research-proposal/scripts/integrity_gate.py b/research-proposal/scripts/integrity_gate.py
index 5a48db2..80b88b3 100644
--- a/research-proposal/scripts/integrity_gate.py
+++ b/research-proposal/scripts/integrity_gate.py
@@ -171,7 +171,7 @@ def numeric_entries(lines: list[tuple[int, str]]) -> dict[str, str]:


 def apa_key(surname: str, year: str) -> str:
-    return f"{surname.lower()}, {year}"
+    return f"{surname}, {year}"


 def apa_citations(lines: list[tuple[int, str]]) -> dict[str, int]:

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
..FFFF.............F....F.................                               [100%]
=================================== FAILURES ===================================
______________ CheckProposalTest.test_apa_entry_never_cited_fails ______________

self = <test_check_proposal.CheckProposalTest testMethod=test_apa_entry_never_cited_fails>

    def test_apa_entry_never_cited_fails(self):
        extra = "Zhou, H. (2019). Unused paper. *Venue*, 1, 1-2.\n"
        code, out = self.run_gate(APA_CLEAN + extra)
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"FAIL \[entry-never-cited\] .*zhou, 2019")
E       AssertionError: Regex didn't match: 'FAIL \\[entry-never-cited\\] .*zhou, 2019' not found in 'FAIL [entry-never-cited] proposal.md References line 19: Zhou, 2019 is listed but never cited in the text\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:108: AssertionError
_______ CheckProposalTest.test_apa_in_text_citation_without_entry_fails ________

self = <test_check_proposal.CheckProposalTest testMethod=test_apa_in_text_citation_without_entry_fails>

    def test_apa_in_text_citation_without_entry_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("(Smith, 2024)", "(Smith, 2024; Novak, 2020)"))
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"FAIL \[citation-without-entry\] proposal\.md:\d+: novak, 2020")
E       AssertionError: Regex didn't match: 'FAIL \\[citation-without-entry\\] proposal\\.md:\\d+: novak, 2020' not found in 'FAIL [citation-without-entry] proposal.md:7: Novak, 2020 has no entry in the References list\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:95: AssertionError
_________ CheckProposalTest.test_apa_narrative_citation_is_reconciled __________

self = <test_check_proposal.CheckProposalTest testMethod=test_apa_narrative_citation_is_reconciled>

    def test_apa_narrative_citation_is_reconciled(self):
        code, out = self.run_gate(APA_CLEAN.replace("Okafor et al. (2021)", "Okafor et al. (2020)"))
        self.assertEqual(code, 1, out)
>       self.assertIn("okafor, 2020 has no entry", out)
E       AssertionError: 'okafor, 2020 has no entry' not found in 'FAIL [citation-without-entry] proposal.md:8: Okafor, 2020 has no entry in the References list\nFAIL [entry-never-cited] proposal.md References line 16: Okafor, 2021 is listed but never cited in the text\ncheck_proposal: FAIL (2 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:113: AssertionError
_______ CheckProposalTest.test_apa_year_mismatch_is_an_orphan_both_ways ________

self = <test_check_proposal.CheckProposalTest testMethod=test_apa_year_mismatch_is_an_orphan_both_ways>

    def test_apa_year_mismatch_is_an_orphan_both_ways(self):
        code, out = self.run_gate(APA_CLEAN.replace("(Smith, 2024)", "(Smith, 2023)"))
        self.assertEqual(code, 1, out)
>       self.assertIn("smith, 2023 has no entry", out)
E       AssertionError: 'smith, 2023 has no entry' not found in 'FAIL [citation-without-entry] proposal.md:7: Smith, 2023 has no entry in the References list\nFAIL [entry-never-cited] proposal.md References line 17: Smith, 2024 is listed but never cited in the text\ncheck_proposal: FAIL (2 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:100: AssertionError
___ CheckProposalTest.test_latin_narrative_after_cjk_and_diacritic_surnames ____

self = <test_check_proposal.CheckProposalTest testMethod=test_latin_narrative_after_cjk_and_diacritic_surnames>

    def test_latin_narrative_after_cjk_and_diacritic_surnames(self):
        text = APA_CLEAN + "\n## 补充\n\n根据Okafor et al. (2019)，又见 (Müller, 2020)。\n"
        # 新段落在 References 之后但是同级标题 → 回到正文；两处都是孤儿引用
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
>       self.assertIn("okafor, 2019 has no entry", out)
E       AssertionError: 'okafor, 2019 has no entry' not found in 'FAIL [citation-without-entry] proposal.md:22: Müller, 2020 has no entry in the References list\nFAIL [citation-without-entry] proposal.md:22: Okafor, 2019 has no entry in the References list\ncheck_proposal: FAIL (2 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:217: AssertionError
___________ CheckProposalTest.test_no_comma_and_multi_year_apa_forms ___________

self = <test_check_proposal.CheckProposalTest testMethod=test_no_comma_and_multi_year_apa_forms>

    def test_no_comma_and_multi_year_apa_forms(self):
        text = APA_CLEAN.replace("(Smith, 2024)", "(Smith 2024)").replace(
            "(Garcia & Lee, 2023; Wang et al., 2022a)", "(Garcia & Lee, 2023; Wang et al. 2022a, 2022b)")
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
>       self.assertIn("wang, 2022b has no entry", out)
E       AssertionError: 'wang, 2022b has no entry' not found in 'FAIL [citation-without-entry] proposal.md:8: Wang, 2022b has no entry in the References list\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:231: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_entry_never_cited_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_in_text_citation_without_entry_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_narrative_citation_is_reconciled
FAILED tests/test_check_proposal.py::CheckProposalTest::test_apa_year_mismatch_is_an_orphan_both_ways
FAILED tests/test_check_proposal.py::CheckProposalTest::test_latin_narrative_after_cjk_and_diacritic_surnames
FAILED tests/test_check_proposal.py::CheckProposalTest::test_no_comma_and_multi_year_apa_forms
6 failed, 36 passed in 0.17s

```
- finished: 2026-10-24T16:26:50Z
- result: KILLED
