---
name: apex-tool-evaluator
description: Evaluate AI tools, agent skills, MCP servers, APIs, CLIs, SaaS products, browser extensions, GitHub repositories, and model or dataset assets before adoption. Use whenever a user asks whether a tool is worth using, should replace an existing tool, is safe for company data, is licensed for the intended use, or should be tested, watched, or rejected.
license: Apache-2.0
compatibility: Requires access to primary product documentation and, when relevant, repository or package metadata. Run write actions only after explicit authorization.
metadata:
  author: APEX AI
  version: "0.1.0"
---

# APEX Tool Evaluator

Turn tool discovery into a defensible adoption decision. The goal is not to collect more tools; it is to improve a real workflow without adding avoidable risk, overlap, or operating cost.

## Scope and response depth

Use this Skill for decisions about AI or developer tools, agent capabilities, integrations, technical services, data/model assets, or repeatable workflows that could change an organization's operating stack.

Do not force this framework onto an ordinary consumer-product comparison, a one-step usage question, or a purchase that does not affect a technical workflow. Handle those requests directly with the appropriate product or research method.

Match the response to the decision:

- **Intake response:** when the candidate, current baseline, intended workflow, or primary source is missing, give a concise verdict, name the blocking facts, preserve the current state, and state the next safe evidence step. Do not manufacture a detailed scorecard from missing evidence.
- **Standard evaluation:** when the candidate and workflow are identifiable, provide the verdict, baseline comparison, primary evidence, material risks, and bounded next action.
- **Full evaluation:** use the complete scorecard, risk register, and test plan when the user requests a detailed report, the tool has high side effects, or the decision could affect confidential data, production, meaningful cost, or compliance.

Prefer the shortest response that preserves the decision, evidence boundary, and safe next action. Depth is justified by risk or user need, not by the existence of the template.

## Evaluation contract

1. Name the decision: what workflow could change, who uses it, what data it touches, and what authority is available.
2. Inspect the current stack before recommending a replacement. A new tool has no value if the existing path already solves the problem reliably.
3. Prefer primary evidence: official documentation and terms, source repositories, releases, package metadata, model or dataset cards, security policies, and reproducible local results.
4. Separate discovery evidence from adoption evidence. A launch post, video, directory listing, or star count can start research but cannot justify adoption by itself.
5. Fail closed on P0 risks: unclear license, secret or customer-data exposure, excessive OAuth scope, destructive defaults, unauditable writes, unresolved production instability, or an unbounded paid action.
6. Test safely before promotion. Use synthetic or public data, define success and rollback first, and keep side effects disabled unless the user explicitly authorizes them.

## Evidence ladder

Use the highest available source and identify gaps:

1. Official documentation, terms, pricing, privacy, security, release notes, and status pages.
2. Primary technical evidence: source repository, releases, tests, CI, package registry, model or dataset card.
3. Maintainer discussions and well-scoped issues or pull requests.
4. Reputable practitioner reports that link to primary evidence.
5. Discovery-only sources such as launch posts, short videos, directories, or affiliate articles.

Current facts such as price, limits, versions, maintainers, and security posture require live verification. Do not turn an old snapshot into a present-tense claim.

## Decision workflow

### 1. Define the workflow gap

Record:

- the workflow and user;
- the current mainline tool or manual process;
- the measurable problem;
- the proposed role: replacement, auxiliary, fallback, reference, or no adoption;
- data sensitivity and external side effects;
- decision owner and approval boundary.

### 2. Gather evidence

For every material claim, retain a source or test result. At minimum check:

- product purpose and deployment model;
- maintenance and release health;
- license and intended-use compatibility;
- authentication, permissions, data retention, and training policy;
- pricing, rate limits, quotas, and lock-in;
- tests, CI, failure handling, and rollback;
- overlap with the current stack.

### 3. Apply risk gates

Classify each risk as `clear`, `bounded`, `unverified`, or `blocked`:

- privacy and confidential data;
- secrets and credential storage;
- security and permission scope;
- license and commercial use;
- cost and quota exposure;
- reliability and maintenance;
- side effects and reversibility;
- compliance or regulated-domain constraints.

