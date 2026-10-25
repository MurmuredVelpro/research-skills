# Mutant — mutant-c6-no-ledger-fail-closed-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:17:37Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: b95ebe3ddb0688e731f0c1389463cb8370dd9bcf4a5df38aa2c0e3a88dfcc799
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
- failure signature: ^\s*not ok \d+ - a\ deck\ without\ generated\.json\ \(extract\-only\)\ is\ not\ gated$; expected exit: 1
- mutated files: paper-slide-deck/scripts/proofread.ts
- patch sha256: 9762413d4136a04c4d74c67bfb7d547550105d0b923d432a62da689adb7f5524

```diff
diff --git a/paper-slide-deck/scripts/proofread.ts b/paper-slide-deck/scripts/proofread.ts
index f9d773d..7ea860e 100644
--- a/paper-slide-deck/scripts/proofread.ts
+++ b/paper-slide-deck/scripts/proofread.ts
@@ -53,6 +53,7 @@ export function proofreadGate(
       warnings.push(`no ${GENERATED}: the proofread gate cannot tell which slides are AI-generated — ` +
         `record them with \`proofread.ts --record <deck-dir> <slide-file>\` (Gemini Web path) and proofread them`);
     }
+    fatal.push("no generated.json");
     return { fatal, warnings, checks };
   }
   let generated: Record<string, Entry>;

```
## baseline setup

```sh
cp -a /home/ubuntu/jason/research/.autopilot-deps/psd-node/node_modules/. paper-slide-deck/scripts/node_modules/
```

exit 0; timed out: no

```


```
## baseline (unpatched)

```sh
cd paper-slide-deck && node --test tests/proofread.test.mjs
```

exit 0; timed out: no

```
  ...
# Subtest: merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
ok 16 - merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
  ---
  duration_ms: 8.224128
  type: 'test'
  ...
# Subtest: a renamed generated slide is still gated, and its disposition follows its bytes
ok 17 - a renamed generated slide is still gated, and its disposition follows its bytes
  ---
  duration_ms: 0.725231
  type: 'test'
  ...
# Subtest: a recorded slide missing from the deck is warned about
ok 18 - a recorded slide missing from the deck is warned about
  ---
  duration_ms: 0.631081
  type: 'test'
  ...
# Subtest: prompts without a generated.json ledger are warned about (Gemini Web path)
ok 19 - prompts without a generated.json ledger are warned about (Gemini Web path)
  ---
  duration_ms: 0.29548
  type: 'test'
  ...
# Subtest: slides in the slides/ subdirectory can be recorded and marked
ok 20 - slides in the slides/ subdirectory can be recorded and marked
  ---
  duration_ms: 0.621187
  type: 'test'
  ...
1..20
# tests 20
# suites 0
# pass 20
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 433.133266

```
- source guard: PASS (source write denied; artifact output writable)
- sandbox probes: PASS (allowed read; outside read/write denied; external-address socket denied)
## mutant setup

```sh
cp -a /home/ubuntu/jason/research/.autopilot-deps/psd-node/node_modules/. paper-slide-deck/scripts/node_modules/
```

exit 0; timed out: no

```


```
## mutant (patched)

```sh
cd paper-slide-deck && node --test tests/proofread.test.mjs
```

exit 1; timed out: no

```
  duration_ms: 1.145187
  type: 'test'
  ...
# Subtest: a check disposition is allowed but listed with its note
ok 5 - a check disposition is allowed but listed with its note
  ---
  duration_ms: 0.753414
  type: 'test'
  ...
# Subtest: an invalid status is not a disposition
ok 6 - an invalid status is not a disposition
  ---
  duration_ms: 1.089925
  type: 'test'
  ...
# Subtest: a deck without generated.json (extract-only) is not gated
not ok 7 - a deck without generated.json (extract-only) is not gated
  ---
  duration_ms: 1.7696
  type: 'test'
  location: '/tmp/autopilot-run.DxGY8O/mutant/paper-slide-deck/tests/proofread.test.mjs:85:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

      {
        checks: [],
    +   fatal: [
    +     'no generated.json'
    +   ],
    -   fatal: [],
        warnings: []
      }

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
    fatal:
    warnings:
    checks:
  actual:
    fatal:
      0: 'no generated.json'
    warnings:
    checks:
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.DxGY8O/mutant/paper-slide-deck/tests/proofread.test.mjs:87:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: an unreadable ledger is fatal, not 'nothing to proofread'
ok 8 - an unreadable ledger is fatal, not 'nothing to proofread'
  ---
  duration_ms: 0.48831
  type: 'test'
  ...
