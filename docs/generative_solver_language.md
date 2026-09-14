# Generative Solver Language (GSL)

## Motivation

The goal is to treat a programming-contest solution the way mathematical
physics often treats a model: identify a small collection of operators, compose
them, and generate a concrete realization from the composition.

This is not a claim that arbitrary Codeforces problems can be solved by one
closed-form generating function. Algorithm discovery is the hard part. The
useful target is a domain-specific language (DSL) that can express and generate
large families of known algorithmic patterns.

## Ten reference problems

The initial corpus is:

| Problem | Core abstraction |
| --- | --- |
| 4A Watermelon | predicate on an integer |
| 71A Way Too Long Words | conditional map over strings |
| 231A Team | row reduction + threshold + count |
| 158A Next Round | indexed threshold + filter/count |
| 50A Domino piling | closed-form arithmetic |
| 282A Bit++ | map statements to +/-1 + reduction |
| 112A Petya and Strings | normalization + comparison |
| 339A Helpful Maths | tokenize + sort + join |
| 263A Beautiful Matrix | search + Manhattan distance |
| 281A Word Capitalization | string transformation |

## Mathematical analogy

A generating function packages an infinite family of coefficients into one
object. GSL similarly packages a family of programs into compositions of
operators.

Write a solver schematically as

    S = O_n o O_{n-1} o ... o O_2 o O_1

where each O_i is a reusable transformation. A concrete program is obtained by
compiling the operator chain to Python, C++, Java, or another backend.

For example, Codeforces 339A can be represented as

    stdin -> strip -> split('+') -> sort -> join('+') -> stdout

and 281A as

    stdin -> strip -> capitalize_first -> stdout

The source language describes *what transformations compose the solver*; the
backend decides *how those transformations are written*.

## Proposed operator basis

The next useful basis is:

- parsing: token, line, matrix, repeated rows
- transforms: map, normalize, split, join, sort, unique
- selection: filter, argmin, argmax, find, index
- reduction: sum, product, count, min, max, xor
- predicates: comparison, parity, divisibility, bounds
- geometry: Manhattan and Euclidean distance
- sequence tools: prefix sums, suffix sums, two pointers, sliding window
- discrete structures: set, multiset, frequency map, stack, queue
- graph operators: BFS, DFS, shortest path, components, topological order
- optimization operators: greedy choice, binary search on answer
- dynamic-programming operators: state, transition, base condition, aggregation

## Suggested surface syntax

A future textual form could look like:

```text
problem HelpfulMaths {
    input  s: line
    solve  s |> split("+") |> sort |> join("+")
    output result
}
```

A threshold/count problem could look like:

```text
problem NextRound {
    input n: int, k: int
    input a: ints(n)
    let t = a[k-1]
    solve count(a, x => x > 0 && x >= t)
}
```

This syntax should first compile to a small intermediate representation (IR).
Backends can then generate Python/C++/Java. Verification can reuse
ContestForge-R's existing reference-vs-oracle machinery.

## Research direction

The interesting research question is not merely "can a DSL solve 10 easy
problems?" but:

1. What is the smallest operator basis that covers a large fraction of
   Codeforces A/B problems?
2. Can problem statements be mapped to this IR automatically or
   semi-automatically?
3. Can equivalent solver expressions be simplified algebraically?
4. Can complexity be inferred from the expression tree?
5. Can search over compositions discover a valid algorithm under test-case
   constraints?

That turns the project into a bridge between programming-language design,
program synthesis, symbolic reasoning, and the operator viewpoint common in
mathematical physics.
