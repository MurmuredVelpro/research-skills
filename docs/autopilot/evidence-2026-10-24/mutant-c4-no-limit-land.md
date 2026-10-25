# Mutant — mutant-c4-no-limit-land

- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- HEAD: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:45:37Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: ad9a7d04670998240136267ab290a76a2d4233d5549f32558700912c3642be49
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestSelectTrial::test_random_without_limit_is_refused\b; expected exit: 1
- mutated files: lit-search/src/litsearch/sampling.py
- patch sha256: 48873c99ff8c0e2fb538610ca125fa4e4e079e52c0207925fffff9c8379ddd9a

```diff
diff --git a/lit-search/src/litsearch/sampling.py b/lit-search/src/litsearch/sampling.py
index 9baaf6c..728ec2e 100644
--- a/lit-search/src/litsearch/sampling.py
+++ b/lit-search/src/litsearch/sampling.py
@@ -28,7 +28,7 @@ def select_trial(records: Sequence[T], limit: int | None, method: str, seed: int
     if not limit:
         if method == "random":
             # 没有 --limit 就是全量，「随机抽全部」没有意义，更可能是忘了写 --limit
-            raise SampleError("--sample random 必须配合 --limit N 使用")
+            pass
         return list(records)
     if method == "head" or limit >= len(records):
         return list(records[:limit])

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
17 passed in 1.13s

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
.......F......F..                                                        [100%]
=================================== FAILURES ===================================
_____________ TestSelectTrial.test_random_without_limit_is_refused _____________

self = <tests.test_screen_sample.TestSelectTrial object at 0x703a59be7110>

    def test_random_without_limit_is_refused(self):
>       with pytest.raises(SampleError, match="--limit"):
E       Failed: DID NOT RAISE SampleError

tests/test_screen_sample.py:61: Failed
___ TestScreenSampleCli.test_random_without_limit_exits_2_and_writes_nothing ___

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x703a59be55b0>
seeded_run = <litsearch.run.Run object at 0x703a59bd5130>
topic_path = PosixPath('/tmp/autopilot-run.1VnOjj/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.1VnOjj/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x703a58f4e120>

    def test_random_without_limit_exits_2_and_writes_nothing(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--sample", "random"))
>       assert result.exit_code == 2, result.output
E       AssertionError:
E         2 个请求，预计成本 $0.00（粗估）
E
E         实际用量：缓存命中 20 / 未命中 40 / 输出 10
E         实际成本：$0.0000
E
E         判定                      数量
E         --------------------------
E         纳入                       2
E         排除                       0
E         待人工裁定                    0
E
E         判定 → /tmp/autopilot-run.1VnOjj/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/runs/t/20261024T154545Z/screening_round_1.json
E         待人工裁定 0 条 → /tmp/autopilot-run.1VnOjj/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_without_limit_exit0/runs/t/20261024T154545Z/human_queue.csv
E
E       assert 0 == 2
E        +  where 0 = <Result okay>.exit_code

tests/test_screen_sample.py:144: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestSelectTrial::test_random_without_limit_is_refused
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_random_without_limit_exits_2_and_writes_nothing
2 failed, 15 passed in 1.23s

```
- finished: 2026-10-24T15:45:46Z
- result: KILLED
