import math

from fair_eval import evaluate


def test_evaluate_returns_reasonable_score():
    res = evaluate(
        prompt="Explain transformers to a 12 year old.",
        output="Transformers help AI understand text by learning patterns over words."
    )

    # basic sanity checks
    assert isinstance(res.score, (int, float))
    assert 0.0 <= res.score <= 1.0 or not math.isfinite(res.score)

    assert isinstance(res.rubric_breakdown, dict)
    assert set(res.rubric_breakdown.keys()) >= {"helpfulness", "relevance", "clarity"}

    # toxicity should be a small dict-like with a composite field
    tox = res.toxicity.to_dict()
    assert "composite" in tox
    assert isinstance(tox["composite"], (int, float))
    assert 0.0 <= tox["composite"] <= 1.0

