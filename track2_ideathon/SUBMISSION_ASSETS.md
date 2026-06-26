# Track 2 — Ideathon Submission Assets
# Team SignalSutra · Bharat Score

**Deadline:** July 2, 2026 | **Portal:** hack2skill.com/event/india_runs

---

## What to Submit on the Portal

The Hack2Skill portal for Track 2 will ask for:
1. **Pitch title** → copy from Section A below
2. **One-paragraph summary** → copy from Section B below
3. **Problem statement / pitch deck** → upload `pitch/bharat_score_pitch.pdf`
4. **Contact details** → use Section D

---

## A · Pitch Title

```
Bharat Score — AI Work Credentials for India's 450M Informal Workers
```

---

## B · One-Paragraph Summary (for portal submission form)

```
India has 450 million informal workers — masons, gig drivers, data-entry
staff — who have no verifiable employment record, no LinkedIn, and no CV.
Recruiters and MSMEs cannot discover or trust them. Bharat Score is a
WhatsApp-native AI credentialing system that changes this: a worker texts
a number, completes a 5-minute adaptive voice assessment in one of 12
Indian languages, and receives a shareable verified credential — no app
download, no English required, zero friction. The system uses Indic LLMs
(Sarvam AI / IndicBERT) for multilingual NLP, adaptive questioning per
skill domain, fraud-detection via answer-consistency checks, and employer
SMS verification. The resulting Bharat Score (0–100 + skill tier) becomes
a new signal in Redrob's candidate ranking engine — expanding Redrob's
addressable talent pool from 100K structured profiles to 135M previously
invisible workers. Revenue: ₹49/verification (B2B), ₹2,000/month recruiter
seat, government skilling contracts. Year 3 ARR potential: ₹80–120 Cr.
```

---

## C · Problem Statement Mapping

The Track 2 ideathon asks: *"What AI product should Redrob build for India?"*

**Bharat Score maps to this as follows:**

| Evaluation criterion | How Bharat Score answers it |
|---|---|
| **Clear Indian problem** | 450M informal workers invisible to formal hiring platforms — the largest unserved talent pool in the world |
| **AI is essential, not optional** | Vernacular NLP, adaptive voice assessment, fraud detection via consistency scoring — none of this is possible without AI |
| **Redrob should build this** | It is literally the upstream input to Redrob's existing ranker — it creates the structured data Redrob's engine already knows how to rank |
| **Business model** | B2B verification fees + recruiter seats + government skilling contracts |
| **Market size** | 135M addressable workers, ₹80–120 Cr Year 3 ARR |

---

## D · Contact Details

- **Team name:** SignalSutra
- **Participant:** Pushpender
- **Email:** rpyaduvanshi950@gmail.com
- **Phone:** +91-9257009192
- **GitHub:** https://github.com/rpyaduvanshi950/Indiaruns-redrob

---

## E · Longer Pitch Brief (for judges / supplementary materials)

### The Problem

India's hiring platforms — Redrob, Naukri, LinkedIn — operate on structured
profiles. A candidate without a profile doesn't exist to the platform. But 450
million Indian workers — masons, electricians, gig delivery workers, small-shop
data-entry staff — have no CV, no LinkedIn, and no digital employment record.
They get jobs by word-of-mouth, lose them the same way, and can never build a
verifiable track record.

Recruiters and contractors trying to hire from this pool face a structural problem:
they can't verify what candidates claim. This isn't a scaling problem — it's a
missing-infrastructure problem.

### Why AI Is Not Optional

Three things make this an AI problem, not a forms problem:

1. **Language**: 12 Indian languages, many workers semi-literate in any written form.
   Only voice-based assessment in vernacular works at this scale.
2. **Fraud detection**: coached/memorized answers must be identified via adaptive
   follow-up questioning and consistency scoring — not checkboxes.
3. **Rubric generation**: skill assessment rubrics for 200+ informal skill domains
   (masonry, electrical, driving, cooking, tailoring, data entry...) cannot be
   hand-coded — they must be generated and calibrated from actual answer quality
   distributions using LLMs.

