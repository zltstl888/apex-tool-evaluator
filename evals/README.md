# Evaluation fixtures

`evals.json` contains normal, edge, and negative behavior fixtures for manual or external agent evaluation. `trigger-evals.json` contains 20 realistic routing prompts split evenly between should-trigger and should-not-trigger cases.

Continuous integration validates both files' structure, required expectations, uniqueness, and 10:10 trigger balance. The fixtures provide a portable, inspectable contract that can be run in a compatible model or agent harness. See [`../EVALUATION.md`](../EVALUATION.md) for the public evaluation model and worked example.
