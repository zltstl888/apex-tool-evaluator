# Compact examples

These examples show the expected decision shape. They do not make factual claims about real products or replace live primary-source verification.

## 1. High-permission connector with missing evidence

**Input:** An unnamed open-source MCP server requests read/write access to Slack and Google Drive for an internal support workflow. Installation and authorization are not allowed.

**Expected decision:** `shelved_pending_authorization`

- Treat the missing candidate identity, license, security evidence, and exact OAuth scopes as blockers.
- Preserve the current read-only connector.
- Do not assign candidate scores from absent evidence.
- Verify primary sources before proposing a local mock with synthetic data.

## 2. Overlapping Agent Skills

**Input:** A team wants to clean up several coding-agent Skills but has not authorized deletion or disabling.

**Expected decision:** `shelved_pending_authorization` until the inventory and cleanup authority are known. Identifiable candidates can move to `test_first` after the read-only inventory.

- Inventory first and group Skills by workflow.
- Separate mainline, auxiliary, fallback, and reference roles.
- Preserve cross-runtime copies until their provenance and packaging purpose are known.
- Compare candidates with representative tasks before recommending a reversible cleanup.

## 3. Ordinary consumer comparison

**Input:** Compare two laptop stands for a home office. No company systems, integrations, or technical adoption process are involved.

**Expected response:** The Skill is not applicable.

- Do not force an enterprise scorecard onto the request.
- Ask for the two product identities or links.
- Do not invent prices, materials, dimensions, or rankings.