### Why Redrob Specifically

Redrob already has:
- A candidate ranking engine that consumes structured signals
- Recruiter relationships to validate whether Bharat Scores predict hire quality
- The product infrastructure to surface a "Bharat Score" field on candidate cards

Bharat Score is not a pivot — it is the upstream data creation layer that feeds
Redrob's existing downstream ranking engine. No other company has both the AI
credentialing problem to solve AND the ranking infrastructure to consume the output.

### The Bharat Score Formula

```
Bharat Score (0–100) =
    0.40 × Skill Assessment Score    (LLM-graded voice answers, domain rubric)
  + 0.35 × Verified Tenure           (employer SMS confirmation + duration)
  + 0.25 × Engagement Signals        (response rate, re-assessment frequency)
```

Score is language-agnostic, skill-domain-specific, and updates on each
re-assessment. Workers can improve their score by getting new employer verifications
or completing refresher assessments.

### Three Tailwinds

1. **Sarvam AI / IndicBERT / Whisper** now handle Hindi, Tamil, Bengali, Marathi,
   Telugu, Gujarati at conversational quality — the Indic NLP barrier is gone.
2. **WhatsApp Business API** allows full voice+text conversational flows to any
   verified business — zero install friction for workers.
3. **PMKVY-3.0 and ONDC** require skill certificates for government procurement —
   there is now regulatory demand for exactly this type of credential.

### 90-Day Pilot

- **Days 1–30**: 500 workers, 2 contractor clients, Hindi + Marathi, 3 skill domains
- **Days 31–60**: Measure time-to-hire improvement; recruiter NPS; worker
  re-engagement rate. Target: 60% of hired workers had a Bharat Score.
- **Days 61–90**: Add 2 more languages, 10 more skill domains; launch ₹49
  pay-per-verify; integrate score link into Redrob candidate card.

---

## F · Pitch Deck

**File:** `pitch/bharat_score_pitch.pdf` (14 slides)

**Slide structure:**
1. Title
2. About the Builder (team intro)
3. The Problem — 450M invisible workers
4. The Insight — Voice as universal interface
5. Introducing Bharat Score (WhatsApp demo mockup)
6. How It Works — 5-step pipeline
7. The AI Assessment — what we measure
8. Why Now — three tailwinds
9. Market Sizing
10. Competitive Moat
11. Redrob AI Fit
12. Go-to-Market: 90-day pilot
13. The Ask
14. Summary + Contact

---

## G · Track 3 Social Media Challenge (closes June 28 — URGENT)

Track 3 closes in **2 days**. This is the easiest track to enter — just post on
social media about AI/hiring. It has 200 "Participation Reward" prizes at ₹1.5L each.

**What to post (pick one or more):**

Option 1 — LinkedIn post:
```
I just built an AI ranker that scored 100,000 candidate profiles in 58 seconds
for @Redrob AI's India Runs Hackathon.

Here's what I learned about finding India's best ML engineers at scale:

→ Job titles lie. "AI Research Engineer" at a product startup ≠ a researcher.
  Career descriptions tell the real story.
→ The hardest signal: has someone actually shipped a search/ranking system to
  real users? Keywords like "NDCG", "learning-to-rank", "BM25", "latency" don't
  appear in synthetic resumes.
→ Behavioral signals (open-to-work, response rate, notice period) matter as
  much as skills — a 10x engineer with 90-day notice beats the 8x engineer
  who can join Monday.

Built in pure Python, no GPU, no embeddings. Just signal extraction at scale.

The future of hiring isn't ChatGPT writing JDs — it's AI that reads what
candidates actually built and surfaces the ones who shipped.

#IndiaRuns #RedrobiAI #Hack2Skill #AIHiring #MachineLearning
```

Option 2 — Twitter/X thread about Bharat Score idea.

**Hashtags to use:** #IndiaRuns #RedrobiAI #Hack2Skill

**Tag:** @redrob_ai @hack2skill (or search their actual handles)

After posting, submit the post link on the Hack2Skill portal for Track 3.
