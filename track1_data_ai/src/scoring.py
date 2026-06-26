"""
Scoring functions for the Redrob Intelligent Candidate Discovery challenge.

JD target: Senior AI Engineer — Founding Team at Redrob AI
  - 5–9 years (flexible 4–11 if other signals strong)
  - Production experience with embeddings, vector DBs, ranking eval
  - Product company background (NOT pure IT services)
  - Noida/Pune preferred; broader India acceptable

Composite formula:
  raw = 0.35*role + 0.25*skills + 0.20*experience + 0.10*location + 0.10*notice
  final = clip(raw * behavioral_multiplier, 0, 1)

Key data insight (from EDA on 100K candidates):
  - Common skills (AWS, Docker, Kafka…) appear ~12,000 times — pure noise.
  - JD-critical skills (PyTorch, Milvus, BM25, QLoRA…) appear ~1,300 times — true signal.
  - Scoring must weight rare skills heavily and ignore ubiquitous ones.
"""

from datetime import date

TODAY = date(2026, 6, 26)

# ---------------------------------------------------------------------------
# 1. ROLE RELEVANCE — based on current_title + career history titles
# ---------------------------------------------------------------------------

_TIER_5 = {
    "ml engineer", "machine learning engineer", "applied ml engineer",
    "senior machine learning engineer", "staff machine learning engineer",
    "lead ai engineer", "ai engineer", "senior ai engineer",
    "nlp engineer", "senior nlp engineer",
    "search engineer", "recommendation systems engineer",
    "senior applied scientist", "applied scientist",
    "ai research engineer",
}
_TIER_4 = {
    "data scientist", "senior data scientist",
    "senior software engineer (ml)", "computer vision engineer",
    "ai specialist", "junior ml engineer",
    "analytics engineer", "senior data engineer",
    "backend engineer", "senior software engineer",
    "data engineer",
}
_TIER_3 = {
    "software engineer", "full stack developer", "cloud engineer",
    "devops engineer", "data analyst", "java developer",
    ".net developer", "mobile developer", "frontend engineer",
    "qa engineer",
}
_TIER_2 = {
    "business analyst", "product manager", "technical lead",
    "solutions architect",
}
# Everything else → tier 1 (non-technical, e.g. HR Manager, Accountant, Sales…)

_TITLE_TO_TIER = {}
for t in _TIER_5:
    _TITLE_TO_TIER[t] = 5
for t in _TIER_4:
    _TITLE_TO_TIER[t] = 4
for t in _TIER_3:
    _TITLE_TO_TIER[t] = 3
for t in _TIER_2:
    _TITLE_TO_TIER[t] = 2

_TIER_SCORE = {5: 1.00, 4: 0.72, 3: 0.38, 2: 0.15, 1: 0.04}


def _title_tier(title: str) -> int:
    return _TITLE_TO_TIER.get(title.lower().strip(), 1)


def role_relevance_score(candidate: dict) -> float:
    """
    Weight current title at 70%, best historical AI title at 30%.
    A Backend Engineer whose last two roles were ML Engineer gets partial credit.
    """
    current_tier = _title_tier(candidate["profile"]["current_title"])

    # Best tier seen across career history (excluding current role)
    past_titles = [
        r["title"] for r in candidate.get("career_history", [])
        if not r.get("is_current", False)
    ]
    best_past_tier = max((_title_tier(t) for t in past_titles), default=1)

    combined_tier = max(current_tier, int(0.7 * current_tier + 0.3 * best_past_tier + 0.5))
    combined_tier = min(combined_tier, 5)

    score = _TIER_SCORE[current_tier] * 0.70 + _TIER_SCORE[best_past_tier] * 0.30
    return min(score, 1.0)


# ---------------------------------------------------------------------------
# 2. SKILLS MATCH — JD-critical skills are rare (~1300 occurrences each)
# ---------------------------------------------------------------------------

# Tier A: JD-critical, appear ~1300 times out of 100K → weight 1.0
_SKILLS_A = {
    "python", "pytorch", "tensorflow", "nlp", "machine learning", "deep learning",
    "scikit-learn", "elasticsearch", "llamaindex", "haystack",
    "lora", "peft", "qlora",
    "qdrant", "weaviate", "pgvector", "milvus", "opensearch", "pinecone", "faiss",
    "bm25", "learning to rank", "rag", "fine-tuning llms",
    "mlops", "mlflow", "feature engineering", "weights & biases",
    "statistical modeling", "kubeflow", "hugging face", "hugging face transformers",
    "semantic search", "vector search", "information retrieval",
    "huggingface", "transformers", "sentence-transformers",
    "xgboost", "lightgbm", "retrieval augmented generation",
}

