from contestforge_r.generative import HELPFUL_MATHS, WORD_CAPITALIZATION


def test_helpful_maths_pipeline() -> None:
    assert HELPFUL_MATHS.run("3+2+1\n") == "1+2+3\n"
    assert HELPFUL_MATHS.run("1+1+3+1+3\n") == "1+1+1+3+3\n"


def test_word_capitalization_pipeline() -> None:
    assert WORD_CAPITALIZATION.run("konjac\n") == "Konjac\n"
    assert WORD_CAPITALIZATION.run("ApPLe\n") == "ApPLe\n"
