# Mutant — mutant-c4-resume-guard-r2

- tested commit: a16bf94a9fae9aaf216e10ae96d3d774e720c092
- HEAD: a16bf94a9fae9aaf216e10ae96d3d774e720c092
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:25:42Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: 069c706f400a5f14b308502ef5ccbc3e38e0cdeb4188736dc34d418d9188d6ee
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
- failure signature: ^FAILED tests/test_screen_sample\.py::test_resume_with_random_is_refused_for_its_own_reason\b; expected exit: 1
- mutated files: lit-search/src/litsearch/cli.py
- patch sha256: 79781aa0b2018558fb49adc0fe5da97be288430db49b08ff2df233df7d7084ac

```diff
diff --git a/lit-search/src/litsearch/cli.py b/lit-search/src/litsearch/cli.py
index a472fae..8ccd3d0 100644
--- a/lit-search/src/litsearch/cli.py
+++ b/lit-search/src/litsearch/cli.py
@@ -951,7 +951,7 @@ def screen_command(
     records = [CanonicalRecord.model_validate(row) for row in run_dir.read_jsonl("corpus.jsonl")]
     records = [item for item in records if item.window_status == WindowStatus.IN_WINDOW]
     try:
-        if resume and sample == "random":
+        if False:
             # 续跑补的是上一轮缺的判定；试跑样本换了种子就是另一批记录，混进去无从解释
             raise SampleError("--resume 不能与 --sample random 同用：要换样本就重新试跑")
         if seed is not None and sample != "random":

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
17 passed in 1.07s

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
................F                                                        [100%]
=================================== FAILURES ===================================
____________ test_resume_with_random_is_refused_for_its_own_reason _____________

seeded_run = <litsearch.run.Run object at 0x7e3813b23ad0>
topic_path = PosixPath('/tmp/autopilot-run.v6Wpq6/mutant-tmp/pytest-of-ubuntu/pytest-0/test_resume_with_random_is_ref0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.v6Wpq6/mutant-tmp/pytest-of-ubuntu/pytest-0/test_resume_with_random_is_ref0/runs')

    def test_resume_with_random_is_refused_for_its_own_reason(
        seeded_run, topic_path, runs_root  # noqa: F811
    ):
        # 没有上一轮时续跑本来也会以 2 退出；这里要看到的是 random 冲突本身被点名
        extra = ("--limit", "1", "--sample", "random", "--resume")
        args = TestScreenSampleCli._cmd(topic_path, runs_root, *extra)
        result = runner.invoke(app, args)
        assert result.exit_code == 2, result.output
>       assert "--resume 不能与 --sample random 同用" in result.output
E       AssertionError: assert '--resume 不能与 --sample random 同用' in '该 run 还没有筛选轮次，无从续跑。\n'
E        +  where '该 run 还没有筛选轮次，无从续跑。\n' = <Result SystemExit(2)>.output

tests/test_screen_sample.py:185: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::test_resume_with_random_is_refused_for_its_own_reason
1 failed, 16 passed in 1.20s

```
- finished: 2026-10-24T15:25:51Z
- result: KILLED
