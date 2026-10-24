# Mutant — mutant-c7-audit-accepts

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:21:04Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 6ab292edf3fff6a79d30cf923db0770bbb68a0275a3dd269a6c82260f259b28b
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
- failure signature: ^FAILED tests/test_import_litsearch\.py::ImportLitsearchTest::test_the_audit_accepts_the_imported_row\b; expected exit: 1
- mutated files: medical-imaging-review/scripts/import_litsearch.py
- patch sha256: 36766d6645ed4b66efa14fa9914c58fc2d0b0a7b58166a0fa231bfc5fd25bb51

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..1966398 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -143,7 +143,7 @@ def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date:
         "filters": "frozen lit-search protocol (concept blocks, window, languages) in topic.yaml",
         "result_count": str(identified),
         "export_file": f"{relative}/dois.md",
-        "searcher_id": searcher_id,
+        "searcher_id": "",
         "notes": (f"imported by import_litsearch.py; PRISMA identified {identified:,}"
                   + (f", after deduplication {canonical:,}" if canonical is not None else "")
                   + "; screening continues under this project's human gates"),
@@ -176,7 +176,7 @@ def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date:
         new_index = sum(1 for _ in csv.DictReader(StringIO(prefix + row))) + 1
         problems, _valid, _total, error = validate_search_log(project_dir)
         rejected = [p for p in problems if f"row {new_index} " in p] + ([error] if error else [])
-        if rejected:
+        if False:
             raise ImportRefused("the audit rejects the imported search_log row: " + "; ".join(rejected))
     except BaseException:
         # Export first: restoring the log can fail for the same reason the append did.

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
........................................................................ [ 52%]
.................................................................        [100%]
137 passed in 1.89s

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
........................................................................ [ 52%]
......................................F......F...................        [100%]
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
        self.assertEqual(row["result_count"], "1234")
        self.assertEqual(row["strategy_file"], f"search/exports/litsearch-{RUN_ID}/topic.yaml")
        self.assertEqual(row["export_file"], f"search/exports/litsearch-{RUN_ID}/dois.md")
        self.assertEqual(row["coverage"], "2021-01-01..2025-12-31")
>       self.assertEqual(row["searcher_id"], "reviewer-a")
E       AssertionError: '' != 'reviewer-a'
E       + reviewer-a

tests/test_import_litsearch.py:107: AssertionError
_________ ImportLitsearchTest.test_the_audit_accepts_the_imported_row __________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_the_audit_accepts_the_imported_row>

    def test_the_audit_accepts_the_imported_row(self):
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        problems, valid, total, error = validate_search_log(self.project)
        self.assertIsNone(error)
>       self.assertEqual(problems, [])
E       AssertionError: Lists differ: ['search/search_log.csv row 2 is incomplet[82 chars]row'] != []
E
E       First list contains 2 additional elements.
E       First extra element 0:
E       'search/search_log.csv row 2 is incomplete'
E
E       + []
E       - ['search/search_log.csv row 2 is incomplete',
E       -  'search/search_log.csv must contain at least one reproducible executed-search '
E       -  'row']

tests/test_import_litsearch.py:115: AssertionError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_import_copies_files_and_appends_one_matching_row
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_the_audit_accepts_the_imported_row
2 failed, 135 passed in 1.85s

```
- finished: 2026-10-24T15:21:12Z
- result: KILLED
