# Track 1 — The Data & AI Challenge: Execution Plan
## Intelligent Candidate Discovery & Ranking

**Prize:** ₹10 Lakhs | **Submission closes:** ~July 2, 2026 | **Evaluation:** July 3–16 | **Finale:** July 22

---

## The Task in One Sentence

Rank the top 100 candidates from `data/candidates.jsonl` (100,000 records) for the **Senior AI Engineer — Founding Team** role at Redrob AI, output a validated CSV, and submit with a GitHub repo + sandbox demo.

---

## Scoring Formula (memorize this)

```
Final Score = 0.50 × NDCG@10 + 0.30 × NDCG@50 + 0.15 × MAP + 0.05 × P@10
```

**Implication: Getting your top 10 right wins you half the contest.** Spend 80% of tuning effort on the top 10. The tail (ranks 11–100) matters for NDCG@50 and MAP but is secondary.

---

## What the JD Actually Wants (non-obvious)

Read `docs/job_description.docx` fully. Key things keyword matching will miss:

### Must-Have Profile
- **5–9 years** total (flexible: 4–10 is fine if other signals strong)
- **Product company** background, NOT pure IT services (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini = negative signal)
- **Shipped to real users**: embedding retrieval, vector DB, ranking/search system
- **Strong Python** + evaluation frameworks (NDCG, MRR, MAP, A/B)
- **Location**: Noida/Pune preferred; Bangalore/Mumbai/Hyderabad/Delhi NCR acceptable; outside India is low score

### Hard Disqualifiers
- Career only at Indian IT services giants (TCS, Infosys, etc.) with no product-company stint
- Pure research (academia, research-only roles) without production deployment
- Primary domain is CV/speech/robotics with no NLP/IR exposure
- "AI experience" = only recent LangChain wrappers with no pre-LLM ML background

### The Big Trap (honeypots + keyword stuffers)
- ~80 honeypot candidates have impossible profiles (8 yrs at company founded 3 yrs ago; expert in 10 skills with 0 months)
- Marketing Managers / Accountants with 9 AI skills listed = keyword stuffers, NOT qualified
- **Honeypot rate > 10% in top 100 = auto-disqualified at Stage 3**
- Your scoring must penalize impossible timelines and title-skill mismatches

---

## Compute Constraints (hard rules, no exceptions)

| Constraint | Value |
|---|---|
| Max runtime (ranking step) | 5 minutes |
| RAM | 16 GB |
| GPU | NOT allowed |
| Network during ranking | NOT allowed (no API calls) |
| Pre-computation | Allowed (offline, unlimited time) |

**Strategy:** Pre-compute all features offline. The `rank.py` script loads pre-computed features and scores in <5 min on CPU.

---

## Ranking Architecture

### Phase 1: Pre-computation (offline, run once)
Run before submission, results saved to disk. No time limit.

```
pre_compute.py
├── Load all 100K candidates
├── Build skill vocabulary and score each candidate's skills
├── Extract title_tier for each candidate (AI/ML tier, Adjacent tier, etc.)
├── Extract company_type flags (product vs. services)
├── Extract location_score
├── Flatten redrob_signals into feature vectors
└── Save: features.pkl (all 100K candidate feature vectors)
```

### Phase 2: Ranking (must run in <5 min, CPU, no network)

```
rank.py --candidates ./data/candidates.jsonl --out ./submission/submission.csv
├── Load features.pkl (or recompute from candidates.jsonl if no pre-computed file)
├── Score each candidate (see scoring below)
├── Sort descending by composite score
├── Detect and penalize honeypots
├── Take top 100
├── Generate reasoning string for each
└── Write CSV: candidate_id, rank, score, reasoning
```

---

## Scoring Components

### 1. Role Relevance Score (weight: 35%)

Score the candidate's **current title + career history titles** against these tiers:

| Tier | Titles | Score |
|---|---|---|
| 5 (perfect) | AI Engineer, ML Engineer, Senior ML Engineer, Applied Scientist, Research Engineer (with prod exp), NLP Engineer, Search Engineer | 1.0 |
| 4 (strong) | Data Scientist (5+ yrs), Backend Engineer (with ML proj), Software Engineer (AI focus), Data Engineer (with ML) | 0.85 |
| 3 (adjacent) | Backend Engineer, Software Engineer, Data Engineer, Full Stack (with ML side projects) | 0.55 |
| 2 (weak) | Business Analyst, Product Manager, DevOps with AI exposure | 0.25 |
| 1 (poor) | Accountant, Marketing Manager, HR Manager, Sales, Graphic Designer | 0.05 |

