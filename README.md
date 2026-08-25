# APEX Tool Evaluator

A portable Agent Skill for deciding whether an AI tool should be tested, adopted, watched, or rejected.

It evaluates agent skills, MCP servers, APIs, CLIs, SaaS products, browser extensions, GitHub repositories, models, and datasets against a real workflow, primary evidence, safety boundaries, license terms, cost, and testability.

## Why it exists

Tool discovery is easy. Tool adoption is expensive.

An impressive demo can still be duplicative, unlicensed, unsafe for company data, costly at scale, or impossible to operate reliably. This skill turns a recommendation into an auditable decision with explicit evidence, risk gates, a bounded test, and one of seven verdicts.

## Install

Clone the tagged release directly into a skill directory supported by your agent client. Stable installations are deliberately pinned to a version instead of following the development branch.

Project-local Agent Skills convention:

```bash
mkdir -p .agents/skills
git clone --branch v0.1.0 --depth 1 https://github.com/zltstl888/apex-tool-evaluator.git \
  .agents/skills/apex-tool-evaluator
```

Codex user-level installation:

```bash
mkdir -p ~/.codex/skills
git clone --branch v0.1.0 --depth 1 https://github.com/zltstl888/apex-tool-evaluator.git \
  ~/.codex/skills/apex-tool-evaluator
```

The repository follows the Agent Skills directory convention. The required entry point is [`SKILL.md`](SKILL.md).

## Example prompt

```text
We are considering a GitHub-hosted MCP server for an internal support workflow.
It asks for read/write access to Slack and Google Drive. Compare it with our
current read-only connector, verify the license and maintenance status, and
propose a synthetic-data test. Do not install or authorize anything.
```

The skill returns:

- the workflow and current baseline;
- primary evidence and missing facts;
- a 0-5 evidence-backed scorecard;
- P0 blockers and bounded risks;
- a safe test with cost and rollback;
- a single adoption verdict.

When core identifiers are missing, it intentionally returns a short intake decision instead of filling a large scorecard with guessed zeroes. Full reports are reserved for identifiable or high-risk decisions.

## Verdicts

`mainline_candidate`, `auxiliary_candidate`, `test_first`, `observe_only`, `reference_only`, `shelved_pending_authorization`, or `reject`.

No verdict authorizes installation, payment, authentication, production changes, or access grants by itself.

## Repository layout

```text
SKILL.md                         Agent instructions
references/evaluation-form.md  Durable decision template
evals/evals.json               Normal, edge, and negative cases
scripts/validate_skill.py      Structure and public-boundary linter
tests/test_validate_skill.py   Validator regression tests
PROVENANCE.md                  Authorship and origin record
THIRD_PARTY_NOTICES.md         External names and bundled-code boundary
SECURITY.md                    Vulnerability reporting guidance
```

## 中文说明

这是一个面向企业 AI 工具治理的通用 Skill。它不会因为工具“热门”就建议接入，而是先回答五个问题：解决什么真实流程、是否重复、证据是否可信、数据和权限是否安全、能否用合成数据小范围验证。

公开版本不包含客户资料、本机路径、账号凭证、内部工具库存或生产状态。

## Development

Validation tooling requires Python 3.12 or later.

```bash
python3 -m pip install \
  "git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref"
skills-ref validate "$PWD"
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

The `main` branch is the development channel. Contributors who intentionally want that channel can clone it without `--branch`; stable users should install a tagged release and move to a newer tag only after reviewing its release notes.

The linter catches a limited set of accidental-publication indicators. It is not a complete secret scanner, privacy audit, or substitute for human review.

## Publisher

Published by [`@zltstl888`](https://github.com/zltstl888) under the APEX AI project name. APEX AI is the project and brand name used by the repository owner for this work.

## Provenance and AI assistance

This project was developed from APEX AI's operational tool-governance practice. Drafting was AI-assisted; scope, structure, edits, examples, safety boundaries, and tests were selected and reviewed by humans. See [`PROVENANCE.md`](PROVENANCE.md).

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
