from __future__ import annotations

import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List

from .spec import EvalCase


REQUIRED_TOP_LEVEL_KEYS = {"id", "input"}


def _stable_case_hash(case: EvalCase) -> str:
    payload = {
        "id": case.id,
        "input": case.input,
        "expected": case.expected,
        "metadata": case.metadata,
    }
    return hashlib.sha256(str(payload).encode("utf-8")).hexdigest()


def validate_cases(cases: List[EvalCase], baseline_created_at: str | None = None) -> Dict[str, Any]:
    duplicate_ids: List[str] = []
    duplicate_payloads: List[str] = []
    missing_expected_ids: List[str] = []
    schema_violations: List[Dict[str, Any]] = []

    seen_ids = set()
    seen_hashes = set()
    for case in cases:
        if case.id in seen_ids:
            duplicate_ids.append(case.id)
        seen_ids.add(case.id)

        payload_hash = _stable_case_hash(case)
        if payload_hash in seen_hashes:
            duplicate_payloads.append(case.id)
        seen_hashes.add(payload_hash)

        if not case.expected:
            missing_expected_ids.append(case.id)
        if not isinstance(case.input, dict):
            schema_violations.append({"case_id": case.id, "reason": "input_not_object"})
        if case.expected is not None and not isinstance(case.expected, dict):
            schema_violations.append({"case_id": case.id, "reason": "expected_not_object"})

    stale_baseline_warning = None
    if baseline_created_at:
        try:
            created = datetime.fromisoformat(baseline_created_at.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - created).days
            if age_days >= 30:
                stale_baseline_warning = {
                    "age_days": age_days,
                    "message": f"baseline is {age_days} days old; refresh recommended before release decision",
                }
        except ValueError:
            stale_baseline_warning = {"message": "unable to parse baseline_created_at"}

    pack_completeness = {
        "num_cases": len(cases),
        "complete": len(cases) > 0 and len(missing_expected_ids) == 0,
    }
    status = "pass"
    if duplicate_ids or duplicate_payloads or schema_violations or len(cases) == 0:
        status = "fail"
    elif missing_expected_ids or stale_baseline_warning:
        status = "warn"

    return {
        "status": status,
        "duplicate_case_ids": sorted(set(duplicate_ids)),
        "duplicate_case_payloads": sorted(set(duplicate_payloads)),
        "missing_expected_ids": sorted(set(missing_expected_ids)),
        "schema_violations": schema_violations,
        "stale_baseline_warning": stale_baseline_warning,
        "pack_completeness": pack_completeness,
    }
