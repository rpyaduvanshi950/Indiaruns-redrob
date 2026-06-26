"""
Honeypot detection for the Redrob candidate ranking challenge.

The dataset contains ~80 honeypots with subtly impossible profiles.
Submissions with honeypot rate > 10% in top 100 are auto-disqualified.

Detection signals (from submission_spec + analysis of 100K candidates):
  1. duration_mismatch  — stated duration_months vs. computed date diff > 3 months
  2. expert_zero        — 'expert' proficiency with 0 duration_months (≥2 skills)
  3. too_many_expert    — ≥6 expert-level skills across a 5-23 skill profile
  4. future_end_date    — a past (non-current) role whose end_date is in the future
  5. end_before_start   — role where end_date < start_date
"""

from datetime import date

TODAY = date(2026, 6, 26)


def _date(s):
    return date.fromisoformat(s) if s else None


def is_honeypot(candidate: dict) -> tuple[bool, list[str]]:
    """Return (flagged, reasons). If flagged, caller should force score to 0."""
    reasons = []

    for role in candidate.get("career_history", []):
        sd = _date(role.get("start_date"))
        ed = _date(role.get("end_date")) if not role.get("is_current") else None

        if sd is None:
            continue

        end = ed if ed else TODAY

        # Flag: end before start
        if ed and ed < sd:
            reasons.append("end_before_start")

        # Flag: past role with future end date
        if ed and ed > TODAY:
            reasons.append("future_end_date")

        # Flag: duration mismatch > 3 months (generous tolerance)
        stated = role.get("duration_months", 0)
        actual = (end.year - sd.year) * 12 + (end.month - sd.month)
        if abs(actual - stated) > 3:
            reasons.append(f"duration_mismatch(stated={stated},actual={actual})")

    skills = candidate.get("skills", [])

    # Flag: expert proficiency with 0 months used (≥2 such skills)
    expert_zero = sum(
        1 for s in skills
        if s.get("proficiency") == "expert" and s.get("duration_months", 1) == 0
    )
    if expert_zero >= 2:
        reasons.append(f"expert_zero_duration({expert_zero})")

    # Flag: implausibly many expert skills (≥6 out of max 23)
    expert_count = sum(1 for s in skills if s.get("proficiency") == "expert")
    if expert_count >= 6:
        reasons.append(f"too_many_expert({expert_count})")

    return bool(reasons), reasons
