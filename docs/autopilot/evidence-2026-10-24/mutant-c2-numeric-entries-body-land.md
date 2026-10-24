# Mutant — mutant-c2-numeric-entries-body-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:41:30Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: df4db561a2e851a8a37976c106ad9055a45cca27d6d2c2ad24baa400e357ae90
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
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_citation_without_entry_fails\b; expected exit: 1
- mutated files: research-proposal/scripts/check_proposal.py
- patch sha256: 10846a685c4822cb61c2e527bb65668db7347b621c15c918915a299768735ccd

```diff
diff --git a/research-proposal/scripts/check_proposal.py b/research-proposal/scripts/check_proposal.py
index f111820..5a46068 100644
--- a/research-proposal/scripts/check_proposal.py
+++ b/research-proposal/scripts/check_proposal.py
@@ -94,7 +94,7 @@ def check_citations(path: Path, body, refs, style: str) -> list[Finding]:
     if style == "numeric":
         cited = {f"[{key}]": line for key, line in numeric_cited.items()}
         listed = {f"[{key}]": f"{path.name} References {where}"
-                  for key, where in numeric_entries(refs).items()}
+                  for key, where in numeric_entries(body).items()}
     else:
         cited = apa_cited
         listed = {<redacted> References {where}" for key, where in apa_entries(refs).items()}

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
......F....F..F..F........FFFF.F..........                               [100%]
=================================== FAILURES ===================================
___________ CheckProposalTest.test_auto_detects_numeric_from_entries ___________

self = <test_check_proposal.CheckProposalTest testMethod=test_auto_detects_numeric_from_entries>

    def test_auto_detects_numeric_from_entries(self):
        code, out = self.run_gate(NUMERIC_CLEAN, "--style", "numeric")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list
E       check_proposal: FAIL (4 finding(s), 0 warning(s))

tests/test_check_proposal.py:86: AssertionError
_____________ CheckProposalTest.test_clean_numeric_proposal_passes _____________

self = <test_check_proposal.CheckProposalTest testMethod=test_clean_numeric_proposal_passes>

    def test_clean_numeric_proposal_passes(self):
        code, out = self.run_gate(NUMERIC_CLEAN)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list
E       check_proposal: FAIL (4 finding(s), 0 warning(s))

tests/test_check_proposal.py:82: AssertionError
_____ CheckProposalTest.test_exempt_personalization_fields_are_not_flagged _____

self = <test_check_proposal.CheckProposalTest testMethod=test_exempt_personalization_fields_are_not_flagged>

    def test_exempt_personalization_fields_are_not_flagged(self):
        for text in (APA_CLEAN, NUMERIC_CLEAN):
            with self.subTest(style="apa" if text is APA_CLEAN else "numeric"):
                code, out = self.run_gate(text)
                self.assertNotIn("scaffold-bracket", out)
>               self.assertEqual(code, 0, out)
E               AssertionError: 1 != 0 : FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list
E               FAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list
E               FAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list
E               FAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list
E               check_proposal: FAIL (4 finding(s), 0 warning(s))

tests/test_check_proposal.py:175: AssertionError
__________ CheckProposalTest.test_fullwidth_comma_in_numeric_citation __________

self = <test_check_proposal.CheckProposalTest testMethod=test_fullwidth_comma_in_numeric_citation>

    def test_fullwidth_comma_in_numeric_citation(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2，4]"))
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list
E       check_proposal: FAIL (4 finding(s), 0 warning(s))

tests/test_check_proposal.py:198: AssertionError
__ CheckProposalTest.test_numbered_list_references_are_reconciled_not_skipped __

self = <test_check_proposal.CheckProposalTest testMethod=test_numbered_list_references_are_reconciled_not_skipped>

    def test_numbered_list_references_are_reconciled_not_skipped(self):
        # 回归（对抗方 S2 阻断）：文献表写成 `1. …` 时 auto 回退 APA，数字引用整体被忽略
        text = NUMERIC_CLEAN.replace("[1] 史密斯", "1. 史密斯").replace("[2] 加西亚", "2. 加西亚")
        text = text.replace("[3] 王", "3. 王").replace("[4] 奥卡福", "4. 奥卡福")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list
E       FAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list
E       check_proposal: FAIL (4 finding(s), 0 warning(s))

tests/test_check_proposal.py:184: AssertionError
_________ CheckProposalTest.test_numeric_citation_without_entry_fails __________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_citation_without_entry_fails>

    def test_numeric_citation_without_entry_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2, 5]"))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"FAIL \[citation-without-entry\] proposal\.md:\d+: \[5\]")
>       self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[4\]")
E       AssertionError: Regex didn't match: 'FAIL \\[entry-never-cited\\] .*\\[4\\]' not found in 'FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:8: [5] has no entry in the References list\ncheck_proposal: FAIL (4 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:121: AssertionError
____________ CheckProposalTest.test_numeric_entry_never_cited_fails ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_entry_never_cited_fails>

    def test_numeric_entry_never_cited_fails(self):
        code, out = self.run_gate(NUMERIC_CLEAN + "[5] 未引用. 题名[J]. 刊名, 2020, 1: 1-2.\n")
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[5\]")
E       AssertionError: Regex didn't match: 'FAIL \\[entry-never-cited\\] .*\\[5\\]' not found in 'FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list\ncheck_proposal: FAIL (4 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:132: AssertionError
_________________ CheckProposalTest.test_numeric_range_expands _________________

self = <test_check_proposal.CheckProposalTest testMethod=test_numeric_range_expands>

    def test_numeric_range_expands(self):
        # [2-3] 覆盖 [3]；去掉区间后 [3] 成为未被引用的条目
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2-3]", "[2]"))
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"FAIL \[entry-never-cited\] .*\[3\]")
E       AssertionError: Regex didn't match: 'FAIL \\[entry-never-cited\\] .*\\[3\\]' not found in 'FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list\ncheck_proposal: FAIL (3 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:127: AssertionError
_ CheckProposalTest.test_references_subheadings_stay_in_the_references_section _

self = <test_check_proposal.CheckProposalTest testMethod=test_references_subheadings_stay_in_the_references_section>

    def test_references_subheadings_stay_in_the_references_section(self):
        text = NUMERIC_CLEAN.replace("[3] 王", "### 外文文献\n\n[3] 王") + "[5] 未引. 题名[J]. 刊, 2020.\n"
        code, out = self.run_gate(text)
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"\[entry-never-cited\] .*\[5\]")
E       AssertionError: Regex didn't match: '\\[entry-never-cited\\] .*\\[5\\]' not found in 'FAIL [citation-without-entry] proposal.md:7: [1] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [2] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:7: [3] has no entry in the References list\nFAIL [citation-without-entry] proposal.md:8: [4] has no entry in the References list\ncheck_proposal: FAIL (4 finding(s), 0 warning(s))\n'

tests/test_check_proposal.py:238: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_auto_detects_numeric_from_entries
FAILED tests/test_check_proposal.py::CheckProposalTest::test_clean_numeric_proposal_passes
FAILED tests/test_check_proposal.py::CheckProposalTest::test_exempt_personalization_fields_are_not_flagged
FAILED tests/test_check_proposal.py::CheckProposalTest::test_fullwidth_comma_in_numeric_citation
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numbered_list_references_are_reconciled_not_skipped
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_citation_without_entry_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_entry_never_cited_fails
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numeric_range_expands
FAILED tests/test_check_proposal.py::CheckProposalTest::test_references_subheadings_stay_in_the_references_section
9 failed, 33 passed in 0.17s

```
- finished: 2026-10-24T15:41:34Z
- result: KILLED
