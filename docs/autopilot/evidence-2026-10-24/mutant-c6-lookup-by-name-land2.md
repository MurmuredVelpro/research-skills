# Mutant — mutant-c6-lookup-by-name-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:25:37Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: b3e32fb4199b9246c28e8d7c04a924fc82252fbb0ec0794e7df71b79492c0d86
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
- failure signature: ^\s*not ok \d+ - a\ slide\ changed\ after\ proofreading\ is\ unproofread\ again$; expected exit: 1
- mutated files: paper-slide-deck/scripts/proofread.ts
- patch sha256: 638a85afbcd41072a5f6dfddb0847c278132c2798ed88629bc31249ba53f94c4

```diff
diff --git a/paper-slide-deck/scripts/proofread.ts b/paper-slide-deck/scripts/proofread.ts
index f9d773d..076ff37 100644
--- a/paper-slide-deck/scripts/proofread.ts
+++ b/paper-slide-deck/scripts/proofread.ts
@@ -76,7 +76,7 @@ export function proofreadGate(
     const hash = sha256File(slide.path);
     seenHashes.add(hash);
     if (!(slide.filename in generated) && !generatedHashes.has(hash)) continue; // extracted / hand-made
-    const entry = proofreadByHash.get(hash);
+    const entry = proofread[slide.filename];
     if (entry && STATUSES.has(entry.status ?? "")) {
       if (entry.status === "check") checks.push(`${slide.filename}${entry.note ? ` — ${entry.note}` : ""}`);
     } else if (slide.filename in proofread) {

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
  duration_ms: 6.4289
  type: 'test'
  ...
# Subtest: a renamed generated slide is still gated, and its disposition follows its bytes
ok 17 - a renamed generated slide is still gated, and its disposition follows its bytes
  ---
  duration_ms: 0.836137
  type: 'test'
  ...
# Subtest: a recorded slide missing from the deck is warned about
ok 18 - a recorded slide missing from the deck is warned about
  ---
  duration_ms: 0.569018
  type: 'test'
  ...
# Subtest: prompts without a generated.json ledger are warned about (Gemini Web path)
ok 19 - prompts without a generated.json ledger are warned about (Gemini Web path)
  ---
  duration_ms: 0.403573
  type: 'test'
  ...
# Subtest: slides in the slides/ subdirectory can be recorded and marked
ok 20 - slides in the slides/ subdirectory can be recorded and marked
  ---
  duration_ms: 0.70973
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
# duration_ms 443.347055

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
TAP version 13
# Error: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition)
# Open each listed slide, check spelling / math / numbers, then record it:
#   bun proofread.ts --mark <deck-dir> <slide-file> ok|check [--note "…"]
# Or pass --allow-unproofread to merge anyway (the deck then ships unchecked).
# Warning: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition) — merging anyway (--allow-unproofread)
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-xv5D41
# Added: 01-slide-figure.png
# Added: 02-slide-method.png
# Subtest: an unproofread generated slide is fatal and named; the extracted slide is not
ok 1 - an unproofread generated slide is fatal and named; the extracted slide is not
  ---
  duration_ms: 2.876951
  type: 'test'
  ...
# Subtest: --allow-unproofread turns the refusal into a warning
ok 2 - --allow-unproofread turns the refusal into a warning
  ---
  duration_ms: 0.700384
  type: 'test'
  ...
# Subtest: an ok disposition on the same bytes passes
ok 3 - an ok disposition on the same bytes passes
  ---
  duration_ms: 1.209073
  type: 'test'
  ...
# Subtest: a slide changed after proofreading is unproofread again
not ok 4 - a slide changed after proofreading is unproofread again
  ---
  duration_ms: 1.475922
  type: 'test'
  location: '/tmp/autopilot-run.ZwI1b3/mutant/paper-slide-deck/tests/proofread.test.mjs:62:1'
  failureType: 'testCodeFailure'
  error: |-
    Expected values to be strictly equal:

    0 !== 1

  code: 'ERR_ASSERTION'
  name: 'AssertionError'
  expected: 1
  actual: 0
  operator: 'strictEqual'
  stack: |-
    TestContext.<anonymous> (file:///tmp/autopilot-run.ZwI1b3/mutant/paper-slide-deck/tests/proofread.test.mjs:67:10)
    Test.runInAsyncScope (node:async_hooks:214:14)
    Test.run (node:internal/test_runner/test:1047:25)
    Test.processPendingSubtests (node:internal/test_runner/test:744:18)
    Test.postRun (node:internal/test_runner/test:1173:19)
    Test.run (node:internal/test_runner/test:1101:12)
    async Test.processPendingSubtests (node:internal/test_runner/test:744:7)
  ...
# Subtest: a check disposition is allowed but listed with its note
ok 5 - a check disposition is allowed but listed with its note
  ---
  duration_ms: 0.680074
  type: 'test'
  ...
# Subtest: an invalid status is not a disposition
ok 6 - an invalid status is not a disposition
  ---
  duration_ms: 0.926281
  type: 'test'
  ...
# Subtest: a deck without generated.json (extract-only) is not gated
ok 7 - a deck without generated.json (extract-only) is not gated
  ---
  duration_ms: 0.411003
  type: 'test'
  ...
# Subtest: an unreadable ledger is fatal, not 'nothing to proofread'
ok 8 - an unreadable ledger is fatal, not 'nothing to proofread'
  ---
  duration_ms: 0.465956
  type: 'test'
  ...
# Subtest: merge-to-pptx refuses an unproofread deck and writes nothing
ok 9 - merge-to-pptx refuses an unproofread deck and writes nothing
  ---
  duration_ms: 2.377286
  type: 'test'
  ...
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-xv5D41/forced.pptx
# Total slides: 2
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-xv5D41
# Added: 01-slide-figure.png
# Added: 02-slide-method.png
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-xv5D41/clean.pptx
# Total slides: 2
# Error: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition)
# Open each listed slide, check spelling / math / numbers, then record it:
#   bun proofread.ts --mark <deck-dir> <slide-file> ok|check [--note "…"]
# Or pass --allow-unproofread to merge anyway (the deck then ships unchecked).
# Warning: 1 AI-generated slide(s) not proofread (SKILL.md Step 6.5): 02-slide-method.png (no proofread disposition) — merging anyway (--allow-unproofread)
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-XG5vMP
# Added: 01-slide-figure.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-XG5vMP/forced.pdf
# Total pages: 2
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-XG5vMP
# Added: 01-slide-figure.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof-XG5vMP/clean.pdf
# Total pages: 2
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof2-Pzs8LL
# Added: 01-slide-cover.png
# Added: 02-slide-method.png
# Subtest: merge-to-pptx merges with --allow-unproofread, and after proofreading
ok 10 - merge-to-pptx merges with --allow-unproofread, and after proofreading
  ---
  duration_ms: 85.780654
  type: 'test'
  ...
# Subtest: merge-to-pdf refuses an unproofread deck and writes nothing
ok 11 - merge-to-pdf refuses an unproofread deck and writes nothing
  ---
  duration_ms: 1.610482
  type: 'test'
  ...
# Subtest: merge-to-pdf merges with --allow-unproofread, and after proofreading
ok 12 - merge-to-pdf merges with --allow-unproofread, and after proofreading
  ---
  duration_ms: 181.139574
  type: 'test'
  ...
# Subtest: merge-to-pptx names every unproofread slide on stderr
ok 13 - merge-to-pptx names every unproofread slide on stderr
  ---
  duration_ms: 1.560228
  type: 'test'
  ...
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof2-Pzs8LL/o.pptx
# Total slides: 2
# Found 2 slides in: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof2-je4V8Y
# Added: 01-slide-cover.png [png]
# Added: 02-slide-method.png [png]
# Created: /tmp/autopilot-run.ZwI1b3/mutant-tmp/psd-proof2-je4V8Y/o.pdf
# Total pages: 2
# Subtest: merge-to-pptx lists [CHECK] slides and the --allow-unproofread warning
ok 14 - merge-to-pptx lists [CHECK] slides and the --allow-unproofread warning
  ---
  duration_ms: 11.183732
  type: 'test'
  ...
# Subtest: merge-to-pdf names every unproofread slide on stderr
ok 15 - merge-to-pdf names every unproofread slide on stderr
  ---
  duration_ms: 1.228362
  type: 'test'
  ...
# Subtest: merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
ok 16 - merge-to-pdf lists [CHECK] slides and the --allow-unproofread warning
  ---
  duration_ms: 7.585695
  type: 'test'
  ...
# Subtest: a renamed generated slide is still gated, and its disposition follows its bytes
ok 17 - a renamed generated slide is still gated, and its disposition follows its bytes
  ---
  duration_ms: 0.981054
  type: 'test'
  ...
# Subtest: a recorded slide missing from the deck is warned about
ok 18 - a recorded slide missing from the deck is warned about
  ---
  duration_ms: 0.606856
  type: 'test'
  ...
# Subtest: prompts without a generated.json ledger are warned about (Gemini Web path)
ok 19 - prompts without a generated.json ledger are warned about (Gemini Web path)
  ---
  duration_ms: 0.385896
  type: 'test'
  ...
# Subtest: slides in the slides/ subdirectory can be recorded and marked
ok 20 - slides in the slides/ subdirectory can be recorded and marked
  ---
  duration_ms: 0.72339
  type: 'test'
  ...
1..20
# tests 20
# suites 0
# pass 19
# fail 1
# cancelled 0
# skipped 0
# todo 0
# duration_ms 458.107611

```
- finished: 2026-10-24T16:25:43Z
- result: KILLED
