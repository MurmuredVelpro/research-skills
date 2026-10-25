# Mutant — mutant-c1a-invert-ledger-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:04:58Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 0d10c22927c1e9bddf9259ced2060c8d91160631a5919a6b520f0846a7ba85dc
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_decimal_fails_and_is_named\b; expected exit: 1
- mutated files: research-paper/scripts/check_paper.py
- patch sha256: 9c48e34669c6aa68c521deae94f8c073a16e7f03c4864f2a1df8caf1108f4845

```diff
diff --git a/research-paper/scripts/check_paper.py b/research-paper/scripts/check_paper.py
index 816d8ac..2b2347a 100644
--- a/research-paper/scripts/check_paper.py
+++ b/research-paper/scripts/check_paper.py
@@ -58,7 +58,7 @@ def check_numbers(draft: Path, body: list[tuple[int, str]], ledger: Path) -> lis
         Finding("number-not-in-ledger", f"{draft.name}:{line}",
                 f"'{raw}' is not covered by any {ledger.name} value — trace it or flag it [PENDING: …]")
         for line, raw, value in metric_numbers(body)
-        if value not in covered
+        if value in covered
     ]



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
cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
....................................                                     [100%]
36 passed in 0.13s

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
cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```
        (self.dir / "checklist_claim.md").unlink()
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("[checklist-missing]", out)
        code, out = self.run_gate("--skip-checklist")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : WARN [checklist-skipped] -: reporting checklist not checked (--skip-checklist)
E       FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (7 finding(s), 1 warning(s))

tests/test_check_paper.py:283: AssertionError
___________ CheckPaperTest.test_numbers_in_chinese_prose_are_checked ___________

self = <test_check_paper.CheckPaperTest testMethod=test_numbers_in_chinese_prose_are_checked>

    def test_numbers_in_chinese_prose_are_checked(self):
        # 回归（对抗方 S1-1）：\w 含汉字，旧边界让紧贴汉字的数字整句漏检
        draft = CLEAN_DRAFT.replace("## References", "外部验证AUC为0.912。\n\n## References")
        self.write(draft=draft)
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
>       self.assertIn("'0.912'", out)
E       AssertionError: "'0.912'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (7 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:155: AssertionError
___________ CheckPaperTest.test_pending_flag_fails_unless_disclosed ____________

self = <test_check_paper.CheckPaperTest testMethod=test_pending_flag_fails_unless_disclosed>

    def test_pending_flag_fails_unless_disclosed(self):
        self.write(draft=CLEAN_DRAFT + "\nExternal AUC [PENDING: user to supply].\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL [placeholder]", out)
        code, out = self.run_gate("--allow-disclosed-flags")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : WARN [placeholder] paper_draft.md:22: '[PENDING' in: External AUC [PENDING: user to supply].
E       FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (7 finding(s), 1 warning(s))

tests/test_check_paper.py:242: AssertionError
___ CheckPaperTest.test_pending_flag_headings_and_references_are_not_numbers ___

