# ContestForge-R design

ContestForge-R treats a contest problem as a JSON `ProblemSpec`. Solvers use a
deliberately small protocol: one JSON value is read from stdin and one JSON
value is written to stdout. This makes generated cases language-independent and
keeps verification reproducible.

The verification loop runs both a trusted reference and a brute-force oracle
with `sys.executable`, captures stderr, rejects malformed output, and enforces
a wall-clock timeout. A solver population is measured against the reference;
the difficulty score is the percentage of solvers that fail at least one case.
The reward function combines correctness, difficulty, quality, and diversity,
with correctness intentionally dominant.

For production isolation, execute untrusted code in a container or sandbox;
the subprocess timeout is a correctness guard, not a security boundary.
