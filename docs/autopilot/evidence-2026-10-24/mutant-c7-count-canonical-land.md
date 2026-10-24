# Mutant — mutant-c7-count-canonical-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:52:32Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 7cf8895c8dbdff465300ddc4341700b4b6cb6265ab009538fbae3f7ded243a8c
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
- failure signature: ^FAILED tests/test_import_litsearch\.py::ImportLitsearchTest::test_import_copies_files_and_appends_one_matching_row\b; expected exit: 1
- mutated files: medical-imaging-review/scripts/import_litsearch.py
- patch sha256: 386d820f211d19113e591f68448b7e7b1a17c4e55c3b6c1de051a26bbf33230e

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..c308600 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -141,7 +141,7 @@ def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date:
         "search_date": search_date or date.today().isoformat(),
         "strategy_file": f"{relative}/topic.yaml",
         "filters": "frozen lit-search protocol (concept blocks, window, languages) in topic.yaml",
-        "result_count": str(identified),
+        "result_count": str(canonical),
         "export_file": f"{relative}/dois.md",
         "searcher_id": searcher_id,
         "notes": (f"imported by import_litsearch.py; PRISMA identified {identified:,}"

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
139 passed in 1.76s

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
.......................................F......F....................      [100%]
=================================== FAILURES ===================================
__ ImportLitsearchTest.test_import_copies_files_and_appends_one_matching_row ___

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_import_copies_files_and_appends_one_matching_row>

    def test_import_copies_files_and_appends_one_matching_row(self):
        before = len(self.rows())
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
        self.assertEqual(sorted(p.name for p in target.iterdir()),
                         ["PRISMA.md", "dois.md", "references.md", "topic.yaml"])
        self.assertEqual((target / "PRISMA.md").read_text(encoding="utf-8"), PRISMA)
        rows = self.rows()
        self.assertEqual(len(rows), before + 1)
        row = rows[-1]
>       self.assertEqual(row["result_count"], "1234")
E       AssertionError: '1000' != '1234'
E       - 1000
E       + 1234

tests/test_import_litsearch.py:104: AssertionError
_________ ImportLitsearchTest.test_the_audit_accepts_the_imported_row __________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_the_audit_accepts_the_imported_row>

    def test_the_audit_accepts_the_imported_row(self):
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        problems, valid, total, error = validate_search_log(self.project)
        self.assertIsNone(error)
        self.assertEqual(problems, [])
>       self.assertEqual((valid, total), (1, 1234))
E       AssertionError: Tuples differ: (1, 1000) != (1, 1234)
E
E       First differing element 1:
E       1000
E       1234
E
E       - (1, 1000)
E       + (1, 1234)

tests/test_import_litsearch.py:117: AssertionError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_import_copies_files_and_appends_one_matching_row
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_the_audit_accepts_the_imported_row
2 failed, 137 passed in 1.74s

```
- finished: 2026-10-24T15:52:39Z
- result: KILLED