# Subtest: merge-to-pptx refuses an unproofread deck and writes nothing
ok 9 - merge-to-pptx refuses an unproofread deck and writes nothing
  ---
  duration_ms: 2.508141
  type: 'test'
  ...
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-GxS1LK/forced.pptx
# Total slides: 2
# Found 2 slides in: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-GxS1LK
# Added: 01-slide-figure.png
# Added: 02-slide-method.png
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-GxS1LK/clean.pptx
# Total slides: 2
# Error: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition)
# Open each listed slide, check spelling / math / numbers, then record it:
#   bun proofread.ts --mark <deck-dir> <slide-file> ok|check [--note "…"]
# Or pass --allow-unproofread to merge anyway (the deck then ships unchecked).
# Warning: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition) — merging anyway (--allow-unproofread)
# Found 2 slides in: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-7w0O0u
# Added: 01-slide-figure.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-7w0O0u/forced.pdf
# Total pages: 2
# Found 2 slides in: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-7w0O0u
# Added: 01-slide-figure.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof-7w0O0u/clean.pdf
# Total pages: 2
# Found 2 slides in: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof2-O61qiH
# Added: 01-slide-cover.png
# Added: 02-slide-method.png
# Subtest: merge-to-pptx merges with --allow-unproofread, and after proofreading
ok 10 - merge-to-pptx merges with --allow-unproofread, and after proofreading
  ---
  duration_ms: 77.613159
  type: 'test'
  ...
# Subtest: merge-to-pdf refuses an unproofread deck and writes nothing
ok 11 - merge-to-pdf refuses an unproofread deck and writes nothing
  ---
  duration_ms: 1.632045
  type: 'test'
  ...
# Subtest: merge-to-pdf merges with --allow-unproofread, and after proofreading
ok 12 - merge-to-pdf merges with --allow-unproofread, and after proofreading
  ---
  duration_ms: 138.521088
  type: 'test'
  ...
# Subtest: merge-to-pptx names every unproofread slide on stderr
ok 13 - merge-to-pptx names every unproofread slide on stderr
  ---
  duration_ms: 2.497826
  type: 'test'
  ...
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof2-O61qiH/o.pptx
# Total slides: 2
# Found 2 slides in: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof2-EYG6cR
# Added: 01-slide-cover.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.DxGY8O/mutant-tmp/psd-proof2-EYG6cR/o.pdf
# Total pages: 2
# Subtest: merge-to-pptx lists [CHECK] slides and the --allow-unproofread warning
ok 14 - merge-to-pptx lists [CHECK] slides and the --allow-unproofread warning
  ---
  duration_ms: 22.293216
  type: 'test'
  ...
# Subtest: merge-to-pdf names every unproofread slide on stderr
ok 15 - merge-to-pdf names every unproofread slide on stderr
  ---
  duration_ms: 1.678574
  type: 'test'
  ...
# Subtest: merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
ok 16 - merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
  ---
  duration_ms: 6.997569
  type: 'test'
  ...
# Subtest: a renamed generated slide is still gated, and its disposition follows its bytes
ok 17 - a renamed generated slide is still gated, and its disposition follows its bytes
  ---
  duration_ms: 0.909157
  type: 'test'
  ...
# Subtest: a recorded slide missing from the deck is warned about
ok 18 - a recorded slide missing from the deck is warned about
  ---
  duration_ms: 0.514707
  type: 'test'
  ...
# Subtest: prompts without a generated.json ledger are warned about (Gemini Web path)
not ok 19 - prompts without a generated.json ledger are warned about (Gemini Web path)
  ---
  duration_ms: 0.941245
  type: 'test'
  location: '/tmp/autopilot-run.DxGY8O/mutant/paper-slide-deck/tests/proofread.test.mjs:174:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly deep-equal:
    + actual - expected

    + [
    +   'no generated.json'
    + ]
    - []

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected:
  actual:
    0: 'no generated.json'
  operator: 'deepStrictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.DxGY8O/mutant/paper-slide-deck/tests/proofread.test.mjs:178:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: slides in the slides/ subdirectory can be recorded and marked
ok 20 - slides in the slides/ subdirectory can be recorded and marked
  ---
  duration_ms: 0.920013
  type: 'test'
  ...
1..20
# tests 20
# suites 0
# pass 18
# fail 2
# cancelled 0
# skipped 0
# todo 0
# duration_ms 428.717136

```
- finished: 2026-10-24T16:17:43Z
- result: KILLED
