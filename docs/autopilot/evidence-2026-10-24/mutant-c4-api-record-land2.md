# Mutant — mutant-c4-api-record-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:11:13Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 2b3a38e3562032c9cdba154f58f5882a17576cce131b10a3c58b144d3ee71bbb
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestScreenSampleCli::test_random_trial_screens_the_seeded_sample_and_records_it\b; expected exit: 1
- mutated files: lit-search/src/litsearch/cli.py
- patch sha256: c0d5b3eab5f3155bea9534d777d174be24e16665cc7be4ff3645051612ee6ce1

```diff
diff --git a/lit-search/src/litsearch/cli.py b/lit-search/src/litsearch/cli.py
index a472fae..10b0c13 100644
--- a/lit-search/src/litsearch/cli.py
+++ b/lit-search/src/litsearch/cli.py
@@ -1167,7 +1167,6 @@ def screen_command(
             "thinking": False if host else not provider.disable_thinking,
             # 只在真的用了才记：让审计时「这一轮是明知退步仍然写的」一眼看得见。
             **({"allow_regression": True} if allow_regression else {}),
-            **sampling,
         },
         prompt_sha256=hashlib.sha256(system_prompts.encode()).hexdigest(),
     )

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
17 passed in 1.18s

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
..........FF.F...                                                        [100%]
=================================== FAILURES ===================================
_ TestScreenSampleCli.test_random_trial_screens_the_seeded_sample_and_records_it _

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7107fe0de4b0>
seeded_run = <litsearch.run.Run object at 0x7107feda1df0>
topic_path = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7107fe124320>

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
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'sample'

tests/test_screen_sample.py:107: KeyError
________ TestScreenSampleCli.test_the_given_seed_reaches_the_selection _________

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7107fe0ddf70>
seeded_run = <litsearch.run.Run object at 0x7107fe0d5940>
topic_path = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_the_given_seed_reaches_th0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_the_given_seed_reaches_th0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7107fe0d1820>

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
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'sample'

tests/test_screen_sample.py:119: KeyError
_____________ TestScreenSampleCli.test_head_trial_keeps_the_prefix _____________

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7107fe0dd5e0>
seeded_run = <litsearch.run.Run object at 0x7107fd741a90>
topic_path = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.nA9eq7/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7107fd740650>

    def test_head_trial_keeps_the_prefix(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        keys = self._in_window_keys(seeded_run)
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--limit", "1"))
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
        assert list(trial["decisions"]) == [keys[0]]
>       assert trial["parameters"]["sample"] == {"method": "head", "size": 1}
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'sample'

tests/test_screen_sample.py:138: KeyError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_random_trial_screens_the_seeded_sample_and_records_it
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_the_given_seed_reaches_the_selection
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_head_trial_keeps_the_prefix
3 failed, 14 passed in 1.19s

```
- finished: 2026-10-24T16:11:22Z
- result: KILLED
