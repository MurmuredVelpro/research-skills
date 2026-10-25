# Mutant — mutant-c6-sha-empty-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:48:42Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 2b7507c72bf06b9673ce1a2118480f2b3fb4475850a74185877bb450a3edba3a
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
- failure signature: ^FAILED tests/test_generate_slides\.py::test_record_generated_writes_sha_prompt_and_model\b; expected exit: 1
- mutated files: paper-slide-deck/scripts/generate-slides.py
- patch sha256: da72cb13c1bdcc10fdaf00f9b2aa98bd14815236687d3e4fa41affa32b6e9e77

```diff
diff --git a/paper-slide-deck/scripts/generate-slides.py b/paper-slide-deck/scripts/generate-slides.py
index 445b82a..71f1938 100644
--- a/paper-slide-deck/scripts/generate-slides.py
+++ b/paper-slide-deck/scripts/generate-slides.py
@@ -217,7 +217,7 @@ def record_generated(deck_dir: Path, output_path: Path, prompt_file: Path, model
     stem = output_path.stem
     slides = {name: entry for name, entry in slides.items() if Path(name).stem != stem}
     slides[output_path.name] = {
-        "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
+        "sha256": hashlib.sha256(b"").hexdigest(),
         "prompt": f"prompts/{prompt_file.name}",
         "model": model,
     }

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
cd paper-slide-deck && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 0; timed out: no

```
...............                                                          [100%]
15 passed in 0.09s

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
cd paper-slide-deck && python3 -B -m pytest tests/ -q -p no:cacheprovider
```

exit 1; timed out: no

```
...........F...                                                          [100%]
=================================== FAILURES ===================================
______________ test_record_generated_writes_sha_prompt_and_model _______________

gs = <module 'generate_slides' from '/tmp/autopilot-run.zETyHl/mutant/paper-slide-deck/scripts/generate-slides.py'>
tmp_path = PosixPath('/tmp/autopilot-run.zETyHl/mutant-tmp/pytest-of-ubuntu/pytest-0/test_record_generated_writes_s0')

    def test_record_generated_writes_sha_prompt_and_model(gs, tmp_path):
        import hashlib
        import json

        slide = tmp_path / "03-slide-results.png"
        slide.write_bytes(b"\x89PNG fake bytes")
        gs.record_generated(tmp_path, slide, tmp_path / "prompts" / "03-slide-results.md", "gemini-x")
        entry = json.loads((tmp_path / "generated.json").read_text())["slides"]["03-slide-results.png"]
>       assert entry == {
            "sha256": hashlib.sha256(b"\x89PNG fake bytes").hexdigest(),
            "prompt": "prompts/03-slide-results.md",
            "model": "gemini-x",
        }
E       AssertionError: assert {'model': 'ge...991b7852b855'} == {'model': 'ge...7b5b98d515e6'}
E         Omitting 2 identical items, use -vv to show
E         Differing items:
E         {'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'} != {'sha256': '707b55b97725e5ddc58dbea8eaff61602906f61d4d33b34a91b37b5b98d515e6'}
E         Use -v to get more diff

tests/test_generate_slides.py:115: AssertionError
=========================== short test summary info ============================
FAILED tests/test_generate_slides.py::test_record_generated_writes_sha_prompt_and_model
1 failed, 14 passed in 0.11s

```
- finished: 2026-10-24T15:48:46Z
- result: KILLED
