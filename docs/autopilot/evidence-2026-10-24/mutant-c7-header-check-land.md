# Mutant — mutant-c7-header-check-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:54:11Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: fad634d3c277a8e335a42a13efbc264b22626cc318a9b2cabe5abe83ad1ce954
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
- failure signature: ^FAILED tests/test_import_litsearch\.py::ForeignHeaderRefusedUpFront::test_foreign_header_is_refused_by_the_precheck_not_by_rollback\b; expected exit: 1
- mutated files: medical-imaging-review/scripts/import_litsearch.py
- patch sha256: 312fac434586fa700a074e319adf320070ef18065cf024e01c760aa28baf78c4

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..6262a03 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -105,7 +105,7 @@ def read_log(log: Path) -> str:
         return ""
     text = log.read_text(encoding="utf-8")
     header = next(csv.reader(StringIO(text)), [])
-    if tuple(header) != SEARCH_LOG_COLUMNS:
+    if False:
         raise ImportRefused(f"{log.name} header is not the audit schema ({', '.join(SEARCH_LOG_COLUMNS)})")
     return text


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
cd medical-imaging-review && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
........................................................................ [ 51%]
...................................................................      [100%]
139 passed in 2.06s

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
cd medical-imaging-review && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```
........................................................................ [ 51%]
.....................................................F.............      [100%]
=================================== FAILURES ===================================
_ ForeignHeaderRefusedUpFront.test_foreign_header_is_refused_by_the_precheck_not_by_rollback _

self = <test_import_litsearch.ForeignHeaderRefusedUpFront testMethod=test_foreign_header_is_refused_by_the_precheck_not_by_rollback>

    def test_foreign_header_is_refused_by_the_precheck_not_by_rollback(self):
        (self.project / "search/search_log.csv").write_text("database,date,hits\n", encoding="utf-8")
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
>       self.assertIn("header is not the audit schema", out)
E       AssertionError: 'header is not the audit schema' not found in "ERROR: the audit rejects the imported search_log row: search_log.csv header must exactly match schema 2.0; expected ['source', 'platform', 'coverage', 'search_date', 'strategy_file', 'filters', 'result_count', 'export_file', 'searcher_id', 'notes'], found ['database', 'date', 'hits']\n"

tests/test_import_litsearch.py:297: AssertionError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ForeignHeaderRefusedUpFront::test_foreign_header_is_refused_by_the_precheck_not_by_rollback
1 failed, 138 passed in 1.76s

```
- finished: 2026-10-24T15:54:19Z
- result: KILLED
