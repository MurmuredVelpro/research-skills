# Mutant — mutant-c2-scaffold-off

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:11:11Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 4b54a24ab4e19aea353c91aa6b3e5eb5de7de8d25ef8f968cab38783b7d11ad9
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
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_scaffold_bracket_fails\b; expected exit: 1
- mutated files: research-proposal/scripts/check_proposal.py
- patch sha256: 89f5960e5325079d0b6d5257bfee70a07b2497850f2ad1fffe89a913cc93e9ea

```diff
diff --git a/research-proposal/scripts/check_proposal.py b/research-proposal/scripts/check_proposal.py
index f111820..9db0828 100644
--- a/research-proposal/scripts/check_proposal.py
+++ b/research-proposal/scripts/check_proposal.py
@@ -117,7 +117,7 @@ def check_patterns(path: Path, text: str, body, allow_flags: bool):

 def _scaffold_hit(path: Path, number: int, content: str) -> Finding | None:
     content = content.strip()
-    if content in EXEMPT_BRACKETS or EXEMPT_BRACKET_RE.match(content) or NOT_SCAFFOLD_RE.match(content):
+    if True:
         return None
     return Finding("scaffold-bracket", f"{path.name}:{number}", f"leftover scaffold field '[{content[:60]}]'")


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
cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
..........................................                               [100%]
42 passed in 0.12s

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
cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```
................F...FF....................                               [100%]
=================================== FAILURES ===================================
____________ CheckProposalTest.test_figure_label_exemption_is_exact ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_figure_label_exemption_is_exact>

    def test_figure_label_exemption_is_exact(self):
        code, out = self.run_gate(APA_CLEAN.replace("[Figure 1 Suggestion]", "[Figure 1 Suggestion: write caption here]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_proposal: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_proposal.py:268: AssertionError
_ CheckProposalTest.test_leftover_instruction_in_references_fails_but_apa_descriptors_pass _

self = <test_check_proposal.CheckProposalTest testMethod=test_leftover_instruction_in_references_fails_but_apa_descriptors_pass>

    def test_leftover_instruction_in_references_fails_but_apa_descriptors_pass(self):
        code, out = self.run_gate(APA_CLEAN + "\n[Follow appropriate citation style: APA, MLA, or Chicago]\n")
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_proposal: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_proposal.py:242: AssertionError
____________ CheckProposalTest.test_leftover_scaffold_bracket_fails ____________

self = <test_check_proposal.CheckProposalTest testMethod=test_leftover_scaffold_bracket_fails>

    def test_leftover_scaffold_bracket_fails(self):
        code, out = self.run_gate(APA_CLEAN.replace("## 1. Introduction", "## 1. Introduction\n\n[Opening sentence: Establish the broader field]"))
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_proposal: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_proposal.py:167: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_figure_label_exemption_is_exact
FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_instruction_in_references_fails_but_apa_descriptors_pass
FAILED tests/test_check_proposal.py::CheckProposalTest::test_leftover_scaffold_bracket_fails
3 failed, 39 passed in 0.17s

```
- finished: 2026-10-24T15:11:15Z
- result: KILLED
