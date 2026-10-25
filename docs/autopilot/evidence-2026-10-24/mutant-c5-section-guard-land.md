# Mutant — mutant-c5-section-guard-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:47:20Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 518d245ef8a2a81f3728d05cf39c21e4168e700047dddf49af4622ce294a0d77
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
- failure signature: ^\s*not ok \d+ - defense:\ a\ divider\ that\ merely\ mentions\ backup,\ or\ a\ non\-divider\ titled\ Backup,\ does\ not\ count$; expected exit: 1
- mutated files: scholar-slides/scripts/lib/qa.mjs
- patch sha256: 199c3aaf4b1b3d4b19b0e1bbd3528fa2c6667631fa3a0a89a1550f06ff752834

```diff
diff --git a/scholar-slides/scripts/lib/qa.mjs b/scholar-slides/scripts/lib/qa.mjs
index 8772ef8..ae6cba4 100644
--- a/scholar-slides/scripts/lib/qa.mjs
+++ b/scholar-slides/scripts/lib/qa.mjs
@@ -190,7 +190,7 @@ export function deckTypeAudit(deck) {
         detail: `journal-club deck has no ${layout} slide — a 组会 owes the room a critique and discussion (references/deck-types.md)` });
     }
   } else if (type === "defense") {
-    const backup = slides.findIndex((s) => s.layout === "section" && BACKUP_RE.test(titleOf(s)));
+    const backup = slides.findIndex((s) => BACKUP_RE.test(titleOf(s)));
     const appendix = backup === -1 ? [] : slides.slice(backup + 1)
       .filter((s) => s.layout !== "section" && !CLOSING_RE.test(titleOf(s)));
     if (!appendix.length) {

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
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.169372
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.250613
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.168251
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.147581
  type: 'test'
  ...
# Subtest: defense: a Backup divider followed only by another divider is a P2
ok 18 - defense: a Backup divider followed only by another divider is a P2
  ---
  duration_ms: 0.124666
  type: 'test'
  ...
1..18
# tests 18
# suites 0
# pass 18
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 576.283947

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
  duration_ms: 2.615951
  type: 'test'
  ...
# Subtest: journal-club: each missing critique / discussion slide is a P2 naming the layout
ok 2 - journal-club: each missing critique / discussion slide is a P2 naming the layout
  ---
  duration_ms: 0.587596
  type: 'test'
  ...
# Subtest: absent deck_type is audited as journal-club
ok 3 - absent deck_type is audited as journal-club
  ---
  duration_ms: 0.193608
  type: 'test'
  ...
# Subtest: defense: no Backup divider is a P2
ok 4 - defense: no Backup divider is a P2
  ---
  duration_ms: 0.391955
  type: 'test'
  ...
# Subtest: defense: a Backup divider with nothing after it is a P2
ok 5 - defense: a Backup divider with nothing after it is a P2
  ---
  duration_ms: 0.204976
  type: 'test'
  ...
# Subtest: defense: Chinese 附录 divider counts as Backup
ok 6 - defense: Chinese 附录 divider counts as Backup
  ---
  duration_ms: 0.426406
  type: 'test'
  ...
# Subtest: defense: no limitations / future-work slide is a P2
ok 7 - defense: no limitations / future-work slide is a P2
  ---
  duration_ms: 0.258385
  type: 'test'
  ...
# Subtest: defense: Chinese 局限与展望 title counts
ok 8 - defense: Chinese 局限与展望 title counts
  ---
  duration_ms: 0.357544
  type: 'test'
  ...
# Subtest: conference: a critique slide is a P3 on that slide
ok 9 - conference: a critique slide is a P3 on that slide
  ---
  duration_ms: 0.476091
  type: 'test'
  ...
# Subtest: conference does not demand journal-club archetypes
ok 10 - conference does not demand journal-club archetypes
  ---
  duration_ms: 0.433927
  type: 'test'
  ...
# Subtest: unknown deck_type is P1 naming the allowed values
ok 11 - unknown deck_type is P1 naming the allowed values
  ---
  duration_ms: 0.274698
  type: 'test'
  ...
# Subtest: qa_report carries deck-type findings into the CKPT-3 report
ok 12 - qa_report carries deck-type findings into the CKPT-3 report
  ---
  duration_ms: 1.66985
  type: 'test'
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.248641
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.203312
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.241249
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
not ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 1.23395
  type: 'test'
  location: '/tmp/autopilot-run.a58zyj/mutant/scholar-slides/tests/deck_type.test.mjs:129:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

    + []
    - [
    -   'P2:missing-backup'
    - ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P2:missing-backup'
  actual:
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.a58zyj/mutant/scholar-slides/tests/deck_type.test.mjs:134:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.226478
  type: 'test'
  ...
# Subtest: defense: a Backup divider followed only by another divider is a P2
ok 18 - defense: a Backup divider followed only by another divider is a P2
  ---
  duration_ms: 0.149834
  type: 'test'
  ...
1..18
# tests 18
# suites 0
# pass 17
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 606.658051

```
- finished: 2026-10-24T15:47:25Z
- result: KILLED
