# Mutant — mutant-c1e-exit-findings

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:09:17Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 97ca6a5495056e8ddfb40b6ccc0dd3500ea95d29d0c44fb91135ecacc15a2da1
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
- mutated files: research-paper/scripts/integrity_gate.py
- patch sha256: 3d09c0e8c44e96973d052ebd4aa1e373f0e0cbfca161bdeba4480d4a382b3618

```diff
diff --git a/research-paper/scripts/integrity_gate.py b/research-paper/scripts/integrity_gate.py
index 3dafe47..73b8bfa 100644
--- a/research-paper/scripts/integrity_gate.py
+++ b/research-paper/scripts/integrity_gate.py
@@ -18,7 +18,7 @@ from dataclasses import dataclass
 from pathlib import Path

 #: 退出码：0 干净；1 有门禁失败；2 用法或输入文件错误（门禁没能运行，不是「通过」）
-EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE = 0, 1, 2
+EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE = 0, 0, 2

 #: 参考文献节的标题——数字门禁与引文正文扫描到此为止（年份、卷期、页码不是结果数字）
 REFERENCES_HEADING_RE = re.compile(

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
...............................                                          [100%]
31 passed in 0.11s

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

tests/test_check_paper.py:214: AssertionError
_______________ CheckPaperTest.test_bib_entry_never_cited_fails ________________

self = <test_check_paper.CheckPaperTest testMethod=test_bib_entry_never_cited_fails>

    def test_bib_entry_never_cited_fails(self):
        self.write(bib=BIB + "@article{orphan2022,\n  title = {Orphan},\n  year = {2022},\n}\n")
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [entry-never-cited] references.bib: orphan2022 is listed but never cited in the text
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:173: AssertionError
_________ CheckPaperTest.test_bracketed_confidence_interval_is_checked _________

self = <test_check_paper.CheckPaperTest testMethod=test_bracketed_confidence_interval_is_checked>

    def test_bracketed_confidence_interval_is_checked(self):
        # 回归（对抗方 S1-2）：只有 [PENDING…] 与引文可豁免，方括号里的置信区间要对账
        self.write(draft=CLEAN_DRAFT.replace("(95% CI 0.82-0.87)", "[95% CI 0.71, 0.80]"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:6: '0.71' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:6: '0.80' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (2 finding(s), 0 warning(s))

tests/test_check_paper.py:143: AssertionError
_________ CheckPaperTest.test_checklist_row_without_disposition_fails __________

self = <test_check_paper.CheckPaperTest testMethod=test_checklist_row_without_disposition_fails>

    def test_checklist_row_without_disposition_fails(self):
        self.write(checklist=CHECKLIST + "| 3. Data sources |  |\n")
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [checklist-undisposed] checklist_claim.md:7: no location or disposition for: 3. Data sources
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:222: AssertionError
____ CheckPaperTest.test_checklist_unchecked_box_tbd_and_missing_cell_fail _____

self = <test_check_paper.CheckPaperTest testMethod=test_checklist_unchecked_box_tbd_and_missing_cell_fail>

    def test_checklist_unchecked_box_tbd_and_missing_cell_fail(self):
        # 回归（对抗方 S1-5）
        for row, label in (("- [ ] 4. Reference standard", "unchecked box"),
                           ("| 5. Split unit | TBD |", "5. Split unit"),
                           ("| 6. External test |", "6. External test")):
            with self.subTest(row=row):
                self.write(checklist=CHECKLIST + row + "\n")
                code, out = self.run_gate()
>               self.assertEqual(code, 1, out)
E               AssertionError: 0 != 1 : FAIL [checklist-undisposed] checklist_claim.md:7: unchecked box: - [ ] 4. Reference standard
E               check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:233: AssertionError
_____________ CheckPaperTest.test_citekey_without_bib_entry_fails ______________

self = <test_check_paper.CheckPaperTest testMethod=test_citekey_without_bib_entry_fails>

    def test_citekey_without_bib_entry_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("[@smith2024model]", "[@smith2024model; @ghost2025]"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [citation-without-entry] paper_draft.md:6: ghost2025 has no entry in references.bib
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:167: AssertionError
____ CheckPaperTest.test_disclosure_flag_does_not_excuse_other_placeholders ____

self = <test_check_paper.CheckPaperTest testMethod=test_disclosure_flag_does_not_excuse_other_placeholders>

    def test_disclosure_flag_does_not_excuse_other_placeholders(self):
        # 回归（对抗方 S1-3）：--allow-disclosed-flags 只降级 [PENDING…]/[UNVERIFIED…]
        self.write(draft=CLEAN_DRAFT.replace("doi:10.1148/radiol.2024.0001", "doi:10.xxxx/abc"))
        code, out = self.run_gate("--allow-disclosed-flags")
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [placeholder] paper_draft.md:20: '10.xxxx' in: Smith J. Model. Radiology. 2024;310(2):1-12. Reported kappa 0.62 and 87.5% agree
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:208: AssertionError
________________ CheckPaperTest.test_fake_doi_placeholder_fails ________________

self = <test_check_paper.CheckPaperTest testMethod=test_fake_doi_placeholder_fails>

    def test_fake_doi_placeholder_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("doi:10.1148/radiol.2024.0001", "doi:10.xxxx/abc"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [placeholder] paper_draft.md:20: '10.xxxx' in: Smith J. Model. Radiology. 2024;310(2):1-12. Reported kappa 0.62 and 87.5% agree
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:192: AssertionError
__________ CheckPaperTest.test_missing_checklist_fails_unless_skipped __________

self = <test_check_paper.CheckPaperTest testMethod=test_missing_checklist_fails_unless_skipped>

    def test_missing_checklist_fails_unless_skipped(self):
        (self.dir / "checklist_claim.md").unlink()
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [checklist-missing] /tmp/autopilot-run.B1W1mJ/mutant-tmp/tmpn49lrt9w: no checklist_*.md next to the draft (REPORTING_CHECKLISTS step 4)
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:239: AssertionError
___________ CheckPaperTest.test_numbers_in_chinese_prose_are_checked ___________

self = <test_check_paper.CheckPaperTest testMethod=test_numbers_in_chinese_prose_are_checked>

    def test_numbers_in_chinese_prose_are_checked(self):
        # 回归（对抗方 S1-1）：\w 含汉字，旧边界让紧贴汉字的数字整句漏检
        draft = CLEAN_DRAFT.replace("## References", "外部验证AUC为0.912。\n\n## References")
        self.write(draft=draft)
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:18: '0.912' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:136: AssertionError
___________ CheckPaperTest.test_pending_flag_fails_unless_disclosed ____________

self = <test_check_paper.CheckPaperTest testMethod=test_pending_flag_fails_unless_disclosed>

    def test_pending_flag_fails_unless_disclosed(self):
        self.write(draft=CLEAN_DRAFT + "\nExternal AUC [PENDING: user to supply].\n")
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [placeholder] paper_draft.md:22: '[PENDING' in: External AUC [PENDING: user to supply].
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:198: AssertionError
_________ CheckPaperTest.test_references_section_numbers_are_excluded __________

self = <test_check_paper.CheckPaperTest testMethod=test_references_section_numbers_are_excluded>

    def test_references_section_numbers_are_excluded(self):
        # 回归（对抗方 S1-6）：文献表里的 0.62 / 87.5% 不是本文结果；把它挪进正文就必须失败
        code, out = self.run_gate()
        self.assertEqual(code, 0, out)
        self.write(draft=CLEAN_DRAFT.replace("## References\n", "Reported kappa 0.62.\n\n## References\n"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:18: '0.62' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:159: AssertionError
___________ CheckPaperTest.test_untraced_decimal_fails_and_is_named ____________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_decimal_fails_and_is_named>

    def test_untraced_decimal_fails_and_is_named(self):
        self.write(draft=CLEAN_DRAFT.replace("Sensitivity was 91.5%", "Specificity was 0.912"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:16: '0.912' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:106: AssertionError
________________ CheckPaperTest.test_untraced_percentage_fails _________________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_percentage_fails>

    def test_untraced_percentage_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("91.5%", "93.0%"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:16: '93.0%' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:112: AssertionError
________________ CheckPaperTest.test_untraced_sample_size_fails ________________

self = <test_check_paper.CheckPaperTest testMethod=test_untraced_sample_size_fails>

    def test_untraced_sample_size_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("(n=412)", "(n=1,204)"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : FAIL [number-not-in-ledger] paper_draft.md:5: 'n=1,204' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:118: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_ai_tell_fails - Assert...
FAILED tests/test_check_paper.py::CheckPaperTest::test_bib_entry_never_cited_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_bracketed_confidence_interval_is_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_checklist_row_without_disposition_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_checklist_unchecked_box_tbd_and_missing_cell_fail
FAILED tests/test_check_paper.py::CheckPaperTest::test_citekey_without_bib_entry_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_disclosure_flag_does_not_excuse_other_placeholders
FAILED tests/test_check_paper.py::CheckPaperTest::test_fake_doi_placeholder_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_missing_checklist_fails_unless_skipped
FAILED tests/test_check_paper.py::CheckPaperTest::test_numbers_in_chinese_prose_are_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_pending_flag_fails_unless_disclosed
FAILED tests/test_check_paper.py::CheckPaperTest::test_references_section_numbers_are_excluded
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_decimal_fails_and_is_named
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_percentage_fails
FAILED tests/test_check_paper.py::CheckPaperTest::test_untraced_sample_size_fails
15 failed, 16 passed in 0.18s

```
- finished: 2026-10-24T15:09:21Z
- result: KILLED
