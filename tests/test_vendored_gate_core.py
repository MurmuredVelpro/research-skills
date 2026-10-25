"""共享门禁核心 integrity_gate.py 的副本一致性。

skill 目录被单独复制到 ~/.claude/skills/ 安装，不能跨目录 import，所以写作类 skill 各带一份
逐字节相同的副本（lit-search 的 vendored 模块同理，见 lit-search/tests/test_vendored_sync.py）。
改了一份忘了另一份，两个 skill 的门禁就会悄悄判出不同结论——此测试让那种漂移在 CI 变红。
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = "scripts/integrity_gate.py"
#: 携带副本的 skill，以及各自 import 它的门禁脚本
CARRIERS = {
    "research-paper": "scripts/check_paper.py",
    "research-proposal": "scripts/check_proposal.py",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VendoredGateCoreTest(unittest.TestCase):
    def test_every_carrier_has_the_core(self):
        for skill in CARRIERS:
            with self.subTest(skill=skill):
                self.assertTrue((ROOT / skill / CORE).is_file(), f"{skill}/{CORE} missing")

    def test_copies_are_byte_identical(self):
        digests = {skill: digest(ROOT / skill / CORE) for skill in CARRIERS}
        self.assertEqual(
            len(set(digests.values())), 1,
            f"integrity_gate.py copies diverged — sync them: {digests}",
        )

    def test_each_gate_imports_the_core(self):
        for skill, script in CARRIERS.items():
            with self.subTest(skill=skill):
                text = (ROOT / skill / script).read_text(encoding="utf-8")
                self.assertRegex(text, re.compile(r"^from integrity_gate import", re.M))

    def test_each_gate_uses_its_own_copy_without_shadowing(self):
        """导入后的函数必须就是本 skill 副本里的对象——本地重定义同名函数会让副本形同虚设。"""
        shared = ("split_body", "reconcile", "pattern_hits", "finish", "read_text")
        for skill, script in CARRIERS.items():
            with self.subTest(skill=skill):
                saved_path, saved_core = list(sys.path), sys.modules.pop("integrity_gate", None)
                try:
                    spec = importlib.util.spec_from_file_location(f"_gate_{skill}", ROOT / skill / script)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    core = sys.modules["integrity_gate"]
                    self.assertEqual(Path(core.__file__).resolve(), (ROOT / skill / CORE).resolve())
                    for name in shared:
                        if hasattr(module, name):
                            self.assertIs(getattr(module, name), getattr(core, name), f"{skill}: {name} shadowed")
                finally:
                    sys.path[:] = saved_path
                    sys.modules.pop("integrity_gate", None)
                    if saved_core is not None:
                        sys.modules["integrity_gate"] = saved_core


if __name__ == "__main__":
    unittest.main()
