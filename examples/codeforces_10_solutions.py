"""Ten small Codeforces reference solutions used to study solver abstractions.

Each function accepts the full stdin text and returns exactly what should be
printed. This makes the solutions easy to unit-test and easy to compare with a
future generated solver.
"""

from __future__ import annotations


def cf_4a_watermelon(data: str) -> str:
    w = int(data.strip())
    return "YES\n" if w > 2 and w % 2 == 0 else "NO\n"


def cf_71a_way_too_long_words(data: str) -> str:
    lines = data.strip().splitlines()
    n = int(lines[0])
    out: list[str] = []
    for word in lines[1 : n + 1]:
        out.append(word if len(word) <= 10 else f"{word[0]}{len(word)-2}{word[-1]}")
    return "\n".join(out) + "\n"


def cf_231a_team(data: str) -> str:
    lines = data.strip().splitlines()
    n = int(lines[0])
    solved = sum(sum(map(int, row.split())) >= 2 for row in lines[1 : n + 1])
    return f"{solved}\n"


def cf_158a_next_round(data: str) -> str:
    lines = data.strip().splitlines()
    _, k = map(int, lines[0].split())
    scores = list(map(int, lines[1].split()))
    threshold = scores[k - 1]
    return f"{sum(score > 0 and score >= threshold for score in scores)}\n"


def cf_50a_domino_piling(data: str) -> str:
    m, n = map(int, data.split())
    return f"{(m * n) // 2}\n"


def cf_282a_bit_plus_plus(data: str) -> str:
    lines = data.strip().splitlines()
    n = int(lines[0])
    x = sum(1 if "+" in statement else -1 for statement in lines[1 : n + 1])
    return f"{x}\n"


def cf_112a_petya_and_strings(data: str) -> str:
    a, b = data.strip().splitlines()[:2]
    a = a.lower()
    b = b.lower()
    return f"{(a > b) - (a < b)}\n"


def cf_339a_helpful_maths(data: str) -> str:
    terms = data.strip().split("+")
    return "+".join(sorted(terms)) + "\n"


def cf_263a_beautiful_matrix(data: str) -> str:
    rows = [list(map(int, line.split())) for line in data.strip().splitlines()]
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            if value == 1:
                return f"{abs(i - 2) + abs(j - 2)}\n"
    raise ValueError("matrix must contain a 1")


def cf_281a_word_capitalization(data: str) -> str:
    word = data.strip()
    return word[0].upper() + word[1:] + "\n"


SOLVERS = {
    "4A": cf_4a_watermelon,
    "71A": cf_71a_way_too_long_words,
    "231A": cf_231a_team,
    "158A": cf_158a_next_round,
    "50A": cf_50a_domino_piling,
    "282A": cf_282a_bit_plus_plus,
    "112A": cf_112a_petya_and_strings,
    "339A": cf_339a_helpful_maths,
    "263A": cf_263a_beautiful_matrix,
    "281A": cf_281a_word_capitalization,
}
