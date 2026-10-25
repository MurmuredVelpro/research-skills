# Mutant — mutant-c4-head-tail-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:46:14Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: f26b4a4f9c4fc3496099a9fbd520193b9f9d386a499037c896e3ae241f5304f9
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestSelectTrial::test_head_is_the_prefix\b; expected exit: 1
- mutated files: lit-search/src/litsearch/sampling.py
- patch sha256: 82f955c2bc7a4e3635cd57ea93d01964e2366effff8cdcd171d7f3b265304a1c

```diff
diff --git a/lit-search/src/litsearch/sampling.py b/lit-search/src/litsearch/sampling.py
index 9baaf6c..fab043b 100644
--- a/lit-search/src/litsearch/sampling.py
+++ b/lit-search/src/litsearch/sampling.py
@@ -31,7 +31,7 @@ def select_trial(records: Sequence[T], limit: int | None, method: str, seed: int
             raise SampleError("--sample random 必须配合 --limit N 使用")
         return list(records)
     if method == "head" or limit >= len(records):
-        return list(records[:limit])
+        return list(records[-limit:])
     chosen = sorted(random.Random(seed).sample(range(len(records)), limit))
     return [records[index] for index in chosen]


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
cd lit-search && /home/ubuntu/jason/research/.autopilot-deps/lit-venv/bin/python -B -m pytest -p no:cacheprovider -o pythonpath=src tests/test_screen_sample.py
```

exit 0; timed out: no

```
.................                                                        [100%]
17 passed in 1.15s

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
cd lit-search && /home/ubuntu/jason/research/.autopilot-deps/lit-venv/bin/python -B -m pytest -p no:cacheprovider -o pythonpath=src tests/test_screen_sample.py
```

exit 1; timed out: no

```
F............F...                                                        [100%]
=================================== FAILURES ===================================
___________________ TestSelectTrial.test_head_is_the_prefix ____________________

self = <tests.test_screen_sample.TestSelectTrial object at 0x72397a8d3fe0>

    def test_head_is_the_prefix(self):
>       assert select_trial(CORPUS, 10, "head", 0) == CORPUS[:10]
E       assert [40, 41, 42, 43, 44, 45, ...] == [0, 1, 2, 3, 4, 5, ...]
E
E         At index 0 diff: 40 != 0
E         Use -v to get more diff

tests/test_screen_sample.py:35: AssertionError
_____________ TestScreenSampleCli.test_head_trial_keeps_the_prefix _____________

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x72397a8d18e0>
seeded_run = <litsearch.run.Run object at 0x723979f3c8c0>
topic_path = PosixPath('/tmp/autopilot-run.Ss0bgH/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.Ss0bgH/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x723979f3c470>

    def test_head_trial_keeps_the_prefix(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        keys = self._in_window_keys(seeded_run)
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--limit", "1"))
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
>       assert list(trial["decisions"]) == [keys[0]]
E       AssertionError: assert ['doi:10.1007...-021-06816-8'] == ['doi:10.1038...-022-01875-5']
E
E         At index 0 diff: 'doi:10.1007/s00521-021-06816-8' != 'doi:10.1038/s41597-022-01875-5'
E         Use -v to get more diff

tests/test_screen_sample.py:137: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestSelectTrial::test_head_is_the_prefix
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_head_trial_keeps_the_prefix
2 failed, 15 passed in 1.14s

```
- finished: 2026-10-24T15:46:23Z
- result: KILLED
