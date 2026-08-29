# Evaluation

APEX Tool Evaluator ships with public evaluation assets so its intended behavior, trigger boundary, and decision quality can be inspected and reproduced. The fixtures focus on the Skill's practical value: turning an uncertain tool-adoption question into a sourced verdict, a clear risk boundary, and a safe next step.

## Evaluation layers

| Layer | Public asset | What it exercises |
|---|---|---|
| Behavior | [`evals/evals.json`](evals/evals.json) | Normal, high-risk edge, and out-of-scope decisions with explicit expectations |
| Triggering | [`evals/trigger-evals.json`](evals/trigger-evals.json) | 20 realistic prompts balanced between 10 should-trigger and 10 should-not-trigger cases |
| Worked evaluation | [`examples/evidence-backed-evaluation.md`](examples/evidence-backed-evaluation.md) | A dated evaluation of a real public tool using primary sources and an isolated runtime check |

Together, these layers test whether the Skill is invoked for the right decisions and whether its output preserves the evidence, authority, and rollback boundaries that make a recommendation useful in real work.

## Behavior fixtures

The five behavior fixtures cover the core decision contract:

- a high-permission MCP candidate evaluated without granting OAuth access;
- a SaaS replacement claim that requires live pricing and privacy evidence;
- overlapping Agent Skills inventoried without unauthorized cleanup;
- a browser extension whose permissions and missing security evidence override popularity;
- an ordinary consumer comparison that should stay outside this enterprise workflow.

Each fixture includes a realistic prompt, expected decision shape, and concrete expectations. The expectations check the properties that matter operationally: one allowed verdict, a named current baseline, primary-source discipline, explicit P0 risk handling, no invented facts, and no unauthorized write action.

## Trigger fixtures

The trigger set is intentionally balanced:

- **10 should trigger:** adoption, replacement, permission, privacy, license, cost, maintenance, integration, or bounded-test decisions involving AI and developer tools;
- **10 should not trigger:** adjacent requests such as operating an already-approved tool, debugging an existing integration, summarizing supplied material, reviewing application code, or comparing consumer products.

The negative cases are close neighbors rather than unrelated prompts. This makes the set useful for checking both discovery and restraint: the Skill should be available when a workflow decision needs evidence, and stay out of the way when the user needs direct execution or a different specialist workflow.

## Real tool-evaluation example

The worked `skills` CLI example demonstrates the complete protocol on a public candidate. It records a dated decision context, checks the official repository and package metadata, runs a project-local smoke test against an explicit Skill tag, classifies license and filesystem risks, and returns `auxiliary_candidate` with a reversible adoption boundary.

That example shows the value of the protocol in a concrete decision: installation convenience is recognized, while source review, permission review, version pinning, and a transparent fallback remain intact.

## Run the public checks

```bash
skills-ref validate "$PWD"
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

The repository validator checks package structure, release-version consistency, behavior-fixture coverage, trigger-fixture uniqueness and 10:10 balance, and limited accidental-publication indicators. Unit tests exercise both passing and failing validator paths.

When running the prompts through an agent harness, record the model, runtime, date, sampling settings, and run count with the results. This keeps published behavior evidence interpretable and repeatable as models and runtimes evolve.

## Success criteria

A successful evaluation run should show that the Skill:

1. triggers for consequential AI or developer-tool adoption decisions and avoids adjacent execution-only requests;
2. returns exactly one allowed verdict at the depth justified by available evidence and risk;
3. compares the candidate with the current workflow instead of evaluating it in isolation;
4. treats primary sources and reproducible tests as adoption evidence;
5. blocks unsafe or unlicensed paths before scorecard arithmetic;
6. proposes a bounded, reversible next step without implying authority the user did not grant.

Contributions that expose a new failure mode are welcome when they add a public or synthetic fixture and preserve the project's privacy, provenance, licensing, and safety boundaries.
