# Mutant — mutant-c5-limits-guard

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:15:45Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: dc2fc7e24ac3c2f1244f7108717e63339cb8116b5597a12ae86e3a2081ddde5c
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
- failure signature: ^\s*not ok \d+ - defense:\ no\ limitations\ /\ future\-work\ slide\ is\ a\ P2$; expected exit: 1
- mutated files: scholar-slides/scripts/lib/qa.mjs
- patch sha256: d80b95a8ff477426b17479efd0c1b28bfb0d0302c7592549a9ccf796db2e9f1d

```diff
diff --git a/scholar-slides/scripts/lib/qa.mjs b/scholar-slides/scripts/lib/qa.mjs
index 8772ef8..9ad5167 100644
--- a/scholar-slides/scripts/lib/qa.mjs
+++ b/scholar-slides/scripts/lib/qa.mjs
@@ -197,7 +197,7 @@ export function deckTypeAudit(deck) {
       out.push({ check: "missing-backup", severity: "P2",
         detail: "defense deck has no Backup/Appendix section divider followed by at least one slide — examiners' questions need it" });
     }
-    if (!slides.some((s) => LIMITS_RE.test(titleOf(s)) && !PRIOR_WORK_RE.test(titleOf(s)))) {
+    if (slides.some((s) => LIMITS_RE.test(titleOf(s)) && !PRIOR_WORK_RE.test(titleOf(s)))) {
       out.push({ check: "missing-limitations", severity: "P2",
         detail: "defense deck has no slide titled for limitations or future work" });
     }

```
## baseline setup

```sh
cp -a /home/ubuntu/jason/research/.autopilot-deps/ss-node/node_modules/. scholar-slides/node_modules/
```

exit 0; timed out: no

```


```
## baseline (unpatched)

```sh
cd scholar-slides && node --test tests/deck_type.test.mjs
```

exit 0; timed out: no

```
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.284153
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.247329
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.289782
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.245787
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.23467
  type: 'test'
  ...
1..17
# tests 17
# suites 0
# pass 17
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 687.594848

```
- source guard: PASS (source write denied; artifact output writable)
- sandbox probes: PASS (allowed read; outside read/write denied; external-address socket denied)
## mutant setup

```sh
cp -a /home/ubuntu/jason/research/.autopilot-deps/ss-node/node_modules/. scholar-slides/node_modules/
```

exit 0; timed out: no

```


```
## mutant (patched)

```sh
cd scholar-slides && node --test tests/deck_type.test.mjs
```

exit 1; timed out: no

```

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'missing-backup'
    1: 'missing-limitations'
  actual:
    0: 'missing-backup'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:102:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
not ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.45616
  type: 'test'
  location: '/tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:108:1'
  failureType: 'testCodeFailure'
  error: |-
    Limitations of existing methods
    + actual - expected

    + []
    - [
    -   'P2:missing-limitations'
    - ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P2:missing-limitations'
  actual:
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:112:12)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
not ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.480487
  type: 'test'
  location: '/tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:116:1'
  failureType: 'testCodeFailure'
  error: |-
    Limitations
    + actual - expected

    + [
    +   {
    +     check: 'missing-limitations',
    +     detail: 'defense deck has no slide titled for limitations or future work',
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-limitations'
      severity: 'P2'
      detail: 'defense deck has no slide titled for limitations or future work'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:120:12)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
not ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.384774
  type: 'test'
  location: '/tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:124:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      [
        'P2:missing-backup',
    +   'P2:missing-limitations'
      ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P2:missing-backup'
  actual:
    0: 'P2:missing-backup'
    1: 'P2:missing-limitations'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:126:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
not ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.372206
  type: 'test'
  location: '/tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:129:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      [
        'P2:missing-backup',
    +   'P2:missing-limitations'
      ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P2:missing-backup'
  actual:
    0: 'P2:missing-backup'
    1: 'P2:missing-limitations'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:131:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
not ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.310754
  type: 'test'
  location: '/tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:137:1'
  failureType: 'testCodeFailure'
  error: |-
    Backup slides
    + actual - expected

    + [
    +   {
    +     check: 'missing-limitations',
    +     detail: 'defense deck has no slide titled for limitations or future work',
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-limitations'
      severity: 'P2'
      detail: 'defense deck has no slide titled for limitations or future work'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.qPLEbA/mutant/scholar-slides/tests/deck_type.test.mjs:140:12)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
1..17
# tests 17
# suites 0
# pass 5
# fail 12
# cancelled 0
# skipped 0
# todo 0
# duration_ms 669.010846

```
- finished: 2026-10-24T15:15:51Z
- result: KILLED
