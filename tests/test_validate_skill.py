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
        VALIDATOR.validate_trigger_evals()
        VALIDATOR.validate_version_consistency()
        VALIDATOR.validate_public_boundary()

    def test_evals_include_a_negative_case(self) -> None:
        data = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
        prompts = "\n".join(item["prompt"] for item in data["evals"])
        self.assertIn("laptop stands", prompts)

    def test_eval_categories_cover_normal_edge_and_negative(self) -> None:
        data = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
        categories = [item["category"] for item in data["evals"]]
        self.assertGreaterEqual(categories.count("normal"), 3)
        self.assertGreaterEqual(categories.count("edge"), 1)
        self.assertGreaterEqual(categories.count("negative"), 1)

    def test_trigger_evals_have_ten_positive_and_ten_negative_cases(self) -> None:
        data = json.loads(
            (ROOT / "evals/trigger-evals.json").read_text(encoding="utf-8")
        )
        labels = [item["should_trigger"] for item in data]
        self.assertEqual(len(data), 20)
        self.assertEqual(labels.count(True), 10)
        self.assertEqual(labels.count(False), 10)

    def test_skill_has_no_absolute_home_path(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for _, pattern in VALIDATOR.PUBLIC_BOUNDARY_PATTERNS:
            self.assertIsNone(pattern.search(text))

    def test_missing_required_file_fails(self) -> None:
        (self.fixture_root / "NOTICE").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required files: NOTICE"):
            VALIDATOR.validate_required_files(self.fixture_root)

    def test_missing_evaluation_guide_fails(self) -> None:
        (self.fixture_root / "EVALUATION.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required files: EVALUATION.md"):
            VALIDATOR.validate_required_files(self.fixture_root)

    def test_missing_trigger_evals_fails(self) -> None:
        (self.fixture_root / "evals/trigger-evals.json").unlink()
        with self.assertRaisesRegex(
            ValueError, "Missing required files: evals/trigger-evals.json"
        ):
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

    def test_missing_eval_category_fails(self) -> None:
        eval_path = self.fixture_root / "evals/evals.json"
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        del data["evals"][0]["category"]
        eval_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing category"):
            VALIDATOR.validate_evals(self.fixture_root)

    def test_duplicate_trigger_query_fails(self) -> None:
        eval_path = self.fixture_root / "evals/trigger-evals.json"
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        data[1]["query"] = data[0]["query"]
        eval_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Trigger eval queries must be unique"):
            VALIDATOR.validate_trigger_evals(self.fixture_root)

    def test_unbalanced_trigger_evals_fail(self) -> None:
        eval_path = self.fixture_root / "evals/trigger-evals.json"
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        data[10]["should_trigger"] = True
        eval_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "10:10 should-trigger balance"):
            VALIDATOR.validate_trigger_evals(self.fixture_root)

    def test_non_boolean_trigger_label_fails(self) -> None:
        eval_path = self.fixture_root / "evals/trigger-evals.json"
        data = json.loads(eval_path.read_text(encoding="utf-8"))
        data[0]["should_trigger"] = "yes"
        eval_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "should_trigger must be a boolean"):
            VALIDATOR.validate_trigger_evals(self.fixture_root)

    def test_citation_version_mismatch_fails(self) -> None:
        citation_path = self.fixture_root / "CITATION.cff"
        text = citation_path.read_text(encoding="utf-8")
        citation_path.write_text(
            text.replace('version: "0.1.3"', 'version: "9.9.9"', 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "CITATION.cff version must match"):
            VALIDATOR.validate_version_consistency(self.fixture_root)

    def test_readme_release_version_mismatch_fails(self) -> None:
        readme_path = self.fixture_root / "README.md"
        text = readme_path.read_text(encoding="utf-8")
        readme_path.write_text(text.replace("v0.1.3", "v9.9.9"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "README release references must match"):
            VALIDATOR.validate_version_consistency(self.fixture_root)

    def test_readme_zip_release_asset_fails(self) -> None:
        readme_path = self.fixture_root / "README.md"
        text = readme_path.read_text(encoding="utf-8")
        readme_path.write_text(
            text.replace(
                "apex-tool-evaluator-v0.1.3.skill",
                "apex-tool-evaluator-v0.1.3.zip",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "versioned \\.skill release asset"):
            VALIDATOR.validate_version_consistency(self.fixture_root)

    def test_latest_changelog_version_mismatch_fails(self) -> None:
        changelog_path = self.fixture_root / "CHANGELOG.md"
        text = changelog_path.read_text(encoding="utf-8")
        changelog_path.write_text(
            text.replace("## 0.1.3 - 2026-08-29", "## 9.9.9 - 2026-08-29", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "CHANGELOG latest release must match"):
            VALIDATOR.validate_version_consistency(self.fixture_root)

    def test_social_preview_sha_mismatch_fails(self) -> None:
        preview_path = self.fixture_root / "SOCIAL_PREVIEW.md"
        text = preview_path.read_text(encoding="utf-8")
        preview_path.write_text(
            text.replace(VALIDATOR.SOCIAL_PREVIEW_SHA, "0" * 64, 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "SOCIAL_PREVIEW.md SHA-256"):
            VALIDATOR.validate_version_consistency(self.fixture_root)

    def test_missing_citation_file_fails(self) -> None:
        (self.fixture_root / "CITATION.cff").unlink()
        with self.assertRaisesRegex(ValueError, "Missing required files: CITATION.cff"):
            VALIDATOR.validate_required_files(self.fixture_root)

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