# Tier B: adjacent/supportive, appear ~4000-5000 times → weight 0.35
_SKILLS_B = {
    "speech recognition", "computer vision", "time series", "forecasting",
    "diffusion models", "object detection", "image classification",
    "reinforcement learning", "cnn", "yolo", "opencv", "asr", "gans",
    "bentoml", "data science", "mlflow", "kubeflow", "tts",
    "spark", "airflow", "kafka", "data pipelines", "etl", "dbt", "snowflake",
    "bigquery", "databricks", "apache flink", "apache beam",
    "sql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd",
    "fastapi", "flask", "django",
    "git", "linux", "bash",
}

# Proficiency multiplier
_PROF_MULT = {"beginner": 0.25, "intermediate": 0.55, "advanced": 0.80, "expert": 1.00}

# Max possible score is capped at 1.0
_MAX_SKILL_SCORE = 8.0  # normalisation denominator


def skills_match_score(candidate: dict) -> float:
    """
    Sum weighted skill contributions, normalise to [0, 1].
    Quality = proficiency * 0.5 + endorsement_trust * 0.3 + duration_trust * 0.2
    """
    total = 0.0
    for s in candidate.get("skills", []):
        name = s["name"].lower().strip()
        if name in _SKILLS_A:
            tier_weight = 1.0
        elif name in _SKILLS_B:
            tier_weight = 0.35
        else:
            tier_weight = 0.0  # noise / irrelevant

        if tier_weight == 0.0:
            continue

        prof = _PROF_MULT.get(s.get("proficiency", "beginner"), 0.25)
        endorse = min(s.get("endorsements", 0), 50) / 50
        dur = min(s.get("duration_months", 0), 60) / 60
        quality = prof * 0.5 + endorse * 0.3 + dur * 0.2
        total += tier_weight * quality

    return min(total / _MAX_SKILL_SCORE, 1.0)


# ---------------------------------------------------------------------------
# 3. EXPERIENCE QUALITY — years + company type
# ---------------------------------------------------------------------------

_CONSULTING_FIRMS = frozenset({
    # Indian IT services majors (JD explicitly red-flags these as sole employers)
    "tcs", "tata consultancy services", "infosys", "wipro", "accenture",
    "cognizant", "capgemini", "hcl", "tech mahindra", "mphasis", "hexaware",
    "ltimindtree", "l&t infotech", "mindtree", "birlasoft", "niit technologies",
    "mastech", "zensar", "persistent systems", "cyient", "coforge", "sonata",
    "kellton tech", "happiest minds", "dxc technology", "ntt data",
    # BPO/process outsourcing — similar services profile to IT services
    "genpact", "exl", "exlservice", "wns", "firstsource", "mphasis", "serco",
    "conduent", "convergys", "teletech", "ibm", "atos", "unisys",
})

# Industries that strongly suggest product-company culture
_PRODUCT_INDUSTRIES = frozenset({
    "software", "fintech", "saas", "e-commerce", "edtech", "ai/ml",
    "ai services", "healthtech", "healthtech ai", "gaming", "adtech",
    "conversational ai", "insurance tech", "transportation", "food delivery",
    "conglomerate",
})
_SERVICES_INDUSTRIES = frozenset({"it services", "consulting"})


def _is_consulting_company(name: str) -> bool:
    n = name.lower()
    return any(cf in n for cf in _CONSULTING_FIRMS)


