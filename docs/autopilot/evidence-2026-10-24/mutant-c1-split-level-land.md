# Mutant — mutant-c1-split-level-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:54:33Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 0d0a96a0274582c95c7cbde34adc47783d601b18db68339c8bc52c5050882c72
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_section_after_references_at_the_same_level_is_checked\b; expected exit: 1
- mutated files: research-paper/scripts/integrity_gate.py
- patch sha256: 17d251ed94d1303fa485feffc7767cf36325d9121ce8b1d9bff90abcb02ea193

```diff
diff --git a/research-paper/scripts/integrity_gate.py b/research-paper/scripts/integrity_gate.py
index 47cfbe6..f513467 100644
--- a/research-paper/scripts/integrity_gate.py
+++ b/research-paper/scripts/integrity_gate.py
@@ -70,7 +70,7 @@ def split_body(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]
         if REFERENCES_HEADING_RE.match(line.strip()):
             refs_level = heading_level(line)
             continue
-        if refs_level and HEADING_RE.match(line) and heading_level(line) <= refs_level:
+        if refs_level and HEADING_RE.match(line) and heading_level(line) < refs_level:
             # 「### 外文文献」这类子标题仍属参考文献节；同级或更高级的标题（附录等）才回到正文
             refs_level = 0
         (refs if refs_level else body).append((number, line))

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
..................................                                       [100%]
34 passed in 0.11s

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
...................F..............                                       [100%]
=================================== FAILURES ===================================
__ CheckPaperTest.test_section_after_references_at_the_same_level_is_checked ___

self = <test_check_paper.CheckPaperTest testMethod=test_section_after_references_at_the_same_level_is_checked>

    def test_section_after_references_at_the_same_level_is_checked(self):
        # landing review：与 References 同级的 `## Appendix` 结束文献表，里面的数字照样对账
        self.write(draft=CLEAN_DRAFT + "\n## Appendix\n\nExtra AUC 0.777.\n")
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_paper: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_paper.py:175: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_section_after_references_at_the_same_level_is_checked
1 failed, 33 passed in 0.13s

```
- finished: 2026-10-24T15:54:38Z
- result: KILLED
