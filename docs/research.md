# Research notes

The starter uses differential testing (reference versus a slower oracle) and
population-based evaluation, two practical signals for generated programming
problems. JSON is preferred over bespoke parsers for an MVP because it supports
nested cases and can be consumed by Python, JavaScript, and judge adapters.

Next experiments: mutation-based case generation, calibrated human-solve
priors, resource limits beyond wall time (memory/CPU), and a language-neutral
runner protocol. Scores should be tracked by problem family to avoid rewarding
trivial variations of the same algorithm.
