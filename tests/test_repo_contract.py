r"""仓库级契约测试（跨 skill 共享层）。

锁 docs/citation-integrity-core.md 的防漂移约定（第三轮评审 XC-02/04、
RP-15）：变体注册表的每一行都指向真实存在的变体文件、每个变体带
Derived-from 标记、共享旗标分类完整、README 的数量声明与注册表一致。
"""

from re import findall
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "docs" / "citation-integrity-core.md"


def registry_rows() -> list[tuple[str, str]]:
    """(skill, variant_file) — 核心注册表数据行。"""
    rows: list[tuple[str, str]] = []
    in_registry = False
    for line in CORE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Variant registry"):
            in_registry = True
            continue
        if in_registry and line.startswith("## "):
            break
        if in_registry and line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 2 and not set(cells[0]) <= {"-", " ", ":"} and cells[0] != "Skill":
                variant = cells[1].replace("`", "").split()[0]  # 「`SKILL.md` Step 6.5」→ SKILL.md
                rows.append((cells[0], variant))
    return rows


class VariantRegistryContract(unittest.TestCase):
    def test_registry_rows_exist(self):
        self.assertGreaterEqual(len(registry_rows()), 5, "注册表应列出全部写作/渲染 skill")

    def test_every_variant_file_exists_and_declares_derivation(self):
        for skill, variant in registry_rows():
            with self.subTest(skill=skill):
                path = ROOT / skill / variant
                self.assertTrue(path.exists(), f"{skill}/{variant} 不存在")
                text = path.read_text(encoding="utf-8")
                self.assertIn(
                    "citation-integrity-core",
                    text,
                    f"{skill}/{variant} 缺 Derived-from 标记（防漂移约定）",
                )

    def test_readme_count_matches_the_registry(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        match = None
        import re

        match = re.search(r"All (\w+) writing/rendering skills", readme)
        self.assertIsNotNone(match, "README 应声明共享核心覆盖的 skill 数")
        words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        self.assertEqual(words[match.group(1)], len(registry_rows()))


class FlagTaxonomyContract(unittest.TestCase):
    def test_shared_taxonomy_lists_every_flag_the_gates_scan(self):
        text = CORE.read_text(encoding="utf-8")
        for flag in ("[UNVERIFIED", "[PENDING", "[MISSING", "[CHECK]", "[REDRAWN]"):
            with self.subTest(flag=flag):
                self.assertIn(flag, text)


if __name__ == "__main__":
    unittest.main()
