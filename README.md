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

# 2. Run (no installs needed — pure Python stdlib):
python track1_data_ai/src/rank.py \
  --candidates track1_data_ai/data/candidates.jsonl \
  --out track1_data_ai/submission/submission.csv

# 3. Validate:
python track1_data_ai/submission/validate_submission.py \
  track1_data_ai/submission/submission.csv
```

**Runtime:** ~15 seconds on CPU with 16 GB RAM. No GPU, no network, no external packages.

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

Rule-based multi-signal ranker with five components and a behavioral multiplier:

| Component | Weight | Key signal |
|---|---|---|
| Role relevance | 35% | Current title tier (ML/AI Engineer = tier 5) + career history |
| Skills match | 25% | JD-critical skills (NLP, vector DBs, Python, BM25…) weighted by proficiency + endorsements |
| Experience quality | 20% | Years in range (5–9 preferred) × company type (product vs. consulting) |
| Location | 10% | Noida/Pune preferred (1.10×), India top cities (1.0×), abroad penalised |
| Notice period | 10% | Sub-30 days = 1.0, 90+ days = 0.40 |
| Behavioral multiplier | ×0.30–1.40 | Activity recency, OTW flag, recruiter response rate, interview completion, GitHub activity |

**Honeypot detection:** 191 candidates flagged via duration mismatch, expert+0-months skills, or impossible profile combinations — all forced to score 0, none appear in top 100.

**Compute:** Scores are computed with pure Python arithmetic. No model inference, no embeddings at runtime. Full 100K dataset scored in ~15 seconds.

---

## Track 2 — The Ideathon

See [`track2_ideathon/PLAN.md`](track2_ideathon/PLAN.md) for the pitch: **Bharat Score** — WhatsApp-native AI credentialing for India's 450M informal workers.

---

## AI tools declaration

Used Claude (claude-sonnet-4-6) for architecture discussion, scoring weight tuning, and code review. All engineering decisions, data analysis, and final design are original work. No candidate data was fed to any LLM during development.