self = <test_check_paper.CheckPaperTest testMethod=test_pending_flag_headings_and_references_are_not_numbers>

    def test_pending_flag_headings_and_references_are_not_numbers(self):
        draft = CLEAN_DRAFT.replace(
            "Sensitivity was 91.5% on the internal set.",
            "Sensitivity was 91.5% on the internal set; specificity [PENDING: 0.93 from rerun].",
        )
        self.write(draft=draft)
        code, out = self.run_gate("--allow-disclosed-flags")
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : WARN [placeholder] paper_draft.md:16: '[PENDING' in: Sensitivity was 91.5% on the internal set; specificity [PENDING: 0.93 from rerun
E       FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (7 finding(s), 1 warning(s))

tests/test_check_paper.py:146: AssertionError
_________ CheckPaperTest.test_references_section_numbers_are_excluded __________

self = <test_check_paper.CheckPaperTest testMethod=test_references_section_numbers_are_excluded>

    def test_references_section_numbers_are_excluded(self):
        # 回归（对抗方 S1-6）：文献表里的 0.62 / 87.5% 不是本文结果；把它挪进正文就必须失败
        code, out = self.run_gate()
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (7 finding(s), 0 warning(s))

tests/test_check_paper.py:197: AssertionError
__ CheckPaperTest.test_section_after_references_at_the_same_level_is_checked ___

self = <test_check_paper.CheckPaperTest testMethod=test_section_after_references_at_the_same_level_is_checked>

    def test_section_after_references_at_the_same_level_is_checked(self):
        # landing review：与 References 同级的 `## Appendix` 结束文献表，里面的数字照样对账
        self.write(draft=CLEAN_DRAFT + "\n## Appendix\n\nExtra AUC 0.777.\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
>       self.assertIn("'0.777'", out)
E       AssertionError: "'0.777'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (7 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:192: AssertionError
__________ CheckPaperTest.test_thousands_separator_matches_the_ledger __________

self = <test_check_paper.CheckPaperTest testMethod=test_thousands_separator_matches_the_ledger>

    def test_thousands_separator_matches_the_ledger(self):
        # 回归（对抗方 S1-4）：账本里的 1,204 是一个数
        self.write(draft=CLEAN_DRAFT.replace("(n=412)", "(n=1,204)"),
                   ledger=LEDGER.replace("external test n,412", 'external test n,"1,204"'))
        code, out = self.run_gate()
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [number-not-in-ledger] paper_draft.md:5: 'n=1,204' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (7 finding(s), 0 warning(s))

tests/test_check_paper.py:185: AssertionError
______ CheckPaperTest.test_unit_glued_and_leading_dot_numbers_are_checked ______

self = <test_check_paper.CheckPaperTest testMethod=test_unit_glued_and_leading_dot_numbers_are_checked>

    def test_unit_glued_and_leading_dot_numbers_are_checked(self):
        # landing review: `12.5ms`、`r = .85`、`95%CI` 曾整段漏检
        for text, shown in (("latency 12.5ms", "12.5"), ("a 2.5x speedup", "2.5"),
                            ("3.5mm slices", "3.5"), ("r = .85", ".85"), ("p < .001", ".001"),
                            ("coverage 97%CI", "97%")):
            with self.subTest(text=text):
                self.write(draft=CLEAN_DRAFT.replace("## References", f"Also {text}.\n\n## References"))
                code, out = self.run_gate()
                self.assertEqual(code, 1, out)
>               self.assertIn(f"'{shown}'", out)
E               AssertionError: "'12.5'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (7 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:124: AssertionError
___________ CheckPaperTest.test_untraced_decimal_fails_and_is_named ____________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_decimal_fails_and_is_named>

    def test_untraced_decimal_fails_and_is_named(self):
        self.write(draft=CLEAN_DRAFT.replace("Sensitivity was 91.5%", "Specificity was 0.912"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
>       self.assertRegex(out, r"FAIL \[number-not-in-ledger\] paper_draft\.md:\d+: '0\.912'")
E       AssertionError: Regex didn't match: "FAIL \\[number-not-in-ledger\\] paper_draft\\.md:\\d+: '0\\.912'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (6 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:107: AssertionError
________________ CheckPaperTest.test_untraced_percentage_fails _________________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_percentage_fails>

    def test_untraced_percentage_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("91.5%", "93.0%"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
>       self.assertIn("'93.0%'", out)
E       AssertionError: "'93.0%'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: 'n=412' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (6 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:113: AssertionError
________________ CheckPaperTest.test_untraced_sample_size_fails ________________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_sample_size_fails>

    def test_untraced_sample_size_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("(n=412)", "(n=1,204)"))
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
>       self.assertIn("'n=1,204'", out)
E       AssertionError: "'n=1,204'" not found in "FAIL [number-not-in-ledger] paper_draft.md:5: '0.847' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '95%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.82' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '0.87' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:6: '4.1' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\nFAIL [number-not-in-ledger] paper_draft.md:16: '91.5%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]\ncheck_paper: FAIL (6 finding(s), 0 warning(s))\n"

tests/test_check_paper.py:137: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_allow_uncited_exempts_only_the_named_entry
FAILED tests/test_check_paper.py::CheckPaperTest::test_bracketed_confidence_interval_is_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_clean_fixture_passes
FAILED tests/test_check_paper.py::CheckPaperTest::test_email_address_is_not_a_citekey
FAILED tests/test_check_paper.py::CheckPaperTest::test_fullwidth_percent_and_equals_are_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_in_the_ledger_matches_the_draft
FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_matches_the_ledger_and_versions_are_not_numbers
FAILED tests/test_check_paper.py::CheckPaperTest::test_missing_checklist_fails_unless_skipped
FAILED tests/test_check_paper.py::CheckPaperTest::test_numbers_in_chinese_prose_are_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_pending_flag_fails_unless_disclosed
FAILED tests/test_check_paper.py::CheckPaperTest::test_pending_flag_headings_and_references_are_not_numbers
FAILED tests/test_check_paper.py::CheckPaperTest::test_references_section_numbers_are_excluded
FAILED tests/test_check_paper.py::CheckPaperTest::test_section_after_references_at_the_same_level_is_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_thousands_separator_matches_the_ledger
FAILED tests/test_check_paper.py::CheckPaperTest::test_unit_glued_and_leading_dot_numbers_are_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_decimal_fails_and_is_named
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_percentage_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_sample_size_fails
18 failed, 18 passed in 0.37s

```
- finished: 2026-10-24T16:05:05Z
- result: KILLED
