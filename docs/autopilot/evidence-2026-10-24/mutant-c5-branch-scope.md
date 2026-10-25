# Mutant — mutant-c5-branch-scope

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:16:28Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 91159a66f57dd1cdc2b5171bd27112fad7542b1ccd666aaf267b8fd89b10d4e2
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
- failure signature: ^\s*not ok \d+ - conference\ does\ not\ demand\ journal\-club\ archetypes$; expected exit: 1
- mutated files: scholar-slides/scripts/lib/qa.mjs
- patch sha256: 530b2a0865c798e38d5f9ff124430adb169d4bfa2c7f75edaa082174da05d7a1

```diff
diff --git a/scholar-slides/scripts/lib/qa.mjs b/scholar-slides/scripts/lib/qa.mjs
index 8772ef8..32b6512 100644
--- a/scholar-slides/scripts/lib/qa.mjs
+++ b/scholar-slides/scripts/lib/qa.mjs
@@ -184,7 +184,7 @@ export function deckTypeAudit(deck) {
   const has = (layout) => slides.some((s) => s.layout === layout);
   const titleOf = (s) => [s.title, s.action_title].filter(Boolean).join(" ");
   const out = [];
-  if (type === "journal-club") {
+  if (type !== "defense") {
     for (const layout of ["critique-concerns", "discussion-questions"]) {
       if (!has(layout)) out.push({ check: "missing-archetype", severity: "P2",
         detail: `journal-club deck has no ${layout} slide — a 组会 owes the room a critique and discussion (references/deck-types.md)` });

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
  duration_ms: 0.225857
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.203793
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.266497
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.189413
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.181361
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
# duration_ms 653.735922

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
    +   {
    +     check: 'missing-archetype',
    +     detail: 'journal-club deck has no discussion-questions slide — a 组会 owes the room a critique and discussion (references/deck-types.md)',
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-archetype'
      severity: 'P2'
      detail: 'journal-club deck has no critique-concerns slide — a 组会 owes the room a critique and discussion (references/deck-types.md)'
    1:
      check: 'missing-archetype'
      severity: 'P2'
      detail: 'journal-club deck has no discussion-questions slide — a 组会 owes the room a critique and discussion (references/deck-types.md)'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.sKPH4G/mutant/scholar-slides/tests/deck_type.test.mjs:37:12)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.start (node:internal/test_runner/test:944:17)
    startSubtestAfterBootstrap (node:internal/test_runner/harness:296:17)
  ...
# Subtest: journal-club: each missing critique / discussion slide is a P2 naming the layout
ok 2 - journal-club: each missing critique / discussion slide is a P2 naming the layout
  ---
  duration_ms: 0.494868
  type: 'test'
  ...
# Subtest: absent deck_type is audited as journal-club
ok 3 - absent deck_type is audited as journal-club
  ---
  duration_ms: 0.212687
  type: 'test'
  ...
# Subtest: defense: no Backup divider is a P2
ok 4 - defense: no Backup divider is a P2
  ---
  duration_ms: 0.52281
  type: 'test'
  ...
# Subtest: defense: a Backup divider with nothing after it is a P2
ok 5 - defense: a Backup divider with nothing after it is a P2
  ---
  duration_ms: 0.204906
  type: 'test'
  ...
# Subtest: defense: Chinese 附录 divider counts as Backup
ok 6 - defense: Chinese 附录 divider counts as Backup
  ---
  duration_ms: 0.319457
  type: 'test'
  ...
# Subtest: defense: no limitations / future-work slide is a P2
ok 7 - defense: no limitations / future-work slide is a P2
  ---
  duration_ms: 0.343042
  type: 'test'
  ...
# Subtest: defense: Chinese 局限与展望 title counts
ok 8 - defense: Chinese 局限与展望 title counts
  ---
  duration_ms: 0.406227
  type: 'test'
  ...
# Subtest: conference: a critique slide is a P3 on that slide
not ok 9 - conference: a critique slide is a P3 on that slide
  ---
  duration_ms: 0.755287
  type: 'test'
  location: '/tmp/autopilot-run.sKPH4G/mutant/scholar-slides/tests/deck_type.test.mjs:82:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      [
    +   'P2:missing-archetype'
    -   'P3:critique-in-conference'
      ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P3:critique-in-conference'
  actual:
    0: 'P2:missing-archetype'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.sKPH4G/mutant/scholar-slides/tests/deck_type.test.mjs:85:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: conference does not demand journal-club archetypes
not ok 10 - conference does not demand journal-club archetypes
  ---
  duration_ms: 0.904299
  type: 'test'
  location: '/tmp/autopilot-run.sKPH4G/mutant/scholar-slides/tests/deck_type.test.mjs:89:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

    + [
    +   {
    +     check: 'missing-archetype',
    +     detail: 'journal-club deck has no critique-concerns slide — a 组会 owes the room a critique and discussion (references/deck-types.md)',
    +     severity: 'P2'
    +   },
    +   {
    +     check: 'missing-archetype',
    +     detail: 'journal-club deck has no discussion-questions slide — a 组会 owes the room a critique and discussion (references/deck-types.md)',
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-archetype'
      severity: 'P2'
      detail: 'journal-club deck has no critique-concerns slide — a 组会 owes the room a critique and discussion (references/deck-types.md)'
    1:
      check: 'missing-archetype'
      severity: 'P2'
      detail: 'journal-club deck has no discussion-questions slide — a 组会 owes the room a critique and discussion (references/deck-types.md)'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.sKPH4G/mutant/scholar-slides/tests/deck_type.test.mjs:90:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: unknown deck_type is P1 naming the allowed values
ok 11 - unknown deck_type is P1 naming the allowed values
  ---
  duration_ms: 0.28171
  type: 'test'
  ...
# Subtest: qa_report carries deck-type findings into the CKPT-3 report
ok 12 - qa_report carries deck-type findings into the CKPT-3 report
  ---
  duration_ms: 1.7159
  type: 'test'
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.220119
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.207579
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.244704
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.182302
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.182521
  type: 'test'
  ...
1..17
# tests 17
# suites 0
# pass 14
# fail 3
# cancelled 0
# skipped 0
# todo 0
# duration_ms 671.577417

```
- finished: 2026-10-24T15:16:33Z
- result: KILLED
