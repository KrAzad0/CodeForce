"""A tiny compositional DSL for generating simple contest solvers.

This is intentionally small. It models a solver as a sequence of typed-ish
transformations rather than trying to discover arbitrary algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


Transform = Callable[[Any], Any]


@dataclass(frozen=True)
class Pipe:
    steps: tuple[Transform, ...] = ()

    def then(self, fn: Transform) -> "Pipe":
        return Pipe(self.steps + (fn,))

    def run(self, value: Any) -> Any:
        for fn in self.steps:
            value = fn(value)
        return value


def strip() -> Transform:
    return lambda x: x.strip()


def lines() -> Transform:
    return lambda x: x.splitlines()


def split(sep: str | None = None) -> Transform:
    return lambda x: x.split(sep)


def map_int() -> Transform:
    return lambda xs: list(map(int, xs))


def sort_values() -> Transform:
    return lambda xs: sorted(xs)


def join(sep: str) -> Transform:
    return lambda xs: sep.join(map(str, xs))


def lower() -> Transform:
    return lambda x: x.lower()


def capitalize_first() -> Transform:
    return lambda x: x[0].upper() + x[1:]


def count_where(predicate: Callable[[Any], bool]) -> Transform:
    return lambda xs: sum(bool(predicate(x)) for x in xs)


def reduce_sum(mapper: Callable[[Any], int] = lambda x: x) -> Transform:
    return lambda xs: sum(mapper(x) for x in xs)


def emit_newline() -> Transform:
    return lambda x: f"{x}\n"


# Example generated programs. These are not special-cased by the runtime;
# they are ordinary compositions of reusable operators.
HELPFUL_MATHS = (
    Pipe()
    .then(strip())
    .then(split("+"))
    .then(sort_values())
    .then(join("+"))
    .then(emit_newline())
)

WORD_CAPITALIZATION = (
    Pipe()
    .then(strip())
    .then(capitalize_first())
    .then(emit_newline())
)


def compile_python(pipe: Pipe, function_name: str = "solve") -> str:
    """Return a readable Python skeleton for a Pipe.

    A later version can make each operator carry a code-generation template.
    For now this documents the compilation target without using eval/exec.
    """
    names = [getattr(step, "__name__", "transform") for step in pipe.steps]
    body = "\n".join(f"    # step {i + 1}: {name}" for i, name in enumerate(names))
    return f"def {function_name}(value):\n{body}\n    return value\n"
