# Mutant — mutant-c7-refactor-accumulate-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:53:26Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: ec0a0dc684a0296314d6bab5bd2ab31dc097fe1e5b12294917d3bdcb6837cf6a
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
- mutated files: medical-imaging-review/scripts/mir_audit/checks_artifacts.py
- patch sha256: ba1f4d9628b67b97aa82bf17696da4c846f3e870ac9b363e4fee7ca24b1f56be

```diff
diff --git a/medical-imaging-review/scripts/mir_audit/checks_artifacts.py b/medical-imaging-review/scripts/mir_audit/checks_artifacts.py
index aab28f3..e7e9f61 100644
--- a/medical-imaging-review/scripts/mir_audit/checks_artifacts.py
+++ b/medical-imaging-review/scripts/mir_audit/checks_artifacts.py
@@ -64,7 +64,7 @@ def validate_search_log(project_dir: Path) -> tuple[list[str], int, int, str | N
             problems.append(f"search/search_log.csv row {index} has no immutable source export")
             continue
         valid_searches += 1
-        total_search_results += result_count
+        total_search_results += 1
     if valid_searches == 0:
         problems.append(
             "search/search_log.csv must contain at least one reproducible executed-search row"

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
139 passed in 1.71s

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
.......................................F...............F.F.........F.... [ 51%]
.....F........................................F....................      [100%]
=================================== FAILURES ===================================
__ ProjectGateTests.test_complete_human_gate_requires_strict_template_values ___

self = <test_audit_manuscript.ProjectGateTests testMethod=test_complete_human_gate_requires_strict_template_values>

    def test_complete_human_gate_requires_strict_template_values(self):
        gate = self.complete_gate()
        self.make_systematic(gate)
>       self.assertEqual([], audit.scan_project_readiness("systematic", self.project))
E       AssertionError: Lists differ: [] != [Finding(severity='critical', category='no[177 chars]rue)]
E
E       Second list contains 1 additional elements.
E       First extra element 0:
E       Finding(severity='critical', category='not_ready', line=0, message='Systematic project artifacts are incomplete: sum of search_log result_count values does not match flow_counts identified', excerpt='', gate_relevant=True)
E
E       - []
E       + [Finding(severity='critical',
E       +          category='not_ready',
E       +          line=0,
E       +          message='Systematic project artifacts are incomplete: sum of '
E       +                  'search_log result_count values does not match flow_counts '
E       +                  'identified',
E       +          excerpt='',
E       +          gate_relevant=True)]

tests/test_audit_manuscript.py:911: AssertionError
__ ProjectGateTests.test_nested_shadow_route_cannot_override_top_level_route ___

self = <test_audit_manuscript.ProjectGateTests testMethod=test_nested_shadow_route_cannot_override_top_level_route>

    def test_nested_shadow_route_cannot_override_top_level_route(self):
        self.make_scoping(populated=True)
        config = self.config_text("scoping")
        config = "shadow:\n  route: systematic\n" + config
        self.write("review_config.yaml", config)
>       self.assertEqual([], audit.scan_project_readiness("scoping", self.project))
E       AssertionError: Lists differ: [] != [Finding(severity='critical', category='no[174 chars]rue)]
E
E       Second list contains 1 additional elements.
E       First extra element 0:
E       Finding(severity='critical', category='not_ready', line=0, message='Scoping project artifacts are incomplete: sum of search_log result_count values does not match flow_counts identified', excerpt='', gate_relevant=True)
E
E       - []
E       + [Finding(severity='critical',
E       +          category='not_ready',
E       +          line=0,
E       +          message='Scoping project artifacts are incomplete: sum of search_log '
E       +                  'result_count values does not match flow_counts identified',
E       +          excerpt='',
E       +          gate_relevant=True)]

tests/test_audit_manuscript.py:1509: AssertionError
_____ ProjectGateTests.test_populated_scoping_artifacts_are_machine_ready ______

self = <test_audit_manuscript.ProjectGateTests testMethod=test_populated_scoping_artifacts_are_machine_ready>

    def test_populated_scoping_artifacts_are_machine_ready(self):
        self.make_scoping(populated=True)
>       self.assertEqual([], audit.scan_project_readiness("scoping", self.project))
E       AssertionError: Lists differ: [] != [Finding(severity='critical', category='no[174 chars]rue)]
E
E       Second list contains 1 additional elements.
E       First extra element 0:
E       Finding(severity='critical', category='not_ready', line=0, message='Scoping project artifacts are incomplete: sum of search_log result_count values does not match flow_counts identified', excerpt='', gate_relevant=True)
E
E       - []
E       + [Finding(severity='critical',
E       +          category='not_ready',
E       +          line=0,
E       +          message='Scoping project artifacts are incomplete: sum of search_log '
E       +                  'result_count values does not match flow_counts identified',
E       +          excerpt='',
E       +          gate_relevant=True)]

tests/test_audit_manuscript.py:870: AssertionError
_____ ProjectGateTests.test_scoping_positive_example_reaches_not_assessed ______

self = <test_audit_manuscript.ProjectGateTests testMethod=test_scoping_positive_example_reaches_not_assessed>

    def test_scoping_positive_example_reaches_not_assessed(self):
        self.make_scoping(populated=True)
        result = audit.audit_text(
            project_manuscript(SCOPING_ZH),
            file_label="scoping.md",
            requested_route="scoping",
            project_dir=self.project,
        )
>       self.assertEqual("not_assessed", result["gate_status"])
E       AssertionError: 'not_assessed' != 'fail'
E       - not_assessed
E       + fail

tests/test_audit_manuscript.py:880: AssertionError
____ ProjectGateTests.test_systematic_positive_example_reaches_not_assessed ____

self = <test_audit_manuscript.ProjectGateTests testMethod=test_systematic_positive_example_reaches_not_assessed>

    def test_systematic_positive_example_reaches_not_assessed(self):
        self.make_systematic(self.complete_gate())
        result = audit.audit_text(
            project_manuscript(SYSTEMATIC),
            file_label="systematic.md",
            requested_route="systematic",
            project_dir=self.project,
        )
>       self.assertEqual("not_assessed", result["gate_status"])
E       AssertionError: 'not_assessed' != 'fail'
E       - not_assessed
E       + fail

tests/test_audit_manuscript.py:893: AssertionError
_________ ImportLitsearchTest.test_the_audit_accepts_the_imported_row __________

self = <test_import_litsearch.ImportLitsearchTest testMethod=test_the_audit_accepts_the_imported_row>

    def test_the_audit_accepts_the_imported_row(self):
        code, out = self.run_import()
        self.assertEqual(code, 0, out)
        problems, valid, total, error = validate_search_log(self.project)
        self.assertIsNone(error)
        self.assertEqual(problems, [])
>       self.assertEqual((valid, total), (1, 1234))
E       AssertionError: Tuples differ: (1, 1) != (1, 1234)
E
E       First differing element 1:
E       1
E       1234
E
E       - (1, 1)
E       + (1, 1234)
E       ?      +++

tests/test_import_litsearch.py:117: AssertionError
=========================== short test summary info ============================
FAILED tests/test_audit_manuscript.py::ProjectGateTests::test_complete_human_gate_requires_strict_template_values
FAILED tests/test_audit_manuscript.py::ProjectGateTests::test_nested_shadow_route_cannot_override_top_level_route
FAILED tests/test_audit_manuscript.py::ProjectGateTests::test_populated_scoping_artifacts_are_machine_ready
FAILED tests/test_audit_manuscript.py::ProjectGateTests::test_scoping_positive_example_reaches_not_assessed
FAILED tests/test_audit_manuscript.py::ProjectGateTests::test_systematic_positive_example_reaches_not_assessed
FAILED tests/test_import_litsearch.py::ImportLitsearchTest::test_the_audit_accepts_the_imported_row
6 failed, 133 passed in 2.09s

```
- finished: 2026-10-24T15:53:34Z
- result: KILLED
