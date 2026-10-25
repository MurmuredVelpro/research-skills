# Mutant — mutant-c4-seed-record-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:45:11Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: bbbf864fd873e6f84595598746595a8d061414dbc96e3a850920fd989751378a
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestSelectTrial::test_parameters_record_method_and_seed_only_for_trials\b; expected exit: 1
- mutated files: lit-search/src/litsearch/sampling.py
- patch sha256: 0f6f336d96d4bf513fdb9b0d92e442b7f259cb8713ed299d0081544945ef0ddc

```diff
diff --git a/lit-search/src/litsearch/sampling.py b/lit-search/src/litsearch/sampling.py
index 9baaf6c..1d3d1e0 100644
--- a/lit-search/src/litsearch/sampling.py
+++ b/lit-search/src/litsearch/sampling.py
@@ -42,5 +42,5 @@ def sample_parameters(limit: int | None, method: str, seed: int, size: int) -> d
         return {}
     detail: dict[str, object] = {"method": method, "size": size}
     if method == "random":
-        detail["seed"] = seed
+        pass
     return {"sample": detail}

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
17 passed in 1.33s

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
.........FFF...F.                                                        [100%]
=================================== FAILURES ===================================
____ TestSelectTrial.test_parameters_record_method_and_seed_only_for_trials ____

self = <tests.test_screen_sample.TestSelectTrial object at 0x75d3ce3e6cc0>

    def test_parameters_record_method_and_seed_only_for_trials(self):
>       assert sample_parameters(10, "random", 7, 10) == {
            "sample": {"method": "random", "size": 10, "seed": 7}
        }
E       AssertionError: assert {'sample': {'..., 'size': 10}} == {'sample': {'...0, 'seed': 7}}
E
E         Differing items:
E         {'sample': {'method': 'random', 'size': 10}} != {'sample': {'method': 'random', 'size': 10, 'seed': 7}}
E         Use -v to get more diff

tests/test_screen_sample.py:69: AssertionError
_ TestScreenSampleCli.test_random_trial_screens_the_seeded_sample_and_records_it _

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x75d3ce3e66f0>
seeded_run = <litsearch.run.Run object at 0x75d3ce3d8770>
topic_path = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x75d3cefb45f0>

    def test_random_trial_screens_the_seeded_sample_and_records_it(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        keys = self._in_window_keys(seeded_run)
        assert len(keys) == 2
        # 种子 5 从 2 条里抽中第 2 条（尾部）；head 永远只给第 1 条
        args = ("--limit", "1", "--sample", "random", "--seed", "5")
        result = runner.invoke(app, self._cmd(topic_path, runs_root, *args))
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
        assert list(trial["decisions"]) == [keys[1]]
>       assert trial["parameters"]["sample"] == {"method": "random", "size": 1, "seed": 5}
E       AssertionError: assert {'method': 'r...m', 'size': 1} == {'method': 'r... 1, 'seed': 5}
E
E         Omitting 2 identical items, use -vv to show
E         Right contains 1 more item:
E         {'seed': 5}
E         Use -v to get more diff

tests/test_screen_sample.py:107: AssertionError
________ TestScreenSampleCli.test_the_given_seed_reaches_the_selection _________

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x75d3ce3e6180>
seeded_run = <litsearch.run.Run object at 0x75d3ceed9700>
topic_path = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_the_given_seed_reaches_th0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_the_given_seed_reaches_th0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x75d3ce3d1be0>

    def test_the_given_seed_reaches_the_selection(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        # 种子 0（默认）抽中第 2 条；种子 1 抽中第 1 条——总用默认种子的实现在这里露馅
        keys = self._in_window_keys(seeded_run)
        args = ("--limit", "1", "--sample", "random", "--seed", "1")
        result = runner.invoke(app, self._cmd(topic_path, runs_root, *args))
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
        assert list(trial["decisions"]) == [keys[0]]
>       assert trial["parameters"]["sample"]["seed"] == 1
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'seed'

tests/test_screen_sample.py:119: KeyError
_________ TestScreenSampleJev.test_jev_random_trial_records_the_sample _________

self = <tests.test_screen_sample.TestScreenSampleJev object at 0x75d3ce3e4f20>
seeded_run = <litsearch.run.Run object at 0x75d3cd724170>
topic_path = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_jev_random_trial_records_0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_jev_random_trial_records_0/runs')
profile_path = PosixPath('/tmp/autopilot-run.yt46dQ/mutant-tmp/pytest-of-ubuntu/pytest-0/test_jev_random_trial_records_0/t.jev.yaml')
respx_mock = <respx.router.MockRouter object at 0x75d3cf81a6f0>
<redacted> object at 0x75d3cd7fcd70>

    def test_jev_random_trial_records_the_sample(
        self, seeded_run, topic_path, runs_root, profile_path, respx_mock, monkeypatch  # noqa: F811
    ):
        monkeypatch.setenv("TYPESAFE_API_KEY", "k-test")
        respx_mock.post(JEV_URL).mock(
            return_value=httpx.Response(200, json=_jev_reply({"I1": 0.95, "X1": 0.02}))
        )
        result = runner.invoke(app, [
            "screen", "t", "--topic", str(topic_path), "--runs-root", str(runs_root),
            "--model", "jev", "--jev-profile", str(profile_path),
            "--limit", "1", "--sample", "random", "--seed", "1",
        ])
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
        assert trial["parameters"]["judge"] == "jev"
>       assert trial["parameters"]["sample"] == {"method": "random", "size": 1, "seed": 1}
E       AssertionError: assert {'method': 'r...m', 'size': 1} == {'method': 'r... 1, 'seed': 1}
E
E         Omitting 2 identical items, use -vv to show
E         Right contains 1 more item:
E         {'seed': 1}
E         Use -v to get more diff

tests/test_screen_sample.py:174: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestSelectTrial::test_parameters_record_method_and_seed_only_for_trials
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_random_trial_screens_the_seeded_sample_and_records_it
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_the_given_seed_reaches_the_selection
FAILED tests/test_screen_sample.py::TestScreenSampleJev::test_jev_random_trial_records_the_sample
4 failed, 13 passed in 1.56s

```
- finished: 2026-10-24T15:45:21Z
- result: KILLED
