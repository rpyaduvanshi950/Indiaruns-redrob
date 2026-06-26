"""
Scoring functions for the Redrob Intelligent Candidate Discovery challenge.

JD target: Senior AI Engineer — Founding Team at Redrob AI
  - 5–9 years (flexible 4–11 if other signals strong)
  - Has shipped at least one end-to-end ranking, search, or rec system to real users
  - Product company background (NOT pure IT services / BPO)
  - Noida/Pune preferred; broader India acceptable

Composite formula (6 components):
  raw = 0.25*role + 0.25*skills + 0.20*career_desc + 0.15*experience
        + 0.10*location + 0.05*notice
  final = raw * behavioral_multiplier    (multiplier ∈ [0.50, 1.25])

Key data insight (from EDA on 100K candidates):
  - Common skills (AWS, Docker, Kafka…) appear ~12,000 times — pure noise.
  - JD-critical skills (PyTorch, Milvus, BM25, QLoRA…) appear ~1,300 times — true signal.
  - Career descriptions surface the single most valuable signal: whether the
    candidate actually shipped retrieval/ranking/search work to real users.
"""

from datetime import date

TODAY = date(2026, 6, 26)

# ---------------------------------------------------------------------------
# 0. CAREER DESCRIPTION KEYWORD SETS
#    Used by both career_description_score() and role_relevance_score()
# ---------------------------------------------------------------------------

_PROD_DESC_SIGNALS = frozenset({
    "shipped", "ship ", "deployed", "production", "serving",
    "real-time", "realtime", "endpoint", "launched", "live ",
    "a/b test", "scale", "latency", "throughput", "users",
    "traffic", "customers",
})
_RETRIEVAL_DESC_SIGNALS = frozenset({
    "ranking", "retrieval", "recommendation", "semantic search",
    "vector search", "embedding", "faiss", "milvus", "qdrant",
    "weaviate", "pinecone", "opensearch", "elasticsearch", "bm25",
    "hybrid search", "learning to rank", "reranking", "re-rank",
    "nearest neighbor", "ann search", "knowledge base",
    "information retrieval", "search engine", "ndcg",
})
_LLM_DESC_SIGNALS = frozenset({
    "fine-tun", "fine tuning", "lora", "qlora", "peft", " rag ",
    "retrieval augmented", "language model", "llm", "bert",
    "transformer", "hugging face", "langchain", "llamaindex",
    "prompt engineer", "model serving", "inference pipeline",
})
_RESEARCH_DESC_FLAGS = frozenset({
    "paper", "publish", "arxiv", "conference proceeding", "neurips",
    "icml", "cvpr", "emnlp", "acl ", "thesis", "dissertation",
    "research lab", "citation", "co-author", "academia",
})
_CV_DESC_FLAGS = frozenset({
    "image classif", "object detect", "resnet", "yolo", "efficientnet",
    "computer vision", "opencv", "face recognit", "image segment",
    "convolutional neural", "image processing",
})

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

_TITLE_TO_TIER = {}
for _t in _TIER_5:
    _TITLE_TO_TIER[_t] = 5
for _t in _TIER_4:
    _TITLE_TO_TIER[_t] = 4
for _t in _TIER_3:
    _TITLE_TO_TIER[_t] = 3
for _t in _TIER_2:
    _TITLE_TO_TIER[_t] = 2

_TIER_SCORE = {5: 1.00, 4: 0.72, 3: 0.38, 2: 0.15, 1: 0.04}


def _title_tier(title: str) -> int:
    return _TITLE_TO_TIER.get(title.lower().strip(), 1)


def role_relevance_score(candidate: dict) -> float:
    """
    Weight current title at 70%, best historical AI title at 30%.
    "AI Research Engineer" is demoted if descriptions show more research
    signals (papers, conferences) than production signals.
    """
    current_title_raw = candidate["profile"]["current_title"]
    current_tier = _title_tier(current_title_raw)

    # AI Research Engineer: check whether descriptions suggest research or production
    if "research engineer" in current_title_raw.lower():
        all_desc = " ".join(
            r.get("description", "") for r in candidate.get("career_history", [])
        ).lower()
        research_hits = sum(1 for w in _RESEARCH_DESC_FLAGS if w in all_desc)
        prod_hits = sum(1 for w in _PROD_DESC_SIGNALS if w in all_desc)
        retrieval_hits = sum(1 for w in _RETRIEVAL_DESC_SIGNALS if w in all_desc)
        if research_hits >= 2 and (prod_hits + retrieval_hits) < 2:
            current_tier = min(current_tier, 3)  # demote pure researchers

    past_titles = [
        r["title"] for r in candidate.get("career_history", [])
        if not r.get("is_current", False)
    ]
    best_past_tier = max((_title_tier(t) for t in past_titles), default=1)

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

