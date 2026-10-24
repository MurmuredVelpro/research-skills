# Mutant — mutant-c1c-ai-tell-case-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:05:59Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 3bd9a130894c3d9bf80589f5508b5dd2a29fc7f3535ce6472424480b2aa5b37b
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
- failure signature: ^FAILED tests/test_check_paper.py::CheckPaperTest::test_ai_tell_fails\b; expected exit: 1
- mutated files: research-paper/scripts/check_paper.py
- patch sha256: c72ac7c6045dfaf202017d373ed0b69e345ce3a52a90fb977c4ce60b494ab0bd

```diff
diff --git a/research-paper/scripts/check_paper.py b/research-paper/scripts/check_paper.py
index 816d8ac..e9b2fc9 100644
--- a/research-paper/scripts/check_paper.py
+++ b/research-paper/scripts/check_paper.py
@@ -79,7 +79,7 @@ def check_patterns(draft: Path, text: str, allow_flags: bool) -> tuple[list[Find
     for line, hit, context in pattern_hits(text, PLACEHOLDER_PATTERN):
         item = Finding("placeholder", f"{draft.name}:{line}", f"'{hit}' in: {context[:80]}")
         (warnings if allow_flags and DISCLOSED_FLAG_RE.match(hit) else findings).append(item)
-    for line, hit, context in pattern_hits(text, AI_TELL_PATTERN, ignore_case=True):
+    for line, hit, context in pattern_hits(text, AI_TELL_PATTERN, ignore_case=False):
         findings.append(Finding("ai-tell", f"{draft.name}:{line}", f"'{hit}' in: {context[:80]}"))
     return findings, warnings


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
cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
....................................                                     [100%]
36 passed in 0.16s

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
cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```
F...................................                                     [100%]
=================================== FAILURES ===================================
______________________ CheckPaperTest.test_ai_tell_fails _______________________

self = <test_check_paper.CheckPaperTest testMethod=test_ai_tell_fails>

    def test_ai_tell_fails(self):
        self.write(draft=CLEAN_DRAFT.replace("## 2. Methods", "In recent years, X grew.\n\n## 2. Methods"))
        code, out = self.run_gate()
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_paper: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_paper.py:255: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_paper.py::CheckPaperTest::test_ai_tell_fails - Assert...
1 failed, 35 passed in 0.17s

```
- finished: 2026-10-24T16:06:05Z
- result: KILLED
