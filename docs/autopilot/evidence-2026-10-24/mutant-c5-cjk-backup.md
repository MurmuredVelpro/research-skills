# Mutant — mutant-c5-cjk-backup

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:15:37Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 25e6105a089dc0b12c9c488e79308a35c9c0d6d5009d2e916eb2e385417c9a35
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
- failure signature: ^\s*not ok \d+ - defense:\ Chinese\ 附录\ divider\ counts\ as\ Backup$; expected exit: 1
- mutated files: scholar-slides/scripts/lib/qa.mjs
- patch sha256: 40f94c26329d0a453b5816dacaafbbd302692c73d8d19a0b29c62761ea0ff163

```diff
diff --git a/scholar-slides/scripts/lib/qa.mjs b/scholar-slides/scripts/lib/qa.mjs
index 8772ef8..83caf0c 100644
--- a/scholar-slides/scripts/lib/qa.mjs
+++ b/scholar-slides/scripts/lib/qa.mjs
@@ -167,7 +167,7 @@ export function figureCrowding(deck, { maxChars = 240 } = {}) {
 // journal club. Returns findings with severity; qa_report wires them in.
 export const DECK_TYPES = ["journal-club", "conference", "defense"];
 // The divider must BE the backup (title starts with the word), not merely mention one.
-const BACKUP_RE = /^\s*(backup|appendix|附录|备用|备份)(?=$|[\s:：\-–—(（]|slides)/i;
+const BACKUP_RE = /^\s*(backup|appendix|备用|备份)(?=$|[\s:：\-–—(（]|slides)/i;
 // Own limitations / future work — not a motivation slide about prior work's shortcomings.
 const LIMITS_RE = /\blimitations?\b|\bfuture (work|directions?)\b|局限|展望|未来工作|不足/i;
 const PRIOR_WORK_RE = /\b(existing|prior|previous|related|baselines?|state[- ]of[- ]the[- ]art)\b|现有|已有|传统|以往|前人/i;

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
  duration_ms: 0.298013
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.27439
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.438425
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.276452
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.238365
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
# duration_ms 660.601825

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
TAP version 13
# Subtest: a conforming deck of each type has no deck-type finding
ok 1 - a conforming deck of each type has no deck-type finding
  ---
  duration_ms: 2.210959
  type: 'test'
  ...
# Subtest: journal-club: each missing critique / discussion slide is a P2 naming the layout
ok 2 - journal-club: each missing critique / discussion slide is a P2 naming the layout
  ---
  duration_ms: 0.470502
  type: 'test'
  ...
# Subtest: absent deck_type is audited as journal-club
ok 3 - absent deck_type is audited as journal-club
  ---
  duration_ms: 0.171857
  type: 'test'
  ...
# Subtest: defense: no Backup divider is a P2
ok 4 - defense: no Backup divider is a P2
  ---
  duration_ms: 0.360587
  type: 'test'
  ...
# Subtest: defense: a Backup divider with nothing after it is a P2
ok 5 - defense: a Backup divider with nothing after it is a P2
  ---
  duration_ms: 0.176875
  type: 'test'
  ...
# Subtest: defense: Chinese 附录 divider counts as Backup
not ok 6 - defense: Chinese 附录 divider counts as Backup
  ---
  duration_ms: 2.147324
  type: 'test'
  location: '/tmp/autopilot-run.15gf06/mutant/scholar-slides/tests/deck_type.test.mjs:65:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

    + [
    +   {
    +     check: 'missing-backup',
    +     detail: "defense deck has no Backup/Appendix section divider followed by at least one slide — examiners' questions need it",
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-backup'
      severity: 'P2'
      detail: "defense deck has no Backup/Appendix section divider followed by at least one slide — examiners' questions need it"
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.15gf06/mutant/scholar-slides/tests/deck_type.test.mjs:67:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: no limitations / future-work slide is a P2
ok 7 - defense: no limitations / future-work slide is a P2
  ---
  duration_ms: 0.365245
  type: 'test'
  ...
# Subtest: defense: Chinese 局限与展望 title counts
ok 8 - defense: Chinese 局限与展望 title counts
  ---
  duration_ms: 0.467708
  type: 'test'
  ...
# Subtest: conference: a critique slide is a P3 on that slide
ok 9 - conference: a critique slide is a P3 on that slide
  ---
  duration_ms: 0.477343
  type: 'test'
  ...
# Subtest: conference does not demand journal-club archetypes
ok 10 - conference does not demand journal-club archetypes
  ---
  duration_ms: 0.448338
  type: 'test'
  ...
# Subtest: unknown deck_type is P1 naming the allowed values
ok 11 - unknown deck_type is P1 naming the allowed values
  ---
  duration_ms: 0.319987
  type: 'test'
  ...
# Subtest: qa_report carries deck-type findings into the CKPT-3 report
ok 12 - qa_report carries deck-type findings into the CKPT-3 report
  ---
  duration_ms: 1.91076
  type: 'test'
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.22119
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.24799
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.262831
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.202312
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
not ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.565665
  type: 'test'
  location: '/tmp/autopilot-run.15gf06/mutant/scholar-slides/tests/deck_type.test.mjs:137:1'
  failureType: 'testCodeFailure'
  error: |-
    附录：补充实验
    + actual - expected

    + [
    +   {
    +     check: 'missing-backup',
    +     detail: "defense deck has no Backup/Appendix section divider followed by at least one slide — examiners' questions need it",
    +     severity: 'P2'
    +   }
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0:
      check: 'missing-backup'
      severity: 'P2'
      detail: "defense deck has no Backup/Appendix section divider followed by at least one slide — examiners' questions need it"
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.15gf06/mutant/scholar-slides/tests/deck_type.test.mjs:140:12)
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
# pass 15
# fail 2
# cancelled 0
# skipped 0
# todo 0
# duration_ms 634.168733

```
- finished: 2026-10-24T15:15:43Z
- result: KILLED
