# Mutant — mutant-c7-write-before-refusal-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:57:18Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: e7a4a6be0c9b859743c937cb4a50a4fbde5c1655a7f8f0ae65e81cb66eedf6a7
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
- failure signature: ^FAILED tests/test_import_litsearch\.py::ImportLitsearchTest::test_missing_prisma_total_is_refused_and_writes_nothing\b; expected exit: 1
- mutated files: medical-imaging-review/scripts/import_litsearch.py
- patch sha256: 2b0cf21349a3cf15c65bfec89b9aa853f53f7f8da9c2202e9f680d6136c475dc

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..a3939b0 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -123,6 +123,7 @@ def import_run(project_dir: Path, run_dir: Path, searcher_id: str, search_date:
     missing = [name for name in REQUIRED if not (run_dir / name).is_file()]
     if missing:
         raise ImportRefused(f"{run_dir} lacks {', '.join(missing)} — run `lit report` / `lit deliver` first")
+    (project_dir / "search/exports/junk").mkdir(parents=True, exist_ok=True)
     identified, canonical = read_identified(run_dir / "PRISMA.md")
     run_id = read_run_id(run_dir)
     coverage = read_window(run_dir / "topic.yaml")

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
139 passed in 1.86s

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
....................................FFF..F.....FF..................      [100%]
=================================== FAILURES ===================================
_______ ImportLitsearchTest.test_empty_preexisting_export_dir_is_refused _______

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_empty_preexisting_export_dir_is_refused>

    def test_empty_preexisting_export_dir_is_refused(self):
        (self.project / "search/exports" / f"litsearch-{RUN_ID}").mkdir(parents=True)
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("already exists", out)
>       self.assertEqual(self.snapshot(), before)
E       AssertionError: {'rev[12934 chars]orts/junk': None, 'search/exports/litsearch-20[17 chars]None} != {'rev[12934 chars]orts/litsearch-20261020T101500Z': None}
E       Diff is 20395 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:221: AssertionError
_______ ImportLitsearchTest.test_failed_log_append_rolls_back_the_export _______

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_failed_log_append_rolls_back_the_export>

    def test_failed_log_append_rolls_back_the_export(self):
        log = self.project / "search/search_log.csv"
        log.chmod(0o444)
        before = self.snapshot()
        try:
            code, out = self.run_import()
        finally:
            log.chmod(0o644)
        self.assertEqual(code, 2, out)
>       self.assertEqual(self.snapshot(), before)
E       AssertionError: {'rev[12888 chars]: null,\n  "included": null\n}\n', 'search/exports/junk': None} != {'rev[12888 chars]: null,\n  "included": null\n}\n'}
E       Diff is 20341 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:197: AssertionError
_ ImportLitsearchTest.test_foreign_search_log_header_is_refused_before_writing _

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_foreign_search_log_header_is_refused_before_writing>

    def test_foreign_search_log_header_is_refused_before_writing(self):
        log = self.project / "search/search_log.csv"
        log.write_text("database,date,hits\n", encoding="utf-8")
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("header", out)
>       self.assertEqual(self.snapshot(), before)
E       AssertionError: {'rev[12805 chars]: null,\n  "included": null\n}\n', 'search/exports/junk': None} != {'rev[12805 chars]: null,\n  "included": null\n}\n'}
E       Diff is 20194 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:186: AssertionError
_ ImportLitsearchTest.test_missing_prisma_total_is_refused_and_writes_nothing __

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_missing_prisma_total_is_refused_and_writes_nothing>

    def test_missing_prisma_total_is_refused_and_writes_nothing(self):
        (self.run / "PRISMA.md").write_text(PRISMA.replace("合计识别：**1,234** 条", ""), encoding="utf-8")
        before = self.snapshot()
        code, out = self.run_import()
        self.assertEqual(code, 2, out)
        self.assertIn("total-identified", out)
>       self.assertEqual(self.snapshot(), before)
E       AssertionError: {'rev[12888 chars]: null,\n  "included": null\n}\n', 'search/exports/junk': None} != {'rev[12888 chars]: null,\n  "included": null\n}\n'}
E       Diff is 20341 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:139: AssertionError
_________ ImportLitsearchTest.test_unparseable_prisma_total_is_refused _________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_unparseable_prisma_total_is_refused>

    def test_unparseable_prisma_total_is_refused(self):
        for bad in ("合计识别：**N/A** 条", "合计识别：**,** 条"):
            with self.subTest(bad=bad):
                (self.run / "PRISMA.md").write_text(PRISMA.replace("合计识别：**1,234** 条", bad), encoding="utf-8")
                before = self.snapshot()
                code, out = self.run_import()
                self.assertEqual(code, 2, out)
>               self.assertEqual(self.snapshot(), before)
E               AssertionError: {'rev[12888 chars]: null,\n  "included": null\n}\n', 'search/exports/junk': None} != {'rev[12888 chars]: null,\n  "included": null\n}\n'}
E               Diff is 20341 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:159: AssertionError
______________ ImportLitsearchTest.test_unsafe_run_id_is_refused _______________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_unsafe_run_id_is_refused>

    def test_unsafe_run_id_is_refused(self):
        for run_id in ("../escape", "20261020\n", ".hidden"):
            with self.subTest(run_id=run_id):
                (self.run / "manifest.json").write_text(json.dumps({"run_id": run_id}), encoding="utf-8")
                before = self.snapshot()
                code, out = self.run_import()
                self.assertEqual(code, 2, out)
                self.assertIn("safe directory name", out)
>               self.assertEqual(self.snapshot(), before)
E               AssertionError: {'rev[12888 chars]: null,\n  "included": null\n}\n', 'search/exports/junk': None} != {'rev[12888 chars]: null,\n  "included": null\n}\n'}
E               Diff is 20341 characters long. Set self.maxDiff to None to see it.

tests/test_import_litsearch.py:177: AssertionError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_empty_preexisting_export_dir_is_refused
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_failed_log_append_rolls_back_the_export
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_foreign_search_log_header_is_refused_before_writing
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_missing_prisma_total_is_refused_and_writes_nothing
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_unparseable_prisma_total_is_refused
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_unsafe_run_id_is_refused
6 failed, 133 passed in 1.91s

```
- finished: 2026-10-24T15:57:26Z
- result: KILLED
