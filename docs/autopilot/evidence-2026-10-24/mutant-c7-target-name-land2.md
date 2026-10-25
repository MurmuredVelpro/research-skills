# Mutant — mutant-c7-target-name-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:24:16Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 5046d17a2e6602337eb59941e13092c1f5649fa028ea912de3f1d950d4e05a54
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
- patch sha256: 6357d737f88fe72b9c991b256a4aa4f3dc6f6aa2e349620d112bf30bba915bfd

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..de0c2a1 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -130,7 +130,7 @@ def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date:
     log_before = read_log(log)

     exports = project_dir / "search" / "exports"
-    target = exports / f"litsearch-{run_id}"
+    target = exports / f"{run_id}"
     if target.exists() or target.is_symlink():
         raise ImportRefused(f"{target.relative_to(project_dir)} already exists — an import is never redone in place")
     relative = target.relative_to(project_dir).as_posix()

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
....................................................................     [100%]
140 passed in 1.77s

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
....................................FF..FF...F......................     [100%]
=================================== FAILURES ===================================
___ ImportLitsearchTest.test_dangling_symlink_at_the_export_path_is_refused ____

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_dangling_symlink_at_the_export_path_is_refused>

    def test_dangling_symlink_at_the_export_path_is_refused(self):
        exports = self.project / "search/exports"
        exports.mkdir(parents=True, exist_ok=True)
        link = exports / f"litsearch-{RUN_ID}"
        link.symlink_to(self.project / "nowhere")
        before = self.snapshot()
        try:
            code, out = self.run_import()
            after = self.snapshot()
        finally:
            link.unlink(missing_ok=True)  # tearDown 的 chmod 会跟随悬空链接而报错
            if link.is_dir():
                IMPORT.remove_export(link)
>       self.assertEqual(code, 2, out)
E       AssertionError: 0 != 2 : Imported lit-search run into /tmp/autopilot-run.88DG8N/mutant-tmp/tmpywkfkw7o/review_project/ccta-review-20260723-120000-1234abcd/search/exports/20261020T101500Z
E       Next: screening/deduplication stay with the named human reviewers; flow_counts identified must equal the summed search_log result_count.

tests/test_import_litsearch.py:236: AssertionError
_______ ImportLitsearchTest.test_empty_preexisting_export_dir_is_refused _______

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_empty_preexisting_export_dir_is_refused>

    def test_empty_preexisting_export_dir_is_refused(self):
        (self.project / "search/exports" / f"litsearch-{RUN_ID}").mkdir(parents=True)
        before = self.snapshot()
        code, out = self.run_import()
>       self.assertEqual(code, 2, out)
E       AssertionError: 0 != 2 : Imported lit-search run into /tmp/autopilot-run.88DG8N/mutant-tmp/tmpv9yxm3xf/review_project/ccta-review-20260723-120000-1234abcd/search/exports/20261020T101500Z
E       Next: screening/deduplication stay with the named human reviewers; flow_counts identified must equal the summed search_log result_count.

tests/test_import_litsearch.py:219: AssertionError
__ ImportLitsearchTest.test_import_copies_files_and_appends_one_matching_row ___

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_import_copies_files_and_appends_one_matching_row>

    def test_import_copies_files_and_appends_one_matching_row(self):
        before = len(self.rows())
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
>       self.assertEqual(sorted(p.name for p in target.iterdir()),
                         ["PRISMA.md", "dois.md", "references.md", "topic.yaml"])

tests/test_import_litsearch.py:98:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_import_litsearch.py:98: in <genexpr>
    self.assertEqual(sorted(p.name for p in target.iterdir()),
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = PosixPath('/tmp/autopilot-run.88DG8N/mutant-tmp/tmplr0w7n4l/review_project/ccta-review-20260723-120000-1234abcd/search/exports/litsearch-20261020T101500Z')

    def iterdir(self):
        """Yield path objects of the directory contents.

        The children are yielded in arbitrary order, and the
        special entries '.' and '..' are not included.
        """
>       for name in os.listdir(self):
E       FileNotFoundError: [Errno 2] No such file or directory: '/tmp/autopilot-run.88DG8N/mutant-tmp/tmplr0w7n4l/review_project/ccta-review-20260723-120000-1234abcd/search/exports/litsearch-20261020T101500Z'

/usr/lib/python3.12/pathlib.py:1058: FileNotFoundError
____________ ImportLitsearchTest.test_imported_files_are_read_only _____________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_imported_files_are_read_only>

    def test_imported_files_are_read_only(self):
        self.run_import()
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
>       for path in target.iterdir():

tests/test_import_litsearch.py:122:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = PosixPath('/tmp/autopilot-run.88DG8N/mutant-tmp/tmpwr3gu55j/review_project/ccta-review-20260723-120000-1234abcd/search/exports/litsearch-20261020T101500Z')

    def iterdir(self):
        """Yield path objects of the directory contents.

        The children are yielded in arbitrary order, and the
        special entries '.' and '..' are not included.
        """
>       for name in os.listdir(self):
E       FileNotFoundError: [Errno 2] No such file or directory: '/tmp/autopilot-run.88DG8N/mutant-tmp/tmpwr3gu55j/review_project/ccta-review-20260723-120000-1234abcd/search/exports/litsearch-20261020T101500Z'

/usr/lib/python3.12/pathlib.py:1058: FileNotFoundError
_________ ImportLitsearchTest.test_optional_delivery_files_are_copied __________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_optional_delivery_files_are_copied>

    def test_optional_delivery_files_are_copied(self):
        (self.run / "coverage_report.md").write_text("# coverage\n", encoding="utf-8")
        (self.run / "references.bib").write_text("@article{a,}\n", encoding="utf-8")
        self.assertEqual(self.run_import()[0], 0)
        target = self.project / "search/exports" / f"litsearch-{RUN_ID}"
>       self.assertTrue((target / "coverage_report.md").is_file())
E       AssertionError: False is not true

tests/test_import_litsearch.py:166: AssertionError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_dangling_symlink_at_the_export_path_is_refused
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_empty_preexisting_export_dir_is_refused
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_import_copies_files_and_appends_one_matching_row
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_imported_files_are_read_only
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_optional_delivery_files_are_copied
5 failed, 135 passed in 1.91s

```
- finished: 2026-10-24T16:24:24Z
- result: KILLED
