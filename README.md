# India Runs — Redrob AI Hackathon

Submission repository for **India Runs by Redrob AI** on Hack2Skill.

---

## Track 1 — The Data & AI Challenge

**Problem:** Intelligent Candidate Discovery & Ranking  
**Task:** Rank the top 100 candidates from 100,000 profiles for a Senior AI Engineer role.

### Reproduce the submission

```bash
# 1. Obtain candidates.jsonl from the organiser bundle and place it at:
#    track1_data_ai/data/candidates.jsonl

# 2. Run from repo root (no installs needed — pure Python stdlib):
python rank.py \
  --candidates track1_data_ai/data/candidates.jsonl \
  --out submission.csv

# 3. Validate:
python track1_data_ai/submission/validate_submission.py submission.csv
```

**Runtime:** ~58 seconds on CPU with 16 GB RAM. No GPU, no network, no external packages for the ranker (Streamlit required only for the sandbox app).

### Structure

```
track1_data_ai/
├── data/
│   └── candidate_schema.json      # field definitions (candidates.jsonl excluded — 465 MB)
├── src/
│   ├── rank.py                    # entry point — produces submission.csv
│   ├── scoring.py                 # all scoring components
│   └── honeypot.py                # honeypot detection
├── submission/
│   ├── submission.csv             # final ranked top-100
│   ├── validate_submission.py     # organiser-provided format validator
│   └── sample_submission.csv      # format reference
├── requirements.txt               # no external dependencies
└── PLAN.md                        # approach documentation
```

### Approach summary

Rule-based multi-signal ranker with six components and a behavioral multiplier:

| Component | Weight | Key signal |
|---|---|---|
| Role relevance | 25% | Current title tier (ML/AI Engineer = tier 5) + career history; AI Research Engineers demoted if descriptions show research > production signals |
| Skills match | 25% | JD-critical skills (NLP, vector DBs, Python, BM25…) weighted by proficiency + endorsements + duration |
| **Career descriptions** | **20%** | Keyword analysis of `career_history[].description`: production-deployment signals, retrieval/search/ranking work, LLM fine-tuning. Penalises pure-research signals. |
| Experience quality | 15% | Years in range (5–9 preferred) × company type (product vs. consulting/BPO) + salary sanity |
| Location | 10% | Noida/Pune preferred (1.10×), India top cities (1.0×), abroad without relocation willingness penalised heavily |
| Notice period | 5% | Sub-30 days = 1.0, 90+ days = 0.40 |
| Behavioral multiplier | ×0.50–1.25 | Activity recency (28%), OTW flag (18%), recruiter response rate (22%), interview completion (14%), GitHub (10%), profile completeness (8%) |

**Career descriptions** are the novel component: the JD's hardest requirement is "has shipped at least one end-to-end ranking/search/rec system to real users at meaningful scale." Keyword matching on actual career descriptions surfaces this signal without any LLM or embedding at runtime.

**Honeypot detection:** 191 candidates flagged via duration mismatch, expert+0-months skills, or impossible profile combinations — all forced to score 0, none appear in top 100.

**Compute:** Pure Python arithmetic. No model inference, no embeddings, no network. Full 100K dataset scored in ~58 seconds.

---

## Track 2 — The Ideathon

See [`track2_ideathon/PLAN.md`](track2_ideathon/PLAN.md) for the pitch: **Bharat Score** — WhatsApp-native AI credentialing for India's 450M informal workers.

---

## AI tools declaration

Used Claude (claude-sonnet-4-6) for architecture discussion, scoring weight tuning, and code review. All engineering decisions, data analysis, and final design are original work. No candidate data was fed to any LLM during development.
