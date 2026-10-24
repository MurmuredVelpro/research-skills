# Mutant — mutant-c1a-cjk-boundary-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:05:09Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 31d51ba80830fa3ec7ed309aed0bcbcdaff49c674fef8c9ae2d5c589ef57b41b
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_numbers_in_chinese_prose_are_checked\b; expected exit: 1
- mutated files: research-paper/scripts/integrity_gate.py
- patch sha256: 54c5af27546bb5aaa9c341a018d58d993af5b97cac0d3ac97ddd962798f51d85

```diff
diff --git a/research-paper/scripts/integrity_gate.py b/research-paper/scripts/integrity_gate.py
index 5a48db2..f00d3c1 100644
--- a/research-paper/scripts/integrity_gate.py
+++ b/research-paper/scripts/integrity_gate.py
@@ -215,7 +215,7 @@ def reconcile(cited: dict[str, int], listed: dict[str, str], where: str, listing
 #: 小数与百分数后面可以紧跟单位（`12.5ms`、`2.5x`、`95%CI`），只排除再接数字的版本号
 #: `2.0.1`；APA 省略前导零的 `r = .85`、`p < .001` 同样计入；中文输入法的全角 `％`、`＝` 与半角同等对待。
 METRIC_RE = re.compile(
-    r"(?<![A-Za-z0-9_.])(?:[nN]\s*[=＝]\s*(\d[\d,]*)(?![A-Za-z0-9_])|(\d+(?:\.\d+)?)\s*[%％]"
+    r"(?<![\w.])(?:[nN]\s*[=＝]\s*(\d[\d,]*)(?![A-Za-z0-9_])|(\d+(?:\.\d+)?)\s*[%％]"
     r"|(\d*\.\d+)(?![0-9_]|\.\d))"
 )
 #: 只剥离「不是结果数字」的东西：旗标、引文、URL/DOI、行内代码。方括号里的置信区间

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
36 passed in 0.12s

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
...........F.....F..................                                     [100%]
=================================== FAILURES ===================================
_________ CheckPaperTest.test_fullwidth_percent_and_equals_are_checked _________

self = <test_check_paper.CheckPaperTest testMethod=test_fullwidth_percent_and_equals_are_checked>

    def test_fullwidth_percent_and_equals_are_checked(self):
        # landing review r2：中文输入法打出的 `96％`、`n＝120` 曾整个漏检
        for text, shown in (("准确率为96％", "96％"), ("样本量n＝120", "n＝120")):
            with self.subTest(text=text):
                self.write(draft=CLEAN_DRAFT.replace("## References", f"{text}。\n\n## References"))
                code, out = self.run_gate()
>               self.assertEqual(code, 1, out)
E               AssertionError: 0 != 1 : check_paper: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_paper.py:163: AssertionError
___________ CheckPaperTest.test_numbers_in_chinese_prose_are_checked ___________

self = <test_check_paper.CheckPaperTest testMethod=test_numbers_in_chinese_prose_are_checked>

    def test_numbers_in_chinese_prose_are_checked(self):
        # 回归（对抗方 S1-1）：\w 含汉字，旧边界让紧贴汉字的数字整句漏检
        draft = CLEAN_DRAFT.replace("## References", "外部验证AUC为0.912。\n\n## References")
        self.write(draft=draft)
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_paper: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_paper.py:154: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_fullwidth_percent_and_equals_are_checked
FAILED tests/test_check_paper.py::CheckPaperTest::test_numbers_in_chinese_prose_are_checked
2 failed, 34 passed in 0.14s

```
- finished: 2026-10-24T16:05:14Z
- result: KILLED
