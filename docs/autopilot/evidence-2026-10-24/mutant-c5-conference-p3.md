# Mutant — mutant-c5-conference-p3

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:16:20Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 50060b24056182aa17d1a1d98b4a00c63427d308966a38ed285b5d03e7b50968
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
- failure signature: ^\s*not ok \d+ - conference:\ a\ critique\ slide\ is\ a\ P3\ on\ that\ slide$; expected exit: 1
- mutated files: scholar-slides/scripts/lib/qa.mjs
- patch sha256: 0f9cbd27afa665b0a9ffecccd9f08e019aeaa5110867f5f0d74f7f11dffe1406

```diff
diff --git a/scholar-slides/scripts/lib/qa.mjs b/scholar-slides/scripts/lib/qa.mjs
index 8772ef8..5bd1432 100644
--- a/scholar-slides/scripts/lib/qa.mjs
+++ b/scholar-slides/scripts/lib/qa.mjs
@@ -203,7 +203,7 @@ export function deckTypeAudit(deck) {
     }
   } else if (type === "conference") {
     slides.forEach((s, i) => {
-      if (s.layout === "critique-concerns") out.push({ check: "critique-in-conference", severity: "P3", slide: i + 1,
+      if (s.layout === "critique-concerns") out.push({ check: "critique-in-conference", severity: "P2", slide: i + 1,
         detail: "a conference talk presents its own work — drop the critique slide or move it to backup" });
     });
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
  duration_ms: 0.217455
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.206539
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.252066
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.258996
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.230443
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
# duration_ms 690.269952

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
  duration_ms: 2.352179
  type: 'test'
  ...
# Subtest: journal-club: each missing critique / discussion slide is a P2 naming the layout
ok 2 - journal-club: each missing critique / discussion slide is a P2 naming the layout
  ---
  duration_ms: 0.472414
  type: 'test'
  ...
# Subtest: absent deck_type is audited as journal-club
ok 3 - absent deck_type is audited as journal-club
  ---
  duration_ms: 0.186519
  type: 'test'
  ...
# Subtest: defense: no Backup divider is a P2
ok 4 - defense: no Backup divider is a P2
  ---
  duration_ms: 0.403582
  type: 'test'
  ...
# Subtest: defense: a Backup divider with nothing after it is a P2
ok 5 - defense: a Backup divider with nothing after it is a P2
  ---
  duration_ms: 0.216062
  type: 'test'
  ...
# Subtest: defense: Chinese 附录 divider counts as Backup
ok 6 - defense: Chinese 附录 divider counts as Backup
  ---
  duration_ms: 0.45651
  type: 'test'
  ...
# Subtest: defense: no limitations / future-work slide is a P2
ok 7 - defense: no limitations / future-work slide is a P2
  ---
  duration_ms: 0.258486
  type: 'test'
  ...
# Subtest: defense: Chinese 局限与展望 title counts
ok 8 - defense: Chinese 局限与展望 title counts
  ---
  duration_ms: 0.364954
  type: 'test'
  ...
# Subtest: conference: a critique slide is a P3 on that slide
not ok 9 - conference: a critique slide is a P3 on that slide
  ---
  duration_ms: 1.589882
  type: 'test'
  location: '/tmp/autopilot-run.O8q694/mutant/scholar-slides/tests/deck_type.test.mjs:82:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      [
    +   'P2:critique-in-conference'
    -   'P3:critique-in-conference'
      ]

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    0: 'P3:critique-in-conference'
  actual:
    0: 'P2:critique-in-conference'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.O8q694/mutant/scholar-slides/tests/deck_type.test.mjs:85:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: conference does not demand journal-club archetypes
ok 10 - conference does not demand journal-club archetypes
  ---
  duration_ms: 0.497502
  type: 'test'
  ...
# Subtest: unknown deck_type is P1 naming the allowed values
ok 11 - unknown deck_type is P1 naming the allowed values
  ---
  duration_ms: 0.277013
  type: 'test'
  ...
# Subtest: qa_report carries deck-type findings into the CKPT-3 report
ok 12 - qa_report carries deck-type findings into the CKPT-3 report
  ---
  duration_ms: 1.719034
  type: 'test'
  ...
# Subtest: defense: a motivation slide about prior work's limitations is not the thesis's own
ok 13 - defense: a motivation slide about prior work's limitations is not the thesis's own
  ---
  duration_ms: 0.237915
  type: 'test'
  ...
# Subtest: defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
ok 14 - defense: 'Limitations' alone and 'Future work' alone each satisfy the rule
  ---
  duration_ms: 0.211996
  type: 'test'
  ...
# Subtest: defense: only a closing Q&A after the Backup divider is not an appendix
ok 15 - defense: only a closing Q&A after the Backup divider is not an appendix
  ---
  duration_ms: 0.278075
  type: 'test'
  ...
# Subtest: defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
ok 16 - defense: a divider that merely mentions backup, or a non-divider titled Backup, does not count
  ---
  duration_ms: 0.182082
  type: 'test'
  ...
# Subtest: defense: 'Backup slides' and 'Appendix: proofs' dividers count
ok 17 - defense: 'Backup slides' and 'Appendix: proofs' dividers count
  ---
  duration_ms: 0.199057
  type: 'test'
  ...
1..17
# tests 17
# suites 0
# pass 16
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 681.444076

```
- finished: 2026-10-24T15:16:26Z
- result: KILLED
