---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Inter', sans-serif;
    background: #0f172a;
    color: #f1f5f9;
  }
  h1 { color: #38bdf8; font-size: 2.2rem; }
  h2 { color: #7dd3fc; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; }
  h3 { color: #bae6fd; }
  strong { color: #fbbf24; }
  em { color: #a5f3fc; }
  table { border-collapse: collapse; width: 100%; }
  th { background: #1e3a5f; color: #38bdf8; padding: 10px; }
  td { padding: 10px; border: 1px solid #334155; }
  blockquote { background: #1e293b; border-left: 4px solid #38bdf8; padding: 16px 20px; border-radius: 4px; margin: 12px 0; }
  blockquote p { margin: 0; }
  code { background: #1e293b; color: #7dd3fc; }
  pre { background: #1e293b; padding: 16px; border-radius: 6px; border: 1px solid #334155; }
---

# Bharat Score
## AI-Powered Work Credentials for India's Invisible Workforce

**Team SignalSutra** | India Runs Hackathon · Track 2 Ideathon
Redrob AI × Hack2Skill · June 2026

---

## About the Builder

**Pushpender**
ML Engineer · India Runs Hackathon Participant

- Built the **Track 1 AI ranker** — scoring 100K candidate profiles for Redrob's Senior AI Engineer role using multi-signal ML scoring
- From that work: *the hardest problem is not ranking candidates who have profiles — it's that 93% of India's workforce has no profile at all*
- **Bharat Score** is the direct upstream solution: create the structured data that Redrob's ranker then uses

> *"I built the ranking engine. Now I'm building the input."*

**Contact:** rpyaduvanshi950@gmail.com | +91-9257009192

---

## The Problem: 450 Million Workers Without a Verifiable Identity

India's informal sector is **the world's largest unverified talent pool.**

- **450M** informal workers — daily wage, gig, small-trade, migrant
- **93%** of India's workforce has no verifiable employment record
- **Only 50M** Indians have a LinkedIn profile (3.5% of 1.4B population)
- A mason who built an airport cannot prove it to get his next contract
- A data-entry worker in Patna applies to a BPO in Pune — recruiter sees a blank profile

> **Recruiters spend 40% of screening time trying to verify claims they can't actually verify.**
> The result: good workers are invisible and bad claims go unchallenged.

---

## The Insight: Voice Is the Universal Interface

**91% of India's mobile users access the internet primarily through voice or video.**
WhatsApp has **500M+ active users in India** — including workers with no email address.

We don't need to build a new app.
We need to meet workers **where they already are.**

The credential system that works for India must be:
- **Voice-first** — not form-first
- **Vernacular** — 12 Indian languages, not just English
- **Zero-friction** — no app download, no account creation
- **Instantly verifiable** — a QR code that any recruiter can scan right now

---

## Introducing Bharat Score

### One WhatsApp conversation → a verified work credential

```
Worker texts "SCORE" to +91-XXXX-XXXXXX

Redrob AI bot responds in their language:
  "Namaste! Main aapka kaam ka certificate banaunga.
   Aap kya kaam karte hain?"

[5-minute voice/text conversation]

Worker receives a shareable link:
  bharat.score/w/RJ-MASON-2847
  ┌─────────────────────────────┐
  │  Ramesh Jatav               │
  │  ⭐⭐⭐⭐ Mason – Level 4   │
  │  12yr · RCC + Tiling        │
  │  Verified: 3 employers      │
  │  Last active: June 2026     │
  └─────────────────────────────┘
```

Recruiter scans QR. Credential loads in 2 seconds.

---

## How It Works: The 5-Step Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. INTAKE   │────▶│  2. ASSESS   │────▶│  3. VERIFY   │
│              │     │              │     │              │
│ Worker texts │     │ AI conducts  │     │ Employer SMS │
│ WhatsApp     │     │ 5-min voice  │     │ verification │
│ in any lang  │     │ assessment   │     │ loop         │
└──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                              ┌───────────────────┘
                              ▼
                    ┌──────────────┐     ┌──────────────┐
                    │  4. SCORE    │────▶│  5. PUBLISH  │
                    │              │     │              │
                    │ Bharat Score │     │ Shareable    │
                    │ 0–100 + tier │     │ QR link +    │
                    │ computed     │     │ Redrob index │
                    └──────────────┘     └──────────────┘
```

**No human in the loop. End-to-end: 8 minutes.**

---

## The AI Assessment: What We Actually Measure

**Not a quiz. A conversation.**

The AI adapts questions based on the claimed role:

| For a Mason | For a Delivery Driver | For a Data Entry Worker |
|---|---|---|
| "Cement-to-sand ratio for RCC?" | "What do you do if a parcel is wet?" | "How many invoices per hour?" |
| "How do you check plumb line?" | "Describe your GPS app workflow" | "Which Excel formula for totals?" |
| Employer contacts (spoken) | GSTIN/license number | Typing speed (live test) |

**Bharat Score = 0.40 × skill assessment + 0.35 × verified tenure + 0.25 × employer ratings**

Scores update with each verified credential. **It's a living document, not a snapshot.**

---

## Why Now: Three Tailwinds Converging

### 1. WhatsApp Business API opened to developers (2023)
Any verified business can now build conversational flows — no special access needed.

### 2. Indic LLMs have crossed the viability threshold
**Sarvam AI's Saaras** (Hindi/Tamil/Telugu), **AI4Bharat's IndicBERT**, and
**OpenAI Whisper** (12 Indian language transcription) all run at production quality.

### 3. ONDC + PMKVY-3.0 created the demand signal
Government procurement rules now **require skill certificates** for contractors.
MSME owners need credentials to bid for government projects.
The demand is there. The supply (verifiable credentials) is not.

---

## Market Sizing

```
India's informal workforce addressable universe:

450M workers × 30% smartphone + WhatsApp penetration
= 135M addressable workers

Target Year 1:  2M credentialed workers (1.5% penetration)
Target Year 3: 20M credentialed workers

Revenue model: B2B2C
  ├── Recruiter seat access:   ₹2,000/month per seat (ATS integration)
  ├── Background verification: ₹49/check (pay-per-use)
  └── Premium worker profile:  ₹99/year

Year 3 blended ARR potential: ₹80–120 Cr
(20M workers × blended ARPU + recruiter seats)
```

---

## Competitive Moat

| What exists today | What Bharat Score adds |
|---|---|
| LinkedIn — English, degree-focused | Vernacular, skill-work-focused |
| NSDC / PMKVY — one-time certificate | Dynamic score that updates with work history |
| CIBIL / credit score — financial only | Work reputation score |
| Reference checks — slow, biased | AI-structured, consistent, instant |
| Springworks / Keka — corporate HR | Informal sector, zero-infrastructure |

**The moat is the data flywheel:**
More credentialed workers → more recruiter trust → more workers self-credential
→ richer assessment benchmarks → better scores → more recruiter trust.

Early entrant advantage is decisive in a trust network.

---

## Redrob AI Fit

Bharat Score is **a direct extension of Redrob's core product:**

| Redrob today | Bharat Score adds |
|---|---|
| Ranks candidates from structured profiles | Generates structured profiles from unstructured workers |
| Serves corporate recruiters | Expands TAM to informal sector (contractors, MSMEs) |
| 100K structured candidate pool | +135M previously invisible workers |
| Signals: skills, experience, OTW flag | New signal: verified tenure + employer rating |

**This is not a pivot. It's the same ranking engine applied one layer upstream —
creating the structured data that Redrob's ranker then uses.**

Redrob's existing signals (OTW flag, response rate, interview completion)
map directly onto Bharat Score's engagement signals.

---

## Go-to-Market: 90-Day Pilot Plan

### Phase 1 — Pilot (Days 1–30)
- Partner with **2 construction contractors** in Noida/Pune (Redrob's home base)
- Credential **500 workers** in Hindi + Marathi
- Provide **free recruiter access** to 10 early-adopter MSMEs

### Phase 2 — Validate (Days 31–60)
- Measure: time-to-hire, recruiter NPS, worker re-engagement rate
- Target: 60% of hired workers had a Bharat Score vs. none before
- Instrument: did credentialed workers get hired faster?

### Phase 3 — Scale (Days 61–90)
- Add Tamil + Telugu assessment tracks
- Launch ₹49 pay-per-verify for recruiter background checks
- Integrate Bharat Score link into Redrob candidate card

---

## The Ask

**We are building Bharat Score as an open credentialing layer for India.**

What we need from Redrob AI:
- **API access** to Redrob's candidate signal infrastructure
- **Pilot partnership** with 2–3 of Redrob's enterprise recruiter clients
- **Mentorship** from the Redrob team on recruiter adoption patterns

**What Redrob gets:**
- First-mover position in informal-sector credentialing
- A new upstream data source that makes the existing ranker dramatically more powerful
- A mission that resonates: helping 450M Indians become visible to the economy

> *"The mason built an airport. It's time he could prove it."*

---

## Summary

> **Bharat Score** is a WhatsApp-native AI credentialing system that turns a
> 5-minute voice conversation into a verifiable work credential for India's
> 450M informal workers — in 12 languages, with no app, no CV, no friction.
>
> For the mason, the gig driver, the data-entry worker in Tier-3 India:
> **for the first time, their work has a verifiable record.**
>
> For Redrob: it creates the structured data upstream that makes the existing
> ranker work on the largest untapped talent pool in the world.

---

*Team SignalSutra · India Runs Hackathon · Track 2 Ideathon · June 2026*
*Pushpender · rpyaduvanshi950@gmail.com · +91-9257009192*
*GitHub: github.com/rpyaduvanshi950/Indiaruns-redrob*
