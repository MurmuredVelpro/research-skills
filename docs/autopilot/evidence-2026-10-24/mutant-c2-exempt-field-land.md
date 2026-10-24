# Mutant — mutant-c2-exempt-field-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:42:49Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 23b85ddf0a17547a64bef2363e88f7d28f5a22667290a8b8bc609191ced72918
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
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_exempt_personalization_fields_are_not_flagged\b; expected exit: 1
- mutated files: research-proposal/scripts/check_proposal.py
- patch sha256: 2ef9c4ebbf7f369d27c61dca5de9c12d1d73fd91dcd1b4a0b95357c01bfecf03

```diff
diff --git a/research-proposal/scripts/check_proposal.py b/research-proposal/scripts/check_proposal.py
index f111820..4caeb91 100644
--- a/research-proposal/scripts/check_proposal.py
+++ b/research-proposal/scripts/check_proposal.py
@@ -55,7 +55,7 @@ DISCLOSED_FLAG_RE = re.compile(r"^\[UNVERIFIED")
 #: SKILL.md Phase 5 豁免的申请人个性化字段与配图建议标签——用户自己填，允许留在交付稿里
 EXEMPT_BRACKETS = {
     "University/Institution Name", "Your Field", "Month Year",
-    "所属学科", "大学/研究机构名称", "年月",
+    "大学/研究机构名称", "年月",
 }
 EXEMPT_BRACKET_RE = re.compile(r"^(Figure \d+ Suggestion|图\s*\d+\s*建议)$")
 BRACKET_RE = re.compile(r"(?<!!)\[([^\]\n]+)\](?![(\[:])")

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
42 passed in 0.13s

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
......F....F..F..FF.......F...............                               [100%]
=================================== FAILURES ===================================
___________ CheckProposalTest.test_auto_detects_numeric_from_entries ___________

self = <test_check_proposal.CheckProposalTest testMethod=test_auto_detects_numeric_from_entries>

    def test_auto_detects_numeric_from_entries(self):
        code, out = self.run_gate(NUMERIC_CLEAN, "--style", "numeric")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:86: AssertionError
_____________ CheckProposalTest.test_clean_numeric_proposal_passes _____________

self = <test_check_proposal.CheckProposalTest testMethod=test_clean_numeric_proposal_passes>

    def test_clean_numeric_proposal_passes(self):
        code, out = self.run_gate(NUMERIC_CLEAN)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:82: AssertionError
_____ CheckProposalTest.test_exempt_personalization_fields_are_not_flagged _____

self = <test_check_proposal.CheckProposalTest testMethod=test_exempt_personalization_fields_are_not_flagged>

    def test_exempt_personalization_fields_are_not_flagged(self):
        for text in (APA_CLEAN, NUMERIC_CLEAN):
            with self.subTest(style="apa" if text is APA_CLEAN else "numeric"):
                code, out = self.run_gate(text)
>               self.assertNotIn("scaffold-bracket", out)
E               AssertionError: 'scaffold-bracket' unexpectedly found in "FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n"

tests/test_check_proposal.py:174: AssertionError
__________ CheckProposalTest.test_fullwidth_comma_in_numeric_citation __________

self = <test_check_proposal.CheckProposalTest testMethod=test_fullwidth_comma_in_numeric_citation>

    def test_fullwidth_comma_in_numeric_citation(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[2, 4]", "[2，4]"))
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:198: AssertionError
_______ CheckProposalTest.test_gbt_document_type_codes_are_not_scaffold ________

self = <test_check_proposal.CheckProposalTest testMethod=test_gbt_document_type_codes_are_not_scaffold>

    def test_gbt_document_type_codes_are_not_scaffold(self):
        code, out = self.run_gate(NUMERIC_CLEAN.replace("[C]// KDD", "[EB/OL]. (2021-01-02)[2024-01-01]"))
>       self.assertNotIn("scaffold-bracket", out)
E       AssertionError: 'scaffold-bracket' unexpectedly found in "FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'\ncheck_proposal: FAIL (1 finding(s), 0 warning(s))\n"

tests/test_check_proposal.py:253: AssertionError
__ CheckProposalTest.test_numbered_list_references_are_reconciled_not_skipped __

self = <test_check_proposal.CheckProposalTest testMethod=test_numbered_list_references_are_reconciled_not_skipped>

    def test_numbered_list_references_are_reconciled_not_skipped(self):
        # 回归（对抗方 S2 阻断）：文献表写成 `1. …` 时 auto 回退 APA，数字引用整体被忽略
        text = NUMERIC_CLEAN.replace("[1] 史密斯", "1. 史密斯").replace("[2] 加西亚", "2. 加西亚")
        text = text.replace("[3] 王", "3. 王").replace("[4] 奥卡福", "4. 奥卡福")
        code, out = self.run_gate(text)
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [scaffold-bracket] proposal.md:3: leftover scaffold field '[所属学科]'
E       check_proposal: FAIL (1 finding(s), 0 warning(s))

tests/test_check_proposal.py:184: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_auto_detects_numeric_from_entries
FAILED tests/test_check_proposal.py::CheckProposalTest::test_clean_numeric_proposal_passes
FAILED tests/test_check_proposal.py::CheckProposalTest::test_exempt_personalization_fields_are_not_flagged
FAILED tests/test_check_proposal.py::CheckProposalTest::test_fullwidth_comma_in_numeric_citation
FAILED tests/test_check_proposal.py::CheckProposalTest::test_gbt_document_type_codes_are_not_scaffold
FAILED tests/test_check_proposal.py::CheckProposalTest::test_numbered_list_references_are_reconciled_not_skipped
6 failed, 36 passed in 0.15s

```
- finished: 2026-10-24T15:42:53Z
- result: KILLED
