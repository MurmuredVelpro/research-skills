# Mutant — mutant-c1-leading-dot-norm-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:54:55Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 774a8d16e8bb16c2623e9f3c9cee35aa6b8888fdf0d8f47193b7a5f5060f47ee
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_matches_the_ledger_and_versions_are_not_numbers\b; expected exit: 1
- mutated files: research-paper/scripts/integrity_gate.py
- patch sha256: 61bb3425889b1654f27a523a86095332f89f675a01cdaa666212e31dff69abf5

```diff
diff --git a/research-paper/scripts/integrity_gate.py b/research-paper/scripts/integrity_gate.py
index 47cfbe6..9d7aafa 100644
--- a/research-paper/scripts/integrity_gate.py
+++ b/research-paper/scripts/integrity_gate.py
@@ -235,8 +235,6 @@ NUMBER_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")

 def normalize_number(raw: str) -> str:
     value = raw.replace(",", "")
-    if value.startswith("."):
-        value = "0" + value
     if "." in value:
         value = value.rstrip("0").rstrip(".") or "0"
     return value

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
...........F......................                                       [100%]
=================================== FAILURES ===================================
_ CheckPaperTest.test_leading_dot_matches_the_ledger_and_versions_are_not_numbers _

self = <test_check_paper.CheckPaperTest testMethod=test_leading_dot_matches_the_ledger_and_versions_are_not_numbers>

    def test_leading_dot_matches_the_ledger_and_versions_are_not_numbers(self):
        ledger = LEDGER.rstrip("\n") + "\nC9,results,corr,0.85,,,a.csv,row 9,verified\n"
        draft = CLEAN_DRAFT.replace("## References", "Agreement r = .85 with tool 2.0.1.\n\n## References")
        self.write(draft=draft, ledger=ledger)
        code, out = self.run_gate()
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [number-not-in-ledger] paper_draft.md:18: '.85' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (1 finding(s), 0 warning(s))

tests/test_check_paper.py:131: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_matches_the_ledger_and_versions_are_not_numbers
1 failed, 33 passed in 0.12s

```
- finished: 2026-10-24T15:54:59Z
- result: KILLED
