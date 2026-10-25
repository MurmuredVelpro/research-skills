# Mutant — mutant-c4-exit-code-land2

- tested commit: 1811dc6702f4f2148ed9b316874e5453434e6022
- HEAD: 1811dc6702f4f2148ed9b316874e5453434e6022
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T16:12:05Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 29bf74899b5f82dfc9e7017e00c65740b0a16178d4eb77b82d668bc8b43aa9d5
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestScreenSampleCli::test_random_without_limit_exits_2_and_writes_nothing\b; expected exit: 1
- mutated files: lit-search/src/litsearch/cli.py
- patch sha256: 977043f07f9877754223bddda6a79d773998e731f24931b80525d2645cc5be98

```diff
diff --git a/lit-search/src/litsearch/cli.py b/lit-search/src/litsearch/cli.py
index a472fae..218e05f 100644
--- a/lit-search/src/litsearch/cli.py
+++ b/lit-search/src/litsearch/cli.py
@@ -960,7 +960,7 @@ def screen_command(
         records = select_trial(records, limit, sample, seed)
     except SampleError as error:
         typer.secho(str(error), fg=typer.colors.RED, err=True)
-        raise typer.Exit(code=2) from error
+        raise typer.Exit(code=1) from error
     if not records:
         typer.secho("窗口内没有记录，先跑 lit harvest", fg=typer.colors.RED, err=True)
         raise typer.Exit(code=2)

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
17 passed in 1.16s

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
............F.F.F                                                        [100%]
=================================== FAILURES ===================================
_ TestScreenSampleCli.test_seed_without_random_and_resume_with_random_are_refused _

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7aca836e21b0>
seeded_run = <litsearch.run.Run object at 0x7aca83919dc0>
topic_path = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_seed_without_random_and_r0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_seed_without_random_and_r0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7aca83896d50>

    def test_seed_without_random_and_resume_with_random_are_refused(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        for extra in (("--limit", "1", "--seed", "3"),
                      ("--limit", "1", "--sample", "random", "--resume")):
            result = runner.invoke(app, self._cmd(topic_path, runs_root, *extra))
>           assert result.exit_code == 2, (extra, result.output)
E           AssertionError: (('--limit', '1', '--seed', '3'), '--seed 只对 --sample random 生效
E             ')
E           assert 1 == 2
E            +  where 1 = <Result SystemExit(1)>.exit_code

tests/test_screen_sample.py:127: AssertionError
___ TestScreenSampleCli.test_random_without_limit_exits_2_and_writes_nothing ___

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7aca836e1880>
seeded_run = <litsearch.run.Run object at 0x7aca836d8e60>
topic_path = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7aca836e1dc0>

    def test_random_without_limit_exits_2_and_writes_nothing(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--sample", "random"))
>       assert result.exit_code == 2, result.output
E       AssertionError: --sample random 必须配合 --limit N 使用
E
E       assert 1 == 2
E        +  where 1 = <Result SystemExit(1)>.exit_code

tests/test_screen_sample.py:144: AssertionError
____________ test_resume_with_random_is_refused_for_its_own_reason _____________

seeded_run = <litsearch.run.Run object at 0x7aca836da450>
topic_path = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_resume_with_random_is_ref0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.HVqdTe/mutant-tmp/pytest-of-ubuntu/pytest-0/test_resume_with_random_is_ref0/runs')

    def test_resume_with_random_is_refused_for_its_own_reason(
        seeded_run, topic_path, runs_root  # noqa: F811
    ):
        # 没有上一轮时续跑本来也会以 2 退出；这里要看到的是 random 冲突本身被点名
        extra = ("--limit", "1", "--sample", "random", "--resume")
        args = TestScreenSampleCli._cmd(topic_path, runs_root, *extra)
        result = runner.invoke(app, args)
>       assert result.exit_code == 2, result.output
E       AssertionError: --resume 不能与 --sample random 同用：要换样本就重新试跑
E
E       assert 1 == 2
E        +  where 1 = <Result SystemExit(1)>.exit_code

tests/test_screen_sample.py:184: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_seed_without_random_and_resume_with_random_are_refused
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_random_without_limit_exits_2_and_writes_nothing
FAILED tests/test_screen_sample.py::test_resume_with_random_is_refused_for_its_own_reason
3 failed, 14 passed in 1.24s

```
- finished: 2026-10-24T16:12:14Z
- result: KILLED
