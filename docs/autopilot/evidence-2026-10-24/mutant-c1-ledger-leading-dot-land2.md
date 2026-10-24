# Mutant — mutant-c1-ledger-leading-dot-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:25:02Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: f06daa3db81d3be343ef6e573c4bc5f80ce2157351b52697aadcebee218416cf
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_in_the_ledger_matches_the_draft\b; expected exit: 1
- mutated files: research-paper/scripts/integrity_gate.py
- patch sha256: 6e3e524d830ae7f0786ab7fa451bdaf6ee67c86f582df376e0ec409f1ca8f867

```diff
diff --git a/research-paper/scripts/integrity_gate.py b/research-paper/scripts/integrity_gate.py
index 5a48db2..2670e59 100644
--- a/research-paper/scripts/integrity_gate.py
+++ b/research-paper/scripts/integrity_gate.py
@@ -230,7 +230,7 @@ _STRIP_INLINE = (
     re.compile(r"`[^`]*`"),
 )
 #: 文献表/账本里的数字：千分位 1,204 是一个数，不是 1 和 204
-NUMBER_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d*\.\d+|\d+")  # 台账里的 `.85` 与正文同样读作 0.85
+NUMBER_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")  # 台账里的 `.85` 与正文同样读作 0.85


 def normalize_number(raw: str) -> str:

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
36 passed in 0.18s

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
............F.......................                                     [100%]
=================================== FAILURES ===================================
_______ CheckPaperTest.test_leading_dot_in_the_ledger_matches_the_draft ________

self = <test_check_paper.CheckPaperTest testMethod=test_leading_dot_in_the_ledger_matches_the_draft>

    def test_leading_dot_in_the_ledger_matches_the_draft(self):
        ledger = LEDGER.rstrip("\n") + "\nC9,results,corr,.85,,p < .001,a.csv,row 9,verified\n"
        draft = CLEAN_DRAFT.replace("## References", "Agreement r = .85 (p < .001).\n\n## References")
        self.write(draft=draft, ledger=ledger)
        code, out = self.run_gate()
>       self.assertEqual(code, 0, out)
E       AssertionError: 1 != 0 : FAIL [number-not-in-ledger] paper_draft.md:18: '.85' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       FAIL [number-not-in-ledger] paper_draft.md:18: '.001' is not covered by any results_ledger.csv value — trace it or flag it [PENDING: …]
E       check_paper: FAIL (2 finding(s), 0 warning(s))

tests/test_check_paper.py:171: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_leading_dot_in_the_ledger_matches_the_draft
1 failed, 35 passed in 0.14s

```
- finished: 2026-10-24T16:25:07Z
- result: KILLED
