# Contributing

Contributions should improve a demonstrated evaluation problem while keeping the Skill portable and evidence-led.

## Before opening a pull request

1. Explain the failure mode or decision gap the change addresses.
2. Add or update a normal, edge, or negative eval when behavior changes.
3. Keep current facts out of long-lived instructions; point to the live source that should be checked.
4. Do not add customer data, credentials, private URLs, internal paths, or unlicensed material.
5. Document third-party material in `THIRD_PARTY_NOTICES.md`.
6. Run:

```bash
python3 -m pip install \
  "git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref"
skills-ref validate "$PWD"
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

By submitting a contribution, you represent that you have the right to submit it under the repository license.
