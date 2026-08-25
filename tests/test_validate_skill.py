from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skill", ROOT / "scripts/validate_skill.py"
)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PublicSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.fixture_root = Path(self.temporary_directory.name) / "apex-tool-evaluator"
        shutil.copytree(ROOT, self.fixture_root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_package_validator_passes(self) -> None:
        VALIDATOR.validate_required_files()
        VALIDATOR.validate_skill()
        VALIDATOR.validate_evals()
        VALIDATOR.validate_public_boundary()

    def test_evals_include_a_negative_case(self) -> None:
        data = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
        prompts = "\n".join(item["prompt"] for item in data["evals"])
        self.assertIn("laptop stands", prompts)

    def test_skill_has_no_absolute_home_path(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for _, pattern in VALIDATOR.PUBLIC_BOUNDARY_PATTERNS:
            self.assertIsNone(pattern.search(text))

    def test_missing_required_file_fails(self) -> None:
        (self.fixture_root / "NOTICE").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required files: NOTICE"):
            VALIDATOR.validate_required_files(self.fixture_root)

    def test_bad_frontmatter_name_fails(self) -> None:
        skill_path = self.fixture_root / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        skill_path.write_text(
            text.replace("name: apex-tool-evaluator", "name: Apex Tool Evaluator", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "Skill name must be"):
            VALIDATOR.validate_skill(self.fixture_root)

    def test_duplicate_eval_id_fails(self) -> None:
        eval_path = self.fixture_root / "evals/evals.json"
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        data["evals"][1]["id"] = data["evals"][0]["id"]
        eval_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Eval IDs must be unique"):
            VALIDATOR.validate_evals(self.fixture_root)

    def test_windows_user_path_fails(self) -> None:
        private_path = "C:" + "\\" + "Users" + "\\" + "example" + "\\" + "notes.txt"
        (self.fixture_root / "accidental-path.txt").write_text(private_path, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Windows user path"):
            VALIDATOR.validate_public_boundary(self.fixture_root)

    def test_credential_assignment_fails(self) -> None:
        credential = "api" + "_key" + "=" + "examplevalue12345"
        (self.fixture_root / "accidental-secret.txt").write_text(credential, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "credential assignment"):
            VALIDATOR.validate_public_boundary(self.fixture_root)

    def test_bytecode_cache_fails(self) -> None:
        cache = self.fixture_root / "scripts" / "__pycache__"
        cache.mkdir()
        (cache / "validator.pyc").write_bytes(b"compiled-cache")
        with self.assertRaisesRegex(ValueError, "cache or bytecode"):
            VALIDATOR.validate_public_boundary(self.fixture_root)

    def test_binary_file_fails(self) -> None:
        (self.fixture_root / "unexpected.bin").write_bytes(b"public\x00private")
        with self.assertRaisesRegex(ValueError, "binary file is not allowed"):
            VALIDATOR.validate_public_boundary(self.fixture_root)


if __name__ == "__main__":
    unittest.main()
