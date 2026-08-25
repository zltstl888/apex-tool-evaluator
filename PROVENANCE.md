# Provenance

## Origin

APEX Tool Evaluator was developed from APEX AI's internal practice for evaluating agent skills, MCP servers, APIs, CLIs, SaaS products, repositories, and model or dataset assets before adoption.

The public edition is a clean rewrite designed for cross-client use. It does not copy the internal installation, customer names, local paths, credentials, tool inventory, production status, or dated operating facts.

## Human and AI contributions

AI systems assisted with drafting, restructuring, and test-case generation. Humans determined the problem, selected the workflow, edited the instructions, set the safety boundaries, reviewed the public scope, and authored or approved the validation criteria.

## Authoring tools

The public edition was structured and tested with Anthropic's Apache-2.0-licensed [`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/2a40fd2e7c52207aa903bd33fc4c65716126966e/plugins/skill-creator/skills/skill-creator) authoring workflow. Publication review cross-checked upstream commit `2a40fd2e7c52207aa903bd33fc4c65716126966e` on 2026-08-25.

The local authoring snapshot had `SKILL.md` SHA-256 `053e01e040e4fa3bae41bd7a23bd51173c06ca83603d10fe4cad1858435cfcf6` and a sorted per-file manifest SHA-256 of `5f0bba9e2be180aac3106d40ef4aea620d1a234da6963b08c9670af7af4bd015`. Its original upstream commit was not retained, so the cross-check commit is recorded separately rather than presented as the snapshot's source revision.

No text or source code from that authoring workflow is bundled in this repository. It is not required at runtime.

## Third-party material

No third-party Skill text, source code, brand asset, customer material, credential, or proprietary dataset is intentionally bundled. Product and platform names may appear only as examples or interoperability references. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Release rule

Before publication, run the reference validator, project linter, and tests; review every dependency or copied fragment; and perform a human privacy and license review. A successful test does not itself authorize publication.