# Tier B: adjacent/supportive → weight 0.35
_SKILLS_B = {
    "speech recognition", "computer vision", "time series", "forecasting",
    "diffusion models", "object detection", "image classification",
    "reinforcement learning", "cnn", "yolo", "opencv", "asr", "gans",
    "bentoml", "data science", "tts",
    "spark", "airflow", "kafka", "data pipelines", "etl", "dbt", "snowflake",
    "bigquery", "databricks", "apache flink", "apache beam",
    "sql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd",
    "fastapi", "flask", "django",
    "git", "linux", "bash",
}

_PROF_MULT = {"beginner": 0.25, "intermediate": 0.55, "advanced": 0.80, "expert": 1.00}
_MAX_SKILL_SCORE = 8.0


def skills_match_score(candidate: dict) -> float:
    """
    Sum weighted skill contributions, normalise to [0, 1].
    quality = proficiency*0.5 + endorsement_trust*0.3 + duration_trust*0.2
    """
    total = 0.0
    for s in candidate.get("skills", []):
        name = s["name"].lower().strip()
        if name in _SKILLS_A:
            tier_weight = 1.0
        elif name in _SKILLS_B:
            tier_weight = 0.35
        else:
            tier_weight = 0.0
        if tier_weight == 0.0:
            continue
        prof = _PROF_MULT.get(s.get("proficiency", "beginner"), 0.25)
        endorse = min(s.get("endorsements", 0), 50) / 50
        dur = min(s.get("duration_months", 0), 60) / 60
        quality = prof * 0.5 + endorse * 0.3 + dur * 0.2
        total += tier_weight * quality
    return min(total / _MAX_SKILL_SCORE, 1.0)


# ---------------------------------------------------------------------------
# 3. CAREER DESCRIPTION SCORE — the single most important JD check:
#    "Has shipped at least one end-to-end ranking / search / rec system
#     to real users at meaningful scale."
# ---------------------------------------------------------------------------

def career_description_score(candidate: dict) -> float:
    """
    Keyword analysis of all career_history descriptions.
    Rewards: production-deployment signals + retrieval/search/ranking work + LLMs.
    Penalises: pure-research signals (papers/conferences) and CV-only work.
    Returns [0, 1].
    """
    all_text = " " + " ".join(
        r.get("description", "") for r in candidate.get("career_history", [])
    ).lower() + " "

    prod_count     = sum(1 for w in _PROD_DESC_SIGNALS      if w in all_text)
    retrieval_count = sum(1 for w in _RETRIEVAL_DESC_SIGNALS if w in all_text)
    llm_count      = sum(1 for w in _LLM_DESC_SIGNALS        if w in all_text)
    research_count = sum(1 for w in _RESEARCH_DESC_FLAGS     if w in all_text)
    cv_count       = sum(1 for w in _CV_DESC_FLAGS           if w in all_text)

    prod_score      = min(prod_count / 4,      1.0) * 0.35
    retrieval_score = min(retrieval_count / 5, 1.0) * 0.50
    llm_score       = min(llm_count / 4,       1.0) * 0.30

    research_penalty = min(research_count / 3, 1.0) * 0.40
    # CV-only penalty only if no retrieval or LLM signals present
    cv_penalty = (min(cv_count / 3, 1.0) * 0.20
                  if retrieval_count == 0 and llm_count == 0 else 0.0)

    raw = prod_score + retrieval_score + llm_score - research_penalty - cv_penalty
    return max(0.0, min(raw / 1.15, 1.0))   # 1.15 = theoretical max positive


# ---------------------------------------------------------------------------
# 4. EXPERIENCE QUALITY — years + company type + salary sanity
# ---------------------------------------------------------------------------

