# Mutant — mutant-c2-no-refs-section

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:10:36Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: fbacb7fd3fb32e08cf0a3b6eca84c2aa7f76b24565e35f082c3055c8b60c624f
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
- failure signature: ^FAILED tests/test_check_proposal.py::CheckProposalTest::test_citations_without_references_section_fail\b; expected exit: 1
- mutated files: research-proposal/scripts/check_proposal.py
- patch sha256: 4eb0fb6460b20dce671258e976a2462ed41b638f98d65925a027eadc041091e1

```diff
diff --git a/research-proposal/scripts/check_proposal.py b/research-proposal/scripts/check_proposal.py
index f111820..155aff2 100644
--- a/research-proposal/scripts/check_proposal.py
+++ b/research-proposal/scripts/check_proposal.py
@@ -74,7 +74,7 @@ def check_citations(path: Path, body, refs, style: str) -> list[Finding]:
         count = len(numeric_cited) + len(apa_cited)
         return [Finding("no-references-section", path.name,
                         f"{count} in-text citation(s) but no '## References' / '## 参考文献' section")
-                ] if count else []
+                ] if False else []
     findings: list[Finding] = []
     if numeric_cited and apa_cited:
         # 只按一种制式对账会把另一种引用整体漏掉——宁可失败也不静默放过

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
42 passed in 0.11s

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
.........F................................                               [100%]
=================================== FAILURES ===================================
_______ CheckProposalTest.test_citations_without_references_section_fail _______

self = <test_check_proposal.CheckProposalTest testMethod=test_citations_without_references_section_fail>

    def test_citations_without_references_section_fail(self):
        body = NUMERIC_CLEAN.split("## 参考文献")[0]
        code, out = self.run_gate(body)
>       self.assertEqual(code, 1, out)
E       AssertionError: 0 != 1 : check_proposal: no mechanical findings (0 warning(s)) — judgment items still apply

tests/test_check_proposal.py:137: AssertionError
=========================== short test summary info ============================
FAILED tests/test_check_proposal.py::CheckProposalTest::test_citations_without_references_section_fail
1 failed, 41 passed in 0.12s

```
- finished: 2026-10-24T15:10:41Z
- result: KILLED