Any blocked P0 risk overrides the scorecard.

### 4. Score the candidate

Score each dimension from 0 to 5 and cite the evidence behind the score:

- workflow fit;
- expected efficiency or quality gain;
- adoption evidence;
- maintenance health;
- integration fit;
- portability across relevant agent or developer environments;
- data safety;
- cost clarity;
- testability and rollback.

Use the average only as a summary:

- `>= 4.0` with no P0 risk: eligible for a bounded test;
- `3.0-3.9`: auxiliary or observe;
- `< 3.0`: reject unless new evidence changes the decision.

### 5. Design a bounded test

Specify:

- synthetic or public test data;
- baseline behavior and measurement;
- exact test steps;
- success criteria;
- cost ceiling;
- permissions and writes allowed;
- rollback and cleanup;
- evidence to retain.

A successful demo is not production approval. Promotion requires a representative eval set, documented limitations, and a named review trigger.

## Verdicts

Use exactly one:

- `mainline_candidate`: may replace the current mainline after a successful eval and explicit approval;
- `auxiliary_candidate`: adds a distinct capability beside the mainline;
- `test_first`: promising, but evidence is insufficient without a bounded test;
- `observe_only`: worth monitoring, not worth integrating now;
- `reference_only`: useful ideas or documentation, but not a tool to run;
- `shelved_pending_authorization`: blocked on paid, legal, production, security, or account authority;
- `reject`: wrong fit, unsafe, unlicensed, unmaintained, duplicative, or unsupported by evidence.

## Output format

For an intake response, use:

```markdown
# Tool Evaluation: [name or unidentified candidate]

## Verdict
[one allowed verdict and one-sentence rationale]

## Current Baseline
[what remains in place and why]

## Blocking Evidence
- [missing identity, license, maintenance, permissions, price, or workflow fact]

## Next Safe Step
[read-only evidence request or bounded test design; no implied authorization]
```

Use the full structure below only for a standard or full evaluation:

```markdown
# Tool Evaluation: [name]

## Verdict
[one verdict and one-sentence rationale]

## Decision Context
- Workflow:
- Current mainline:
- Proposed role:
- Data and side effects:

## Evidence
- Primary sources checked:
- Maintenance and adoption:
- License and intended use:
- Pricing and limits:

## Scorecard
| Dimension | Score 0-5 | Evidence |
|---|---:|---|

## Risks
- P0 blockers:
- Bounded risks:
- Unverified facts:

## Test Plan
- Safe data:
- Baseline:
- Steps:
- Success criteria:
- Cost ceiling:
- Rollback:

## Recommendation
[adopt nothing yet / approve bounded test / keep watch / reject]
```

## Source-specific checks

### GitHub and packages

Check the license, recent commits and releases, contributors, issue response, tests and CI, dependency risk, security policy, install footprint, and whether the repository is a library, application, template, or agent instruction pack.

### Models and datasets

Read the model or dataset card. Check license, intended use, limitations, evaluation methodology, training or data provenance statements, runtime requirements, and whether commercial redistribution is allowed.

### MCP, apps, and plugins

List the exact tools or permissions exposed. Prefer read-only tests. Check authentication, credential storage, write capabilities, data destinations, and overlap with existing connectors.

### APIs and SaaS

Verify official pricing, rate limits, data retention, training policy, regional constraints, SDK maturity, status history, exportability, and account-deletion or exit behavior.

### Browser extensions

Treat broad page-reading permissions as high risk. Inspect the publisher and requested permissions; prefer a narrower CLI, API, or web route for confidential workflows.

## Guardrails

- Do not install, enable, delete, pay, authenticate, invite users, change production, or grant broad scopes without explicit authorization.
- Do not paste confidential data into an unapproved external service.
- Do not report stars, prices, limits, versions, or deployment state as current without live verification.
- Do not call a tool "recommended", "safer", or "faster" without evidence.
- Do not promote a one-off demo to production status.

Use [references/evaluation-form.md](references/evaluation-form.md) when a durable decision record is needed.