def experience_quality_score(candidate: dict) -> float:
    yoe = candidate["profile"].get("years_of_experience", 0)

    # Years score — JD says 5-9 but flexible
    if 5 <= yoe <= 9:
        years_score = 1.0
    elif 4 <= yoe < 5 or 9 < yoe <= 11:
        years_score = 0.80
    elif 11 < yoe <= 13:
        years_score = 0.55
    elif 3.5 <= yoe < 4:
        years_score = 0.40   # borderline junior for founding-team role
    elif yoe >= 13:
        years_score = 0.42
    else:
        years_score = 0.18   # < 3.5 years — JD says "senior judgment", hard pass

    # Company type score
    history = candidate.get("career_history", [])
    if not history:
        company_score = 0.5
    else:
        consulting_months = 0
        product_months = 0
        total_months = 0
        for role in history:
            dm = role.get("duration_months", 0)
            total_months += dm
            if _is_consulting_company(role.get("company", "")):
                consulting_months += dm
            ind = role.get("industry", "").lower()
            if any(pi in ind for pi in _PRODUCT_INDUSTRIES):
                product_months += dm

        if total_months == 0:
            company_score = 0.5
        else:
            consult_ratio = consulting_months / total_months
            product_ratio = product_months / total_months
            # Pure consulting is a JD red flag
            if consult_ratio >= 0.95:
                company_score = 0.20
            elif consult_ratio >= 0.70:
                company_score = 0.45
            elif product_ratio >= 0.60:
                company_score = 1.00
            elif product_ratio >= 0.30:
                company_score = 0.80
            else:
                company_score = 0.65  # IT services but not pure consulting

    # Current industry boost
    current_industry = candidate["profile"].get("current_industry", "").lower()
    if any(pi in current_industry for pi in _PRODUCT_INDUSTRIES):
        industry_boost = 0.10
    elif any(si in current_industry for si in _SERVICES_INDUSTRIES):
        industry_boost = -0.05
    else:
        industry_boost = 0.0

    # JD red flag: Computer Vision / speech / robotics as PRIMARY domain
    # with no NLP/IR exposure — "you'd be re-learning fundamentals here"
    cv_skills = {"computer vision", "opencv", "yolo", "object detection",
                 "image classification", "cnn", "speech recognition", "asr", "tts"}
    nlp_ir_skills = {"nlp", "information retrieval", "semantic search", "bm25",
                     "elasticsearch", "qdrant", "faiss", "weaviate", "milvus",
                     "learning to rank", "rag", "fine-tuning llms", "sentence-transformers",
                     "embeddings", "vector search", "pgvector", "opensearch"}
    cand_skills = {s["name"].lower() for s in candidate.get("skills", [])}
    has_cv_primary = bool(cand_skills & cv_skills)
    has_nlp_ir = bool(cand_skills & nlp_ir_skills)
    if has_cv_primary and not has_nlp_ir:
        domain_penalty = -0.15   # significant penalty: wrong specialisation
    elif has_cv_primary and has_nlp_ir:
        domain_penalty = 0.0     # mixed — no penalty, candidate is versatile
    else:
        domain_penalty = 0.0

    score = years_score * 0.55 + company_score * 0.45 + industry_boost + domain_penalty
    return max(0.0, min(score, 1.0))


# ---------------------------------------------------------------------------
# 4. LOCATION SCORE
# ---------------------------------------------------------------------------

# JD explicitly says "Pune/Noida-preferred" — give them extra weight
_INDIA_TOP_PREFERRED = frozenset({"noida", "pune"})
_INDIA_TOP = frozenset({
    "noida", "pune", "gurgaon", "gurugram", "delhi", "new delhi", "bengaluru",
    "bangalore", "mumbai", "hyderabad", "chennai", "kolkata",
})
_INDIA_OTHER = frozenset({
    "ahmedabad", "kochi", "thiruvananthapuram", "jaipur", "chandigarh",
    "lucknow", "nagpur", "bhopal", "surat", "coimbatore", "indore",
    "vadodara", "visakhapatnam", "patna",
})
_CLOSE_ABROAD = frozenset({"singapore", "uae", "dubai", "abu dhabi"})


def location_score(candidate: dict) -> float:
    loc = candidate["profile"].get("location", "").lower()
    country = candidate["profile"].get("country", "").lower()
    willing = candidate["redrob_signals"].get("willing_to_relocate", False)

    if any(city in loc for city in _INDIA_TOP_PREFERRED):
        return 1.10  # Noida/Pune explicitly preferred in JD
    if any(city in loc for city in _INDIA_TOP):
        return 1.0
    if country == "india":
        if any(city in loc for city in _INDIA_OTHER):
            return 0.80
        return 0.70
    # Outside India: JD says case-by-case, no visa sponsorship
    # willing_to_relocate=False abroad is a strong negative signal
    if any(place in loc or place in country for place in _CLOSE_ABROAD):
        return 0.45 if willing else 0.25
    if country in {"uk", "united kingdom", "australia", "canada", "usa",
                   "united states", "germany"}:
        return 0.35 if willing else 0.12  # unwilling to relocate from abroad ≈ not available
    return 0.18 if willing else 0.08


# ---------------------------------------------------------------------------
# 5. NOTICE PERIOD SCORE
# ---------------------------------------------------------------------------

def notice_period_score(candidate: dict) -> float:
    days = candidate["redrob_signals"].get("notice_period_days", 90)
    if days <= 15:
        return 1.00
    if days <= 30:
        return 0.90
    if days <= 45:
        return 0.75
    if days <= 60:
        return 0.60
    if days <= 90:
        return 0.40
    return 0.20


# ---------------------------------------------------------------------------
# 6. BEHAVIORAL MULTIPLIER — availability + engagement signals
# ---------------------------------------------------------------------------

