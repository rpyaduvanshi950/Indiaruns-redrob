# SignalSutra — Intelligent Candidate Ranker

**India Runs Hackathon · Track 1: The Data & AI Challenge**
Redrob AI × Hack2Skill | Team: SignalSutra | June 2026

---

## Problem

Rank the top 100 candidates from **100,000 profiles** for a Senior AI Engineer role (founding team, Noida/Pune).

The hard part is not filtering for "ML Engineer" — it's surfacing the candidates who have **actually shipped** a search, ranking, or recommendation system to real users at scale, vs. those who have only studied or researched it.

---

## Approach

A rule-based multi-signal ranker with **6 scoring components** and a **behavioral multiplier**. No LLM inference, no embeddings, no network calls at runtime.

### Scoring formula

```
composite = 0.25×role + 0.25×skills + 0.20×career_desc + 0.15×experience + 0.10×location + 0.05×notice
final     = composite × behavioral_multiplier   # multiplier ∈ [0.50, 1.25]
```

Top-100 raw scores are linearly normalised to **[0.2000, 0.9920]** before CSV output.

### Components

| Component | Weight | What it measures |
|---|---|---|
| Role relevance | 25% | Title tier (Senior ML/AI/NLP Engineer → tier 5; Junior ML → tier 3); AI Research Engineers demoted if descriptions show more academic than production signals |
| Skills match | 25% | JD-critical skills weighted by proficiency level, endorsements, and months used; keyword rarity bonus for niche signals (BM25, QLoRA, Milvus) |
| **Career descriptions** | **20%** | Keyword analysis of `career_history[].description` — production signals (shipped, latency, A/B test), retrieval signals (NDCG, BM25, learning-to-rank, FAISS), LLM signals (RAG, LoRA, fine-tuning); research penalty (arxiv, paper, conference) |
| Experience quality | 15% | Years in preferred range (5–9) × company type (product startup > consulting/BPO) |
| Location | 10% | Noida/Pune preferred; India tier-1 cities accepted; abroad without relocation willingness penalised |
| Notice period | 5% | Immediate/≤30 days = 1.0; 90+ days = 0.40 |
| Behavioral multiplier | ×0.50–1.25 | Activity recency (28%) · OTW flag (18%) · recruiter response rate (22%) · interview completion (14%) · GitHub activity (10%) · profile completeness (8%) |

### Career descriptions — the key insight

The JD's hardest requirement is **"has shipped at least one end-to-end ranking/search/recommendation system to real users at meaningful scale."** A candidate's title and skills can be gamed or generic; what they wrote about what they actually built cannot. Keyword analysis on `career_history[].description` surfaces this signal cheaply without any model inference.

### Honeypot detection

191 candidates flagged via 5 structural signals:
- Career end date before start date
- Future end date (year > 2026)
- Role duration > 3 months off from stated months
- Expert-rated skill with 0 months duration
- 6 or more expert-rated skills (statistically impossible)

All flagged candidates are forced to **score 0** and do not appear in the top 100.

---

## Results

| Rank | Candidate | Title | Score |
|---|---|---|---|
| 1 | CAND_0046525 | Senior ML Engineer, Genpact AI (Pune) | 0.9920 |
| 2 | CAND_0076163 | NLP Engineer, Ola (Bengaluru) | 0.9230 |
| 3 | CAND_0041669 | Recommendation Systems Engineer, CRED (Noida) | 0.9032 |
| 4 | CAND_0096142 | Applied ML Engineer, upGrad (Mumbai) | 0.8637 |
| 5 | CAND_0099806 | AI Engineer, Mad Street Den (Chennai) | 0.7738 |

Full ranking: [`track1_data_ai/submission/submission.csv`](track1_data_ai/submission/submission.csv)

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/rpyaduvanshi950/Indiaruns-redrob.git
cd Indiaruns-redrob

# 2. Place the organiser-provided dataset
#    (candidates.jsonl, ~465 MB — not committed)
cp /path/to/candidates.jsonl track1_data_ai/data/candidates.jsonl

# 3. Run the ranker  (pure Python stdlib, no installs needed)
python rank.py \
  --candidates track1_data_ai/data/candidates.jsonl \
  --out submission.csv

# 4. Validate output format
python track1_data_ai/submission/validate_submission.py submission.csv
```

**Runtime:** ~58 seconds on CPU, 16 GB RAM.
**Budget:** 300 seconds (5 minutes). Budget remaining: ~242 seconds.

---

## Sandbox

Try the ranker in-browser on up to 100 candidates (no setup needed):

**[https://signalsutra.streamlit.app](https://signalsutra.streamlit.app)**

Upload your own JSONL or click **Use built-in sample** → **Run ranker**.
Download the resulting `submission.csv` directly from the app.

To run the sandbox locally:

```bash
pip install streamlit
streamlit run track1_data_ai/app.py
```

---

## Repository structure

```
Indiaruns-redrob/
│
├── rank.py                          # Entry point — run from repo root
├── submission_metadata.yaml         # Team info, approach summary, declarations
├── README.md
│
└── track1_data_ai/
    ├── app.py                       # Streamlit sandbox (share.streamlit.io)
    ├── requirements.txt             # streamlit>=1.35.0  (ranker needs none)
    │
    ├── src/
    │   ├── rank.py                  # Loads data, scores, normalises, writes CSV
    │   ├── scoring.py               # All 6 components + behavioral multiplier
    │   └── honeypot.py              # 5-signal honeypot detector
    │
    ├── data/
    │   ├── candidate_schema.json    # Field definitions
    │   └── sample_candidates.json  # 50-candidate sample for the sandbox
    │
    └── submission/
        ├── submission.csv           # Final ranked top-100
        └── validate_submission.py  # Organiser-provided format validator
```

---

## Compute constraints

| Constraint | Requirement | Actual |
|---|---|---|
| Max runtime | 300 s | ~58 s |
| RAM | ≤ 16 GB | < 1 GB |
| GPU | Not allowed | Not used |
| Network during ranking | Not allowed | Not used |
| External packages (ranker) | — | None (pure stdlib) |

---

## AI tools declaration

Used **Claude (claude-sonnet-4-6)** for architecture discussion, scoring weight rationale, and code review. All engineering decisions, skill taxonomy design, honeypot logic, and final scoring weights are original work. No candidate data was fed to any LLM at any point.

---

*Team SignalSutra · Pushpender · rpyaduvanshi950@gmail.com · +91-9257009192*
