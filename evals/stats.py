from __future__ import annotations

import math
from statistics import mean, stdev
from typing import Any, Dict, Iterable, List

try:
    from scipy.stats import chi2_contingency, ttest_ind
except Exception:  # pragma: no cover
    chi2_contingency = None
    ttest_ind = None


def confidence_interval(values: List[float], confidence: float = 0.95) -> Dict[str, Any]:
    if not values:
        return {"n": 0, "mean": 0.0, "lower": 0.0, "upper": 0.0, "half_width": 0.0}
    if len(values) == 1:
        x = float(values[0])
        return {"n": 1, "mean": x, "lower": x, "upper": x, "half_width": 0.0}
    m = mean(values)
    s = stdev(values)
    z = 1.96 if confidence == 0.95 else 1.645
    half = z * (s / math.sqrt(len(values)))
    return {
        "n": len(values),
        "mean": round(float(m), 6),
        "lower": round(float(m - half), 6),
        "upper": round(float(m + half), 6),
        "half_width": round(float(half), 6),
    }


def welch_t_test(sample_a: List[float], sample_b: List[float]) -> Dict[str, Any]:
    if len(sample_a) < 2 or len(sample_b) < 2:
        return {"supported": False, "reason": "need at least 2 observations per sample"}
    if len(set(sample_a + sample_b)) == 1:
        return {
            "supported": False,
            "reason": "all observations identical; t-test not informative",
            "baseline_mean": round(float(mean(sample_a)), 6),
            "candidate_mean": round(float(mean(sample_b)), 6),
        }
    if ttest_ind is not None:
        res = ttest_ind(sample_a, sample_b, equal_var=False)
        statistic = float(res.statistic)
        pvalue = float(res.pvalue)
        if math.isnan(statistic) or math.isnan(pvalue):
            return {
                "supported": False,
                "reason": "t-test returned NaN due to zero variance or identical samples",
                "baseline_mean": round(float(mean(sample_a)), 6),
                "candidate_mean": round(float(mean(sample_b)), 6),
            }
        return {
            "supported": True,
            "test": "welch_t_test",
            "t_statistic": round(statistic, 6),
            "p_value": round(pvalue, 6),
            "baseline_mean": round(float(mean(sample_a)), 6),
            "candidate_mean": round(float(mean(sample_b)), 6),
        }
    m1, m2 = mean(sample_a), mean(sample_b)
    s1, s2 = stdev(sample_a), stdev(sample_b)
    denom = math.sqrt((s1 * s1 / len(sample_a)) + (s2 * s2 / len(sample_b)))
    t_stat = 0.0 if denom == 0 else (m2 - m1) / denom
    # normal approximation fallback
    p_value = math.erfc(abs(t_stat) / math.sqrt(2.0))
    return {
        "supported": True,
        "test": "welch_t_test_normal_approx",
        "t_statistic": round(float(t_stat), 6),
        "p_value": round(float(p_value), 6),
        "baseline_mean": round(float(m1), 6),
        "candidate_mean": round(float(m2), 6),
    }


def chi_squared_pass_fail(baseline_passes: int, baseline_fails: int, candidate_passes: int, candidate_fails: int) -> Dict[str, Any]:
    table = [[baseline_passes, baseline_fails], [candidate_passes, candidate_fails]]
    if baseline_fails == 0 and candidate_fails == 0:
        return {
            "supported": False,
            "reason": "all observations passed; chi-squared not informative",
            "observed": table,
        }
    if baseline_passes == 0 and candidate_passes == 0:
        return {
            "supported": False,
            "reason": "all observations failed; chi-squared not informative",
            "observed": table,
        }
    if chi2_contingency is not None:
        try:
            stat, p_value, _, expected = chi2_contingency(table)
            return {
                "supported": True,
                "test": "chi_squared",
                "chi2_statistic": round(float(stat), 6),
                "p_value": round(float(p_value), 6),
                "observed": table,
                "expected": [[round(float(x), 6) for x in row] for row in expected],
            }
        except ValueError:
            return {
                "supported": False,
                "reason": "zero expected cell prevented chi-squared calculation",
                "observed": table,
            }
    total = sum(sum(row) for row in table)
    if total == 0:
        return {"supported": False, "reason": "empty contingency table"}
    row_totals = [sum(row) for row in table]
    col_totals = [table[0][0] + table[1][0], table[0][1] + table[1][1]]
    expected = [[row_totals[r] * col_totals[c] / total for c in range(2)] for r in range(2)]
    chi2 = 0.0
    for r in range(2):
        for c in range(2):
            if expected[r][c] > 0:
                chi2 += ((table[r][c] - expected[r][c]) ** 2) / expected[r][c]
    p_value = math.exp(-0.5 * chi2)
    return {
        "supported": True,
        "test": "chi_squared_df1_approx",
        "chi2_statistic": round(float(chi2), 6),
        "p_value": round(float(p_value), 6),
        "observed": table,
        "expected": [[round(float(x), 6) for x in row] for row in expected],
    }