Use current_title for primary classification, verify against career_history last 3 roles.

### 2. Skills Match Score (weight: 25%)

Define a "core AI skill set" from the JD. Score each candidate's skills array:

**Tier A skills (full credit per skill):**
- sentence-transformers, embeddings, semantic search, vector search, RAG
- FAISS, Pinecone, Weaviate, Qdrant, Milvus, Elasticsearch, OpenSearch
- LLM fine-tuning, LoRA, QLoRA, PEFT
- NDCG, MRR, MAP, ranking evaluation, learning-to-rank
- Python (strong signal)
- NLP, information retrieval, recommendation systems

**Tier B skills (half credit):**
- PyTorch, TensorFlow, Hugging Face, transformers
- Spark, Kafka, Airflow (data engineering background = positive)
- SQL, dbt (data background = weak positive)
- Docker, Kubernetes, MLflow (MLOps)

**Penalty skills (negative signal if these are PRIMARY skills with no AI skills):**
- Photoshop, Figma, Excel, Tally (non-technical)

**Skill quality multiplier per skill:**
```python
quality = (proficiency_score[proficiency] * 0.5) + (min(endorsements, 50) / 50 * 0.3) + (min(duration_months, 60) / 60 * 0.2)
# proficiency_score: beginner=0.25, intermediate=0.5, advanced=0.75, expert=1.0
```

### 3. Experience Quality Score (weight: 20%)

```python
# Years of experience
years = profile.years_of_experience
if 5 <= years <= 9:
    years_score = 1.0
elif 4 <= years < 5 or 9 < years <= 11:
    years_score = 0.85
elif 3 <= years < 4 or 11 < years <= 13:
    years_score = 0.65
else:
    years_score = 0.4

# Company type (from career_history)
# Penalize pure consulting background
consulting_companies = {'tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini', 
                        'hcl', 'tech mahindra', 'mphasis', 'hexaware', 'ltimindtree'}
# Check if ALL career_history companies are consulting → heavy penalty
# Check if SOME are consulting but also has product companies → minor penalty

# Company size proxy for product vs services
# 201-500, 501-1000, 1001-5000 with product industry = likely product company
# 10001+ in IT Services/Consulting = likely services company
```

### 4. Location Score (weight: 10%)

```python
india_preferred = {'noida', 'pune', 'new delhi', 'delhi', 'gurugram', 'gurgaon',
                   'bangalore', 'bengaluru', 'mumbai', 'hyderabad', 'chennai'}

if location.lower() in india_preferred:
    loc_score = 1.0
elif country == 'India':
    loc_score = 0.75
elif country in ['UAE', 'Singapore', 'UK', 'USA', 'Canada']:
    loc_score = 0.4  # relocatable
else:
    loc_score = 0.2
```

### 5. Behavioral Signal Score (weight: 10%, used as multiplier on final score)

This is a *multiplier* (0.5 to 1.5), not an additive score. A perfect-on-paper candidate with no recent activity gets dragged down significantly.

```python
def behavioral_multiplier(signals):
    score = 0.0
    
    # Activity recency (30% of multiplier)
    days_since_active = (today - last_active_date).days
    if days_since_active <= 30:    activity = 1.0
    elif days_since_active <= 90:  activity = 0.8
    elif days_since_active <= 180: activity = 0.5
    else:                          activity = 0.2
    score += 0.3 * activity
    
    # Open to work (15%)
    score += 0.15 if open_to_work_flag else 0.0
    
    # Recruiter response rate (20%)
    score += 0.20 * recruiter_response_rate
    
    # Interview completion rate (15%)
    score += 0.15 * interview_completion_rate
    
    # GitHub activity (10%)
    if github_activity_score >= 0:
        score += 0.10 * (github_activity_score / 100)
    
    # Profile completeness + verification (10%)
    verif = (verified_email + verified_phone + linkedin_connected) / 3
    score += 0.10 * ((profile_completeness_score / 100) * 0.7 + verif * 0.3)
    
    # Map score [0,1] → multiplier [0.4, 1.3]
    return 0.4 + 0.9 * score
```

### Final Composite

```python
raw_score = (
    0.35 * role_relevance_score +
    0.25 * skills_match_score +
    0.20 * experience_quality_score +
    0.10 * location_score +
    0.10 * notice_period_score  # sub-30 days = 1.0, 90+ = 0.3
)
final_score = raw_score * behavioral_multiplier(signals)
final_score = min(final_score, 1.0)
```

