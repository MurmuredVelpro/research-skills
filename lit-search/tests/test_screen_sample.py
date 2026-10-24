"""试跑取样：``--limit N --sample random --seed S``。

前缀不是抽样（learnings/2026-09-21-前缀不是抽样.md）：前 N 条是最典型的记录，
撑爆人工队列的边缘记录排在语料尾部。校准必须能抽到尾部，而且同一种子可复现。
"""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from litsearch.cli import app
from litsearch.dedupe import CanonicalRecord
from litsearch.normalize import WindowStatus
from litsearch.sampling import SampleError, sample_parameters, select_trial

from .test_cli import _FakeClient, runs_root, seeded_run, topic_path  # noqa: F401

runner = CliRunner()
CORPUS = list(range(50))


class TestSelectTrial:
    def test_head_is_the_prefix(self):
        assert select_trial(CORPUS, 10, "head", 0) == CORPUS[:10]

    def test_random_is_reproducible_for_the_same_seed(self):
        assert select_trial(CORPUS, 10, "random", 7) == select_trial(CORPUS, 10, "random", 7)

    def test_random_differs_by_seed(self):
        assert select_trial(CORPUS, 10, "random", 7) != select_trial(CORPUS, 10, "random", 8)

    def test_random_is_not_the_prefix_and_reaches_the_tail(self):
        chosen = select_trial(CORPUS, 10, "random", 7)
        assert chosen != CORPUS[:10]
        assert max(chosen) >= 25  # 抽得到语料后半段——前缀永远抽不到

    def test_random_has_no_duplicates_keeps_order_and_size(self):
        chosen = select_trial(CORPUS, 10, "random", 3)
        assert len(chosen) == 10
        assert len(set(chosen)) == 10
        assert chosen == sorted(chosen)

    def test_limit_larger_than_corpus_returns_everything(self):
        assert select_trial(CORPUS, 80, "random", 1) == CORPUS

    def test_no_limit_head_returns_everything(self):
        assert select_trial(CORPUS, None, "head", 0) == CORPUS

    def test_random_without_limit_is_refused(self):
        with pytest.raises(SampleError, match="--limit"):
            select_trial(CORPUS, None, "random", 0)

    def test_unknown_method_is_refused(self):
        with pytest.raises(SampleError, match="head / random"):
            select_trial(CORPUS, 5, "stratified", 0)

    def test_parameters_record_method_and_seed_only_for_trials(self):
        assert sample_parameters(10, "random", 7, 10) == {
            "sample": {"method": "random", "size": 10, "seed": 7}
        }
        assert sample_parameters(10, "head", 7, 10) == {"sample": {"method": "head", "size": 10}}
        assert sample_parameters(None, "head", 0, 50) == {}


class TestScreenSampleCli:
    @pytest.fixture
    def fake_llm(self, monkeypatch):
        client = _FakeClient()
        monkeypatch.setenv("LITSEARCH_LLM_API_KEY", "k-test")
        monkeypatch.setattr("litsearch.cli.build_screen_client", lambda *a, **k: client)
        return client

    @staticmethod
    def _cmd(topic_path, runs_root, *extra):  # noqa: F811
        return [
            "screen", "t", "--topic", str(topic_path), "--runs-root", str(runs_root),
            "--concurrency", "1", *extra,
        ]

    @staticmethod
    def _in_window_keys(run) -> list[str]:
        records = [CanonicalRecord.model_validate(row) for row in run.read_jsonl("corpus.jsonl")]
        return [item.key for item in records if item.window_status == WindowStatus.IN_WINDOW]

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
        assert trial["parameters"]["sample"] == {"method": "random", "size": 1, "seed": 5}

    def test_head_trial_keeps_the_prefix(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        keys = self._in_window_keys(seeded_run)
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--limit", "1"))
        assert result.exit_code == 0, result.output
        trial = json.loads((seeded_run.root / "screening_trial.json").read_text())
        assert list(trial["decisions"]) == [keys[0]]
        assert trial["parameters"]["sample"] == {"method": "head", "size": 1}

    def test_random_without_limit_exits_2_and_writes_nothing(
        self, seeded_run, topic_path, runs_root, fake_llm  # noqa: F811
    ):
        result = runner.invoke(app, self._cmd(topic_path, runs_root, "--sample", "random"))
        assert result.exit_code == 2, result.output
        assert "--limit" in result.output
        assert not (seeded_run.root / "screening_trial.json").exists()
        assert not list(seeded_run.root.glob("screening_round_*.json"))