_CONSULTING_FIRMS = frozenset({
    "tcs", "tata consultancy services", "infosys", "wipro", "accenture",
    "cognizant", "capgemini", "hcl", "tech mahindra", "mphasis", "hexaware",
    "ltimindtree", "l&t infotech", "mindtree", "birlasoft", "niit technologies",
    "mastech", "zensar", "persistent systems", "cyient", "coforge", "sonata",
    "kellton tech", "happiest minds", "dxc technology", "ntt data",
    "genpact", "exl", "exlservice", "wns", "firstsource", "serco",
    "conduent", "convergys", "teletech", "ibm", "atos", "unisys",
})
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

    # Years scoring — JD says 5–9 preferred
    if 5 <= yoe <= 9:
        years_score = 1.0
    elif 4 <= yoe < 5 or 9 < yoe <= 11:
        years_score = 0.80
    elif 11 < yoe <= 13:
        years_score = 0.55
    elif 3.5 <= yoe < 4:
        years_score = 0.40
    elif yoe >= 13:
        years_score = 0.42
    else:
        years_score = 0.18   # <3.5yr — JD says "senior judgment", hard pass

    # Company type
    history = candidate.get("career_history", [])
    if not history:
        company_score = 0.5
    else:
        consulting_months = product_months = total_months = 0
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
            if consult_ratio >= 0.95:
                company_score = 0.20
            elif consult_ratio >= 0.70:
                company_score = 0.45
            elif product_ratio >= 0.60:
                company_score = 1.00
            elif product_ratio >= 0.30:
                company_score = 0.80
            else:
                company_score = 0.65

    # Current industry boost
    current_industry = candidate["profile"].get("current_industry", "").lower()
    if any(pi in current_industry for pi in _PRODUCT_INDUSTRIES):
        industry_boost = 0.10
    elif any(si in current_industry for si in _SERVICES_INDUSTRIES):
        industry_boost = -0.05
    else:
        industry_boost = 0.0

    # CV-primary without NLP/IR exposure (JD red flag)
    cv_skills = {"computer vision", "opencv", "yolo", "object detection",
                 "image classification", "cnn", "speech recognition", "asr", "tts"}
    nlp_ir_skills = {"nlp", "information retrieval", "semantic search", "bm25",
                     "elasticsearch", "qdrant", "faiss", "weaviate", "milvus",
                     "learning to rank", "rag", "fine-tuning llms", "sentence-transformers",
                     "embeddings", "vector search", "pgvector", "opensearch"}
    cand_skills = {s["name"].lower() for s in candidate.get("skills", [])}
    has_cv_primary = bool(cand_skills & cv_skills)
    has_nlp_ir = bool(cand_skills & nlp_ir_skills)
    domain_penalty = -0.15 if (has_cv_primary and not has_nlp_ir) else 0.0

    # Salary sanity — gentle signal only
    sig = candidate.get("redrob_signals", {})
    salary_info = sig.get("expected_salary_range_inr_lpa", {})
    sal_min = salary_info.get("min", 0) if isinstance(salary_info, dict) else 0
    sal_adj = 0.0
    if sal_min > 0:
        if yoe >= 5 and sal_min < 8:
            sal_adj = -0.05   # implausibly low for seniority level
        elif sal_min > 100:
            sal_adj = -0.03   # above early-stage startup budget

    score = years_score * 0.55 + company_score * 0.45 + industry_boost + domain_penalty + sal_adj
    return max(0.0, min(score, 1.0))


# ---------------------------------------------------------------------------
# 5. LOCATION SCORE
# ---------------------------------------------------------------------------

_INDIA_TOP_PREFERRED = frozenset({"noida", "pune"})
_INDIA_TOP = frozenset({
    "noida", "pune", "gurgaon", "gurugram", "delhi", "new delhi", "bengaluru",
    "bangalore", "mumbai", "hyderabad", "chennai", "kolkata",
})
_INDIA_OTHER = frozenset({
    "ahmedabad", "kochi", "thiruvananthapuram", "jaipur", "chandigarh",
    "lucknow", "nagpur", "bhopal", "surat", "coimbatore", "indore",
    "vadodara", "visakhapatnam", "vizag", "patna", "bhubaneswar",
})
_CLOSE_ABROAD = frozenset({"singapore", "uae", "dubai", "abu dhabi"})


def location_score(candidate: dict) -> float:
    loc = candidate["profile"].get("location", "").lower()
    country = candidate["profile"].get("country", "").lower()
    willing = candidate["redrob_signals"].get("willing_to_relocate", False)

    if any(city in loc for city in _INDIA_TOP_PREFERRED):
        return 1.10
    if any(city in loc for city in _INDIA_TOP):
        return 1.0
    if country == "india":
        if any(city in loc for city in _INDIA_OTHER):
            return 0.80
        return 0.70
    if any(place in loc or place in country for place in _CLOSE_ABROAD):
        return 0.45 if willing else 0.25
    if country in {"uk", "united kingdom", "australia", "canada", "usa",
                   "united states", "germany"}:
        return 0.35 if willing else 0.12
    return 0.18 if willing else 0.08


