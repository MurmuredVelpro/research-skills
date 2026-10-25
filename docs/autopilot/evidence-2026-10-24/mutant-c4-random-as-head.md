# Mutant — mutant-c4-random-as-head

- tested commit: eced80c47145e624d06bc3bd330226fcb93cb3eb
- HEAD: c55bf35f07847b2b99e72de3e991f018995f519e
- workdir: /home/ubuntu/jason/research/research-skills
- sandbox: bwrap
- started: 2026-10-24T15:12:52Z
- recorded by sha256: 332bc6db1a13f5d6dd7196c8a7c8059e8b9e9905950e145dae93dbad3ea23970
- policy: {"record_paths":{"evidence_dir":"docs/autopilot/evidence-2026-10-24","run_record":"docs/autopilot/runs/2026-10-24-six-skill-takeoff.md"},"write_dirs":["scholar-slides/node_modules","paper-slide-deck/scripts/node_modules"],"version":1,"sandbox":"bwrap","deny_network":true,"deny_paths":[],"read_paths":["/usr","/usr/bin","/bin","/usr/sbin","/sbin","/usr/lib","/lib","/usr/lib64","/lib64","/System/Library","/Library/Apple","/private/var/db/dyld","/private/etc","/etc","/dev","/home/ubuntu/jason/research/.autopilot-deps"],"env":["PLAYWRIGHT_BROWSERS_PATH"]}
- helper inventory sha256: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- helper reference: takeoff pin (AUTOPILOT_HELPER_PIN)
- frozen controls sha256: dbe2a67db3367ff94eef8e98b42979e67e0427d12669034631bc4c2762aed1bc
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
- failure signature: ^FAILED tests/test_screen_sample\.py::TestSelectTrial::test_random_is_not_the_prefix_and_reaches_the_tail\b; expected exit: 1
- mutated files: lit-search/src/litsearch/sampling.py
- patch sha256: 6d9eddf134f64fa6f24aa8c35f6f155761bdf3d12a6c86f5db177b6457ce395e

```diff
diff --git a/lit-search/src/litsearch/sampling.py b/lit-search/src/litsearch/sampling.py
index 9baaf6c..f42c902 100644
--- a/lit-search/src/litsearch/sampling.py
+++ b/lit-search/src/litsearch/sampling.py
@@ -30,7 +30,7 @@ def select_trial(records: Sequence[T], limit: int | None, method: str, seed: int
             # 没有 --limit 就是全量，「随机抽全部」没有意义，更可能是忘了写 --limit
             raise SampleError("--sample random 必须配合 --limit N 使用")
         return list(records)
-    if method == "head" or limit >= len(records):
+    if method in ("head", "random") or limit >= len(records):
         return list(records[:limit])
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
................                                                         [100%]
16 passed in 0.99s

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
..FF......F.....                                                         [100%]
=================================== FAILURES ===================================
_________________ TestSelectTrial.test_random_differs_by_seed __________________

self = <tests.test_screen_sample.TestSelectTrial object at 0x7ef440ddff50>

    def test_random_differs_by_seed(self):
>       assert select_trial(CORPUS, 10, "random", 7) != select_trial(CORPUS, 10, "random", 8)
E       AssertionError: assert [0, 1, 2, 3, 4, 5, ...] != [0, 1, 2, 3, 4, 5, ...]
E        +  where [0, 1, 2, 3, 4, 5, ...] = select_trial([0, 1, 2, 3, 4, 5, ...], 10, 'random', 7)
E        +  and   [0, 1, 2, 3, 4, 5, ...] = select_trial([0, 1, 2, 3, 4, 5, ...], 10, 'random', 8)

tests/test_screen_sample.py:41: AssertionError
______ TestSelectTrial.test_random_is_not_the_prefix_and_reaches_the_tail ______

self = <tests.test_screen_sample.TestSelectTrial object at 0x7ef440ddff80>

    def test_random_is_not_the_prefix_and_reaches_the_tail(self):
        chosen = select_trial(CORPUS, 10, "random", 7)
>       assert chosen != CORPUS[:10]
E       assert [0, 1, 2, 3, 4, 5, ...] != [0, 1, 2, 3, 4, 5, ...]

tests/test_screen_sample.py:45: AssertionError
_ TestScreenSampleCli.test_random_trial_screens_the_seeded_sample_and_records_it _

self = <tests.test_screen_sample.TestScreenSampleCli object at 0x7ef440dde9f0>
seeded_run = <litsearch.run.Run object at 0x7ef440dd56d0>
topic_path = PosixPath('/tmp/autopilot-run.xeVnri/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/topic.yaml')
runs_root = PosixPath('/tmp/autopilot-run.xeVnri/mutant-tmp/pytest-of-ubuntu/pytest-0/test_random_trial_screens_the_0/runs')
fake_llm = <tests.test_cli._FakeClient object at 0x7ef440dcc8c0>

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
>       assert list(trial["decisions"]) == [keys[1]]
E       AssertionError: assert ['doi:10.1038...-022-01875-5'] == ['doi:10.1007...-021-06816-8']
E
E         At index 0 diff: 'doi:10.1038/s41597-022-01875-5' != 'doi:10.1007/s00521-021-06816-8'
E         Use -v to get more diff

tests/test_screen_sample.py:106: AssertionError
=========================== short test summary info ============================
FAILED tests/test_screen_sample.py::TestSelectTrial::test_random_differs_by_seed
FAILED tests/test_screen_sample.py::TestSelectTrial::test_random_is_not_the_prefix_and_reaches_the_tail
FAILED tests/test_screen_sample.py::TestScreenSampleCli::test_random_trial_screens_the_seeded_sample_and_records_it
3 failed, 13 passed in 1.49s

```
- finished: 2026-10-24T15:13:01Z
- result: KILLED
