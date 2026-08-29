# Evidence-backed evaluation: `skills` CLI

This public example shows how APEX Tool Evaluator turns current primary sources and a bounded runtime check into a decision. It is a dated snapshot, not a permanent claim about future releases.

## Verdict

`auxiliary_candidate` — the `skills` CLI can make project-local, version-pinned Agent Skill installation more repeatable, but it does not replace source review, permission review, or a trusted baseline such as a direct pinned clone.

## Decision context

- **Snapshot date:** 2026-08-29.
- **Workflow:** install a reviewed Agent Skill into an isolated project directory.
- **Current baseline:** clone a reviewed repository at an explicit tag and inspect `SKILL.md` plus bundled files before use.
- **Proposed role:** an auxiliary installer and inventory command, not a security or trust gate.
- **Authority used:** public metadata reads and a project-local synthetic smoke test; no global install, account authorization, payment, customer data, or production system.

## Primary evidence

- The official [`vercel-labs/skills`](https://github.com/vercel-labs/skills) repository identified the CLI source and MIT license.
- The [`skills` npm package](https://www.npmjs.com/package/skills) reported version `1.5.23`, MIT license, and the same repository on 2026-08-29.
- The repository's `main` branch pointed to commit `435076e78988e1e6ec40d00b0b1d76bdbbc5419a` (`v1.5.23`) when checked.
- `npx --yes skills --version` returned `1.5.23`.
- `npx --yes skills --help` documented project/global scope, agent selection, named Skill selection, copy mode, listing, updates, and removal.

These facts can change. Recheck the package and repository before relying on a later version.

## Bounded smoke test

The test used a newly created local Git repository under a temporary work directory and ran:

```bash
npx --yes skills add \
  https://github.com/zltstl888/apex-tool-evaluator/tree/v0.1.1 \
  --skill apex-tool-evaluator \
  --agent codex \
  --copy \
  --yes
npx --yes skills list --json
```

Observed result on 2026-08-29:

- the CLI resolved the explicit `v0.1.1` tag;
- it found exactly one named Skill;
- it copied the Skill into the temporary project's `.agents/skills/apex-tool-evaluator` directory;
- `skills list --json` returned that project-local installation;
- it created a project `skills-lock.json`;
- the CLI warned that Skills should be reviewed because they run with the agent's permissions.

The smoke test proved only this isolated install-and-list path. It did not test global installation, update/removal behavior, every supported agent, hostile repositories, telemetry behavior, long-term maintenance, or production use.

## Risk gates

| Risk | State | Evidence and boundary |
|---|---|---|
| License | clear for the tested CLI snapshot | Repository and npm metadata reported MIT; every installed Skill still needs its own license review. |
| Filesystem writes | bounded | The CLI wrote a project Skill directory and lockfile in the isolated test. Global scope was not used. |
| Skill trust | unverified per package | Installation does not make third-party instructions safe; review source, provenance, bundled scripts, and requested permissions first. |
| Version drift | bounded by explicit tag | The test pinned the Skill repository tag. Using `main` or an unpinned package would weaken reproducibility. |
| External authority | clear | No OAuth, account grant, payment, production change, or confidential data was used. |

## Recommendation

Keep direct tagged clone as a transparent fallback. Use the CLI as an auxiliary only when the exact repository and Skill have already passed source, license, and permission review. Prefer project-local scope and an explicit tag for the first test; inspect the resulting files and lock data before executing the Skill.

Re-evaluate after a material CLI release, a change to install scope or telemetry, a permission-related incident, or a failed pinned-install regression.