# ---------------------------------------------------------------------------
# 6. NOTICE PERIOD SCORE
# ---------------------------------------------------------------------------

def notice_period_score(candidate: dict) -> float:
    days = candidate["redrob_signals"].get("notice_period_days", 90)
    if days <= 15:  return 1.00
    if days <= 30:  return 0.90
    if days <= 45:  return 0.75
    if days <= 60:  return 0.60
    if days <= 90:  return 0.40
    return 0.20


# ---------------------------------------------------------------------------
# 7. BEHAVIORAL MULTIPLIER — availability + engagement signals
# ---------------------------------------------------------------------------

def behavioral_multiplier(candidate: dict) -> float:
    """
    Returns a multiplier in [0.50, 1.25].
    Floor 0.50: even a completely inactive candidate halves their score —
    not eliminated (they may be passively open); ceiling 1.25: engaged
    candidates get a 25% boost, not an outsized one.
    """
    sig = candidate["redrob_signals"]
    score = 0.0

    last_active_str = sig.get("last_active_date", "2020-01-01")
    last_active = date.fromisoformat(last_active_str)
    days_inactive = (TODAY - last_active).days
    if days_inactive <= 14:    activity = 1.00
    elif days_inactive <= 30:  activity = 0.90
    elif days_inactive <= 60:  activity = 0.75
    elif days_inactive <= 90:  activity = 0.55
    elif days_inactive <= 180: activity = 0.35
    else:                      activity = 0.10
    score += 0.28 * activity

    score += 0.18 if sig.get("open_to_work_flag") else 0.0
    score += 0.22 * sig.get("recruiter_response_rate", 0.0)
    score += 0.14 * sig.get("interview_completion_rate", 0.0)

    gh = sig.get("github_activity_score", -1)
    if gh >= 0:
        score += 0.10 * (gh / 100)

    completeness = sig.get("profile_completeness_score", 50) / 100
    verified = (
        int(sig.get("verified_email", False)) +
        int(sig.get("verified_phone", False)) +
        int(sig.get("linkedin_connected", False))
    ) / 3
    score += 0.08 * (completeness * 0.6 + verified * 0.4)

    # Map [0, 1] → [0.50, 1.25]
    return 0.50 + 0.75 * score


# ---------------------------------------------------------------------------
# 8. COMPOSITE SCORE
# ---------------------------------------------------------------------------

WEIGHTS = {
    "role":        0.25,
    "skills":      0.25,
    "career_desc": 0.20,
    "experience":  0.15,
    "location":    0.10,
    "notice":      0.05,
}


def composite_score(candidate: dict) -> tuple[float, dict]:
    """
    Return (final_score, component_dict).
    Score is unclipped so top candidates are differentiated before normalization.
    """
    components = {
        "role":        role_relevance_score(candidate),
        "skills":      skills_match_score(candidate),
        "career_desc": career_description_score(candidate),
        "experience":  experience_quality_score(candidate),
        "location":    location_score(candidate),
        "notice":      notice_period_score(candidate),
    }
    raw = sum(WEIGHTS[k] * v for k, v in components.items())
    bm = behavioral_multiplier(candidate)
    components["behavioral_mult"] = bm
    final = raw * bm
    components["final"] = final
    return final, components


# ---------------------------------------------------------------------------
# 9. REASONING GENERATOR — candidate-specific, non-templated
# ---------------------------------------------------------------------------

def _desc_highlight(candidate: dict) -> str:
    """
    First sentence from the most retrieval/production-relevant role description.
    Caps at 110 characters to keep reasoning concise.
    """
    best_desc, best_score = "", 0
    for role in sorted(
        candidate.get("career_history", []),
        key=lambda r: r.get("start_date", ""), reverse=True,
    ):
        desc = role.get("description", "").strip()
        if not desc:
            continue
        relevance = (
            sum(1 for w in _RETRIEVAL_DESC_SIGNALS if w in desc.lower()) * 2
            + sum(1 for w in _PROD_DESC_SIGNALS if w in desc.lower())
        )
        if relevance > best_score:
            best_score, best_desc = relevance, desc

    if not best_desc:
        # Fall back to any description
        for role in sorted(
            candidate.get("career_history", []),
            key=lambda r: r.get("start_date", ""), reverse=True,
        ):
            if role.get("description", "").strip():
                best_desc = role["description"].strip()
                break

    if not best_desc:
        return ""

    first = best_desc.split(".")[0].strip()
    if len(first) < 30 and "." in best_desc:
        parts = best_desc.split(".")
        first = ". ".join(p.strip() for p in parts[:2] if p.strip())
    if len(first) <= 110:
        return first
    # Cut at last space before the limit to avoid mid-word breaks
    cut = first[:110].rsplit(" ", 1)[0]
    return cut + "…"