---

## Honeypot Detection

Check each candidate for these flags. If flagged, force score = 0.0:

```python
def is_honeypot(candidate):
    # Flag 1: Company tenure impossibility
    for role in career_history:
        if role.duration_months > (years_since_company_founded * 12 + 6):
            return True
    
    # Flag 2: Expert skill with 0 months used (more than 3 such skills)
    expert_zero_duration = sum(
        1 for s in skills
        if s.proficiency == 'expert' and s.duration_months == 0
    )
    if expert_zero_duration >= 3:
        return True
    
    # Flag 3: Too many "expert" skills (>8 expert skills = suspicious)
    if sum(1 for s in skills if s.proficiency == 'expert') > 8:
        return True
    
    return False
```

---

## Reasoning Column Strategy

The reasoning field is evaluated at Stage 4 (manual review). Judges sample 10 rows and check:
- No hallucination (only mention skills actually in profile)
- No template strings
- Specific to the candidate

**Template to generate programmatically:**
```python
def generate_reasoning(candidate, score_breakdown):
    title = candidate.profile.current_title
    years = candidate.profile.years_of_experience
    top_skills = [s.name for s in candidate.skills if s.proficiency in ['advanced', 'expert']][:3]
    loc = candidate.profile.location
    resp_rate = candidate.redrob_signals.recruiter_response_rate
    
    skill_str = ', '.join(top_skills) if top_skills else 'general software background'
    activity = 'actively engaged' if open_to_work and resp_rate > 0.5 else 'moderate engagement'
    
    return f"{title} with {years:.1f} yrs; {skill_str}; {loc}; {activity} on platform."
```

---

## File Structure

```
track1_data_ai/
├── data/
│   ├── candidates.jsonl          ← 100K candidates (DO NOT EDIT)
│   ├── candidate_schema.json     ← field definitions
│   └── sample_candidates.json   ← 5 examples for testing
├── docs/
│   ├── job_description.docx      ← the JD you're ranking for
│   ├── submission_spec.docx      ← rules + scoring formula
│   ├── redrob_signals_doc.docx   ← behavioral signals explained
│   └── README.docx               ← getting started guide
├── src/
│   ├── pre_compute.py            ← (YOU WRITE) offline feature extraction
│   ├── rank.py                   ← (YOU WRITE) main ranker, must run <5min CPU
│   ├── honeypot.py               ← (YOU WRITE) honeypot detection
│   ├── scoring.py                ← (YOU WRITE) all scoring functions
│   └── features.pkl              ← (GENERATED) pre-computed features
├── submission/
│   ├── validate_submission.py    ← run this before submitting
│   ├── sample_submission.csv     ← format reference only
│   ├── submission_metadata_template.yaml ← fill this out
│   └── YOUR_TEAM_ID.csv          ← (GENERATED) your final submission
└── PLAN.md                       ← this file
```

---

## What to Submit

1. **CSV file** — top 100 candidates, validated with `validate_submission.py`
2. **GitHub repo** — with `rank.py`, `requirements.txt`, `submission_metadata.yaml`, clear README
3. **Sandbox** — HuggingFace Spaces or Streamlit Cloud demo that accepts ≤100 candidates and outputs ranked CSV
4. **Portal metadata** — team name, email, phone, repo link, sandbox link, AI tools declaration

---

## Build Order (Day-by-Day)

| Day | Task |
|---|---|
| Day 1 | Read all docs fully. Understand every signal field. Explore 20 candidates manually. |
| Day 2 | Write `scoring.py` with role_relevance + skills_match. Test on 1000 candidates. |
| Day 3 | Add experience + location + notice_period scoring. Add honeypot detection. |
| Day 4 | Add behavioral signal multiplier. Run full 100K. Inspect top 200 manually. |
| Day 5 | Tune weights. Verify top 20 are actually strong candidates. Fix any pattern mismatches. |
| Day 6 | Generate reasoning column. Run `validate_submission.py`. Make first submission. |
| Day 7 | Build HuggingFace Spaces sandbox. Push code to GitHub. Clean repo. |

---

## What Will Get You Into Top 10 Teams

1. Correctly identifying that a "Backend Engineer" with an ML-heavy career history outranks a "Marketing Manager" with 9 AI keywords
2. Behavioral signal multiplier that downgrades paper-perfect but inactive candidates
3. Zero or near-zero honeypots in your top 100
4. Clear, specific reasoning strings that demonstrate you read the profiles
5. Reproducible code that runs in under 5 minutes on CPU