def behavioral_multiplier(candidate: dict) -> float:
    """
    Returns a multiplier in [0.30, 1.40].
    A strong-on-paper candidate who is inactive/unresponsive gets dragged down.
    An actively engaged, responsive candidate gets boosted.
    """
    sig = candidate["redrob_signals"]
    score = 0.0

    # Activity recency (weight 0.28) — most predictive of actual availability
    last_active_str = sig.get("last_active_date", "2020-01-01")
    last_active = date.fromisoformat(last_active_str)
    days_inactive = (TODAY - last_active).days
    if days_inactive <= 14:
        activity = 1.00
    elif days_inactive <= 30:
        activity = 0.90
    elif days_inactive <= 60:
        activity = 0.75
    elif days_inactive <= 90:
        activity = 0.55
    elif days_inactive <= 180:
        activity = 0.35
    else:
        activity = 0.10
    score += 0.28 * activity

    # Open to work flag (weight 0.18)
    score += 0.18 if sig.get("open_to_work_flag") else 0.0

    # Recruiter response rate (weight 0.22)
    score += 0.22 * sig.get("recruiter_response_rate", 0.0)

    # Interview completion rate (weight 0.14)
    score += 0.14 * sig.get("interview_completion_rate", 0.0)

    # GitHub activity (weight 0.10) — strong signal for engineering quality
    gh = sig.get("github_activity_score", -1)
    if gh >= 0:
        score += 0.10 * (gh / 100)
    # else: no GitHub linked → no credit, no penalty

    # Profile completeness + verification (weight 0.08)
    completeness = sig.get("profile_completeness_score", 50) / 100
    verified = (
        int(sig.get("verified_email", False)) +
        int(sig.get("verified_phone", False)) +
        int(sig.get("linkedin_connected", False))
    ) / 3
    score += 0.08 * (completeness * 0.6 + verified * 0.4)

    # Map [0, 1] → multiplier [0.30, 1.40]
    return 0.30 + 1.10 * score


# ---------------------------------------------------------------------------
# 7. COMPOSITE SCORE
# ---------------------------------------------------------------------------

WEIGHTS = {
    "role":       0.35,
    "skills":     0.25,
    "experience": 0.20,
    "location":   0.10,
    "notice":     0.10,
}


def composite_score(candidate: dict) -> tuple[float, dict]:
    """
    Return (final_score, component_dict) for a candidate.

    Score is NOT clipped to 1.0 — we allow >1.0 so that truly exceptional
    candidates (top location + skills + behavioral signals) are differentiated
    from merely-good ones. The caller normalises before writing to CSV.
    """
    components = {
        "role":       role_relevance_score(candidate),
        "skills":     skills_match_score(candidate),
        "experience": experience_quality_score(candidate),
        "location":   location_score(candidate),
        "notice":     notice_period_score(candidate),
    }
    raw = sum(WEIGHTS[k] * v for k, v in components.items())
    bm = behavioral_multiplier(candidate)
    components["behavioral_mult"] = bm
    final = raw * bm          # no upper clip — differentiation is the goal
    components["final"] = final
    return final, components


# ---------------------------------------------------------------------------
# 8. REASONING GENERATOR
# ---------------------------------------------------------------------------

def generate_reasoning(candidate: dict, components: dict) -> str:
    """
    Generate a specific, non-hallucinated 1–2 sentence reasoning string.
    Only references facts present in the candidate's profile.
    """
    p = candidate["profile"]
    sig = candidate["redrob_signals"]
    skills = candidate.get("skills", [])

    title = p.get("current_title", "Professional")
    yoe = p.get("years_of_experience", 0)
    loc = p.get("location", p.get("country", "Unknown"))
    company = p.get("current_company", "")
    industry = p.get("current_industry", "")

    # Pick top 3 relevant skills actually in profile
    jd_skills_present = [
        s["name"] for s in skills
        if s["name"].lower() in _SKILLS_A and s.get("proficiency") in ("advanced", "expert")
    ][:3]
    if not jd_skills_present:
        jd_skills_present = [
            s["name"] for s in skills
            if s["name"].lower() in _SKILLS_A
        ][:3]

    skills_str = ", ".join(jd_skills_present) if jd_skills_present else "general software background"

    # Availability signal
    otw = sig.get("open_to_work_flag", False)
    resp = sig.get("recruiter_response_rate", 0.0)
    days_inactive = (TODAY - date.fromisoformat(sig.get("last_active_date", "2020-01-01"))).days
    notice = sig.get("notice_period_days", 90)

    if otw and days_inactive <= 60 and resp >= 0.6:
        availability = f"actively open to work, {notice}d notice, {resp:.0%} response rate"
    elif days_inactive <= 60:
        availability = f"recently active ({days_inactive}d ago), {notice}d notice"
    elif otw:
        availability = f"open to work but lower recent engagement ({days_inactive}d inactive)"
    else:
        availability = f"{days_inactive}d inactive, limited platform engagement"

    industry_str = f" at {company} ({industry})" if company and industry else ""
    return (
        f"{title} with {yoe:.1f} yrs{industry_str}; "
        f"relevant skills: {skills_str}; "
        f"{availability}."
    )