def generate_reasoning(candidate: dict, components: dict) -> str:
    """
    Candidate-specific reasoning with varied structure.
    - Strong retrieval/production fit: leads with description highlight.
    - Moderate fit: leads with career summary + specific skills.
    - Concern-dominant: leads with the main red flag.
    - Default: title + company + skills + availability.
    """
    p = candidate["profile"]
    sig = candidate["redrob_signals"]

    title = p.get("current_title", "Professional")
    yoe = p.get("years_of_experience", 0)
    company = p.get("current_company", "")
    industry = p.get("current_industry", "")

    role_s = components.get("role", 0)
    desc_s = components.get("career_desc", 0)
    exp_s  = components.get("experience", 0)
    bm     = components.get("behavioral_mult", 1.0)

    notice = sig.get("notice_period_days", 90)
    days_inactive = (TODAY - date.fromisoformat(
        sig.get("last_active_date", "2020-01-01")
    )).days
    otw  = sig.get("open_to_work_flag", False)
    resp = sig.get("recruiter_response_rate", 0.0)

    # Top JD-critical skills (prefer advanced/expert)
    top_skills = [
        s["name"] for s in candidate.get("skills", [])
        if s["name"].lower() in _SKILLS_A
        and s.get("proficiency") in ("advanced", "expert")
    ][:4]
    if not top_skills:
        top_skills = [
            s["name"] for s in candidate.get("skills", [])
            if s["name"].lower() in _SKILLS_A
        ][:3]
    skill_str = ", ".join(top_skills) if top_skills else "no JD-critical skills matched"

    highlight = _desc_highlight(candidate)

    # Company context string
    co_str = (f"{company} ({industry})" if company and industry
              else company or industry or "unknown company")

    # Identify the single most important concern
    concern = None
    if yoe < 3.5:
        concern = f"only {yoe:.1f}yr experience — JD needs senior judgment"
    elif exp_s < 0.35:
        concern = "predominantly consulting/BPO background (TCS/Infosys-type)"
    elif notice > 90:
        concern = f"{notice}d notice period"
    elif days_inactive > 180 and not otw:
        concern = f"inactive {days_inactive}d and not open to work"
    elif title.lower() in {"java developer", "frontend engineer", "mobile developer",
                            "devops engineer", "qa engineer", "cloud engineer",
                            ".net developer"}:
        concern = f"primary role ({title}) is non-ML track"

    # Availability line
    if otw and days_inactive <= 30 and resp >= 0.7:
        avail = f"actively engaged — OTW, {resp:.0%} response rate, {notice}d notice"
    elif otw and days_inactive <= 60:
        avail = f"open to work, {notice}d notice"
    elif days_inactive <= 30:
        avail = f"recently active ({days_inactive}d), {notice}d notice"
    elif otw:
        avail = f"OTW but {days_inactive}d inactive; {notice}d notice"
    else:
        avail = f"{days_inactive}d inactive, not OTW"

    # ── Varied reasoning structure ────────────────────────────────────────────

    if desc_s >= 0.55 and role_s >= 0.85 and highlight:
        # Lead with the specific career achievement (the strongest possible signal)
        if concern:
            r = (f"{highlight}. "
                 f"Has {skill_str} at {co_str}; {avail}. "
                 f"Risk: {concern}.")
        else:
            r = (f"{highlight}. "
                 f"{skill_str} in production context at {co_str}; {avail}.")

    elif desc_s >= 0.30 and role_s >= 0.70:
        # Solid retrieval/search work — lead with career profile
        if concern:
            r = (f"{yoe:.0f}yr {title.lower()} at {co_str}; "
                 f"retrieval/search background, {skill_str}. "
                 f"{avail.capitalize()}. Main risk: {concern}.")
        else:
            r = (f"{yoe:.0f}yr {title.lower()} at {co_str}; "
                 f"production retrieval/search background. "
                 f"Skills: {skill_str}. {avail.capitalize()}.")

    elif concern:
        # Concern-first for weak or borderline candidates
        r = (f"Flag — {concern}. "
             f"{yoe:.1f}yr at {co_str}; {skill_str}. "
             f"{avail.capitalize()}.")

    else:
        # Default: concise summary
        r = f"{title} ({yoe:.1f}yr, {co_str}); {skill_str}; {avail}."

    return r.strip()
