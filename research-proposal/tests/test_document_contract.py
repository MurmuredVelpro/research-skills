r"""research-proposal 的文档契约测试。

沿用 medical-imaging-review 的 test_document_contract 模式（第三轮评审
XC-06）：把「文档声称的纪律」锁进 CI，漂移变红。覆盖第三轮评审的
RPROP-07/08——AI-tell 门禁此前放走自家禁用表列出的短语，占位符豁免
此前是英文专属。
"""

from re import findall, search
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def ai_tell_pattern() -> str:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = search(r'grep -nEi "([^"]*over the past[^"]*)"', text)
    assert match, "SKILL.md Phase 5 应包含 AI-tell 门禁 grep"
    return match.group(1)


class AiTellGateContract(unittest.TestCase):
    def test_gate_covers_the_banned_family_from_the_style_guide(self):
        pattern = ai_tell_pattern()
        for phrase in (
            "plays a vital role in",
            "sheds light on",
            "paves the way for",
            "the ever-evolving landscape of",
            "Over the past three decades, scholarship has",
            "Over the past few years,",
        ):
            with self.subTest(phrase=phrase):
                self.assertTrue(search(pattern, phrase, re.I), phrase)

    def test_gate_keeps_legitimate_numbered_spans_out(self):
        self.assertIsNone(
            search(ai_tell_pattern(), "over the past 5 years, enrollment grew.")
        )

    def test_reference_files_do_not_recommend_banned_openings(self):
        for relative in ("references/DOMAIN_TEMPLATES.md", "references/STRUCTURE_GUIDE.md"):
            with self.subTest(file=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIsNone(
                    search(r"over the past\s*\[timeframe\]", text, re.I),
                    "模板句不得推荐门禁禁用的开头家族",
                )


class PlaceholderExemptionContract(unittest.TestCase):
    def test_exemption_covers_the_chinese_scaffold_header_fields(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("[所属学科]", text, "豁免清单应包含中文 scaffold 表头字段")
        self.assertIn("[年月]", text)


class LinkContract(unittest.TestCase):
    def test_relative_links_in_skill_md_resolve(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        targets = findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", text)
        relative = [t for t in targets if not t.startswith(("http", "mailto"))]
        self.assertTrue(relative, "SKILL.md 应引用本地文件")
        for target in relative:
            with self.subTest(target=target):
                self.assertTrue(
                    (ROOT / target).exists(), f"失效引用：{target}"
                )


if __name__ == "__main__":
    unittest.main()
