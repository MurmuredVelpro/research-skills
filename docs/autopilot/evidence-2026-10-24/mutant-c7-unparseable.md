# Mutant — mutant-c7-unparseable

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:20:21Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 8dc98eb54e05b63b26c519c582de421d3e9075326245332ec0826cd2aeefb332
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
- failure signature: ^FAILED tests/test_import_litsearch\.py::ImportLitsearchTest::test_unparseable_prisma_total_is_refused\b; expected exit: 1
- mutated files: medical-imaging-review/scripts/import_litsearch.py
- patch sha256: 3ed17a89f18017f737f21adebf1368574e5843c5e2508ed07caf84ec81b31bd5

```diff
diff --git a/medical-imaging-review/scripts/import_litsearch.py b/medical-imaging-review/scripts/import_litsearch.py
index 3be495e..d53ff9e 100644
--- a/medical-imaging-review/scripts/import_litsearch.py
+++ b/medical-imaging-review/scripts/import_litsearch.py
@@ -44,7 +44,7 @@ from mir_audit.constants import SEARCH_LOG_COLUMNS  # noqa: E402
 REQUIRED = ("dois.md", "PRISMA.md", "topic.yaml")
 OPTIONAL = ("references.md", "coverage_report.md", "references.bib")
 #: lit-search 的 PRISMA.md 渲染行：「合计识别：**1,234** 条」（report.py prisma_markdown）
-IDENTIFIED_RE = re.compile(r"合计识别：\*\*(\d[\d,]*)\*\*")
+IDENTIFIED_RE = re.compile(r"合计识别：\*\*([^*]+)\*\*")
 CANONICAL_RE = re.compile(r"去重后规范记录：\*\*(\d[\d,]*)\*\*")
 SAFE_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

@@ -207,7 +207,7 @@ def main(argv: list[str] | None = None) -> int:
         return 2
     try:
         target = import_run(args.project_dir, args.run_dir, args.searcher_id.strip(), args.search_date)
-    except (ImportRefused, OSError, UnicodeDecodeError, ValueError) as error:
+    except (ImportRefused, OSError, UnicodeDecodeError) as error:
         print(f"ERROR: {error}", file=sys.stderr)
         return 2
     problems, _valid, _total, _error = validate_search_log(args.project_dir)

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
137 passed in 1.94s

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
..............................................F..................        [100%]
=================================== FAILURES ===================================
_________ ImportLitsearchTest.test_unparseable_prisma_total_is_refused _________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_unparseable_prisma_total_is_refused>

    def test_unparseable_prisma_total_is_refused(self):
        for bad in ("合计识别：**N/A** 条", "合计识别：**,** 条"):
            with self.subTest(bad=bad):
                (self.run / "PRISMA.md").write_text(PRISMA.replace("合计识别：**1,234** 条", bad), encoding="utf-8")
                before = self.snapshot()
>               code, out = self.run_import()

tests/test_import_litsearch.py:156:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/test_import_litsearch.py:79: in run_import
    code = IMPORT.main(["--project-dir", str(self.project), "--run-dir", str(self.run),
scripts/import_litsearch.py:209: in main
    target = import_run(args.project_dir, args.run_dir, args.searcher_id.strip(), args.search_date)
scripts/import_litsearch.py:126: in import_run
    identified, canonical = read_identified(run_dir / "PRISMA.md")
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

prisma = PosixPath('/tmp/autopilot-run.fEOZFG/mutant-tmp/tmpauujq60k/runs/ccta/20261020T101500Z/PRISMA.md')

    def read_identified(prisma: Path) -> tuple[int, int | None]:
        text = prisma.read_text(encoding="utf-8")
        match = IDENTIFIED_RE.search(text)
        if not match:
            raise ImportRefused(
                f"{prisma.name} has no total-identified count ('合计识别：**N** 条') — "
                "re-run `lit report` so the PRISMA counts reconcile, then import"
            )
        canonical = CANONICAL_RE.search(text)
>       return (int(match.group(1).replace(",", "")),
                int(canonical.group(1).replace(",", "")) if canonical else None)
E       ValueError: invalid literal for int() with base 10: 'N/A'

scripts/import_litsearch.py:65: ValueError
=========================== short test summary info ============================
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_unparseable_prisma_total_is_refused
1 failed, 136 passed in 2.05s

```
- finished: 2026-10-24T15:20:30Z
- result: KILLED
