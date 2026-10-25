# Mutant — mutant-c4-default-random-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:46:02Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: d40c80bd83b9d1bc4dc186f5bcc3cd1aab0e58c04e51aae285a60b6cbfd8d2a8
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestScreenSampleCli::test_head_trial_keeps_the_prefix\b; expected exit: 1
- mutated files: lit-search/src/litsearch/cli.py
- patch sha256: e841a9ebb96f35dfba70a324adb2041eeb19bd4c56dc05a657e13f433a0bd807

```diff
diff --git a/lit-search/src/litsearch/cli.py b/lit-search/src/litsearch/cli.py
index a472fae..5a7008b 100644
--- a/lit-search/src/litsearch/cli.py
+++ b/lit-search/src/litsearch/cli.py
@@ -901,7 +901,7 @@ def screen_command(
         None, "--limit", min=1, help="只筛 N 条（试跑用）；取哪 N 条见 --sample"
     ),
     sample: str = typer.Option(
-        "head",
+        "random",
         "--sample",
         help="试跑取样：head = 语料前 N 条；random = 按 --seed 无放回随机抽 N 条（校准用这个）",
     ),

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
17 passed in 1.28s

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
............FF...                                                        [100%]
=================================== FAILURES ===================================
_ TestScreenSampleCli.test_seed_without_random_and_resume_with_random_are_refused _

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7f6f5a9e5f70>
seeded_run = <litsearch.run.Run object at 0x7f6f5b72f440>
topic_path = PosixPath('/tmp/autopilot-run.jMPkwY/mutant-tmp/pytest-of-ubuntu/pytest-0/test_seed_without_random_and_r0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.jMPkwY/mutant-tmp/pytest-of-ubuntu/pytest-0/test_seed_without_random_and_r0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7f6f5a9dd520>

    def test_seed_without_random_and_resume_with_random_are_refused(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        for extra in (("--limit", "1", "--seed", "3"),
                      ("--limit", "1", "--sample", "random", "--resume")):
            result = runner.invoke(app, self._cmd(topic_path, runs_root, *extra))
>           assert result.exit_code == 2, (extra, result.output)
E           AssertionError: (('--limit', '1', '--seed', '3'), '
E             2 个请求，预计成本 $0.00（粗估）
E
E             实际用量：缓存命中 20 / 未命中 40 / 输出 10
E             实际成本：$0.0000
E
E             判定        ...ytest-of-ubuntu/pytest-0/test_seed_without_random_and_r0/runs/t/20261024T154610Z/screening_trial.json（不计入轮次，下游读不到它）
E             ')
E           assert 0 == 2
E            +  where 0 = <Result okay>.exit_code

tests/test_screen_sample.py:127: AssertionError
_____________ TestScreenSampleCli.test_head_trial_keeps_the_prefix _____________

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7f6f5a9e5a00>
seeded_run = <litsearch.run.Run object at 0x7f6f5a9d4560>
topic_path = PosixPath('/tmp/autopilot-run.jMPkwY/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.jMPkwY/mutant-tmp/pytest-of-ubuntu/pytest-0/test_head_trial_keeps_the_pref0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7f6f5a9e6840>

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
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_seed_without_random_and_resume_with_random_are_refused
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_head_trial_keeps_the_prefix
2 failed, 15 passed in 1.12s

```
- finished: 2026-10-24T15:46:11Z
- result: KILLED
