# Bharat Score — Pitch Deck Content

---

## Page 1 — Title

# Bharat Score
## AI-Powered Work Credentials for India's Invisible Workforce

**Team SignalSutra** | India Runs Hackathon · Track 2 Ideathon
Redrob AI × Hack2Skill · June 2026

---

## Page 2 — About the Builder

**Pushpender**
ML Engineer · India Runs Hackathon Participant

- Built the **Track 1 AI ranker** — scoring 100K candidate profiles for Redrob's Senior AI Engineer role using multi-signal ML scoring
- From that work: the hardest problem is not ranking candidates who have profiles — it's that 93% of India's workforce has no profile at all
- **Bharat Score** is the direct upstream solution: create the structured data that Redrob's ranker then uses

> *"I built the ranking engine. Now I'm building the input."*

**Contact:** rpyaduvanshi950@gmail.com | +91-9257009192

---

## Page 3 — The Problem

**450 Million Workers Without a Verifiable Identity**

India's informal sector is the world's largest unverified talent pool.

- **450M** informal workers — daily wage, gig, small-trade, migrant
- **93%** of India's workforce has no verifiable employment record
- **Only 50M** Indians have a LinkedIn profile (3.5% of 1.4B population)
- A mason who built an airport cannot prove it to get his next contract
- A data-entry worker in Patna applies to a BPO in Pune — recruiter sees a blank profile

> Recruiters spend 40% of screening time trying to verify claims they can't actually verify. The result: good workers are invisible and bad claims go unchallenged.

---

## Page 4 — The Insight

**Voice Is the Universal Interface**

- 91% of India's mobile users access the internet primarily through voice or video
- WhatsApp has 500M+ active users in India — including workers with no email address
- We don't need to build a new app. We need to meet workers where they already are.

The credential system that works for India must be:

- **Voice-first** — not form-first
- **Vernacular** — 12 Indian languages, not just English
- **Zero-friction** — no app download, no account creation
- **Instantly verifiable** — a QR code that any recruiter can scan right now

---

## Page 5 — The Product

**One WhatsApp conversation → a verified work credential**

Worker texts "SCORE" to a number. The Redrob AI bot responds in their language:
*"Namaste! Main aapka kaam ka certificate banaunga. Aap kya kaam karte hain?"*

After a 5-minute voice/text conversation, the worker receives a shareable link:

```
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

## Page 6 — How It Works

**The 5-Step Pipeline**

1. **INTAKE** — Worker texts WhatsApp in any language
2. **ASSESS** — AI conducts a 5-minute adaptive voice assessment
3. **VERIFY** — Employer SMS verification loop
4. **SCORE** — Bharat Score (0–100 + tier) computed
5. **PUBLISH** — Shareable QR link added to Redrob candidate index

No human in the loop. End-to-end: 8 minutes.

---

## Page 7 — The AI Assessment

**Not a quiz. A conversation.**

The AI adapts questions based on the claimed role:

| For a Mason | For a Delivery Driver | For a Data Entry Worker |
|---|---|---|
| Cement-to-sand ratio for RCC? | What do you do if a parcel is wet? | How many invoices per hour? |
| How do you check plumb line? | Describe your GPS app workflow | Which Excel formula for totals? |
| Employer contacts (spoken) | GSTIN/license number | Typing speed (live test) |

**Bharat Score = 0.40 × skill assessment + 0.35 × verified tenure + 0.25 × employer ratings**

Scores update with each new verified credential. It's a living document, not a snapshot.

---

## Page 8 — Why Now

**Three Tailwinds Converging**

**1. WhatsApp Business API opened to developers (2023)**
Any verified business can now build conversational flows — no special access needed.

**2. Indic LLMs have crossed the viability threshold**
Sarvam AI's Saaras (Hindi/Tamil/Telugu), AI4Bharat's IndicBERT, and OpenAI Whisper (12 Indian language transcription) all run at production quality.

**3. ONDC + PMKVY-3.0 created the demand signal**
Government procurement rules now require skill certificates for contractors. MSME owners need credentials to bid for government projects. The demand is there. The supply (verifiable credentials) is not.

---

## Page 9 — Market Sizing

India's informal workforce addressable universe:

- 450M workers × 30% smartphone + WhatsApp penetration = **135M addressable workers**
- Target Year 1: 2M credentialed workers (1.5% penetration)
- Target Year 3: 20M credentialed workers

**Revenue model (B2B2C):**

| Stream | Price | Scale |
|---|---|---|
| Recruiter seat access | ₹2,000/month | Per seat, ATS integration |
| Background verification | ₹49/check | Pay-per-use |
| Premium worker profile | ₹99/year | Worker-side |

**Year 3 blended ARR potential: ₹80–120 Cr**

---

## Page 10 — Competitive Moat

| What exists today | What Bharat Score adds |
|---|---|
| LinkedIn — English, degree-focused | Vernacular, skill-work-focused |
| NSDC / PMKVY — one-time certificate | Dynamic score that updates with work history |
| CIBIL / credit score — financial only | Work reputation score |
| Reference checks — slow, biased | AI-structured, consistent, instant |
| Springworks / Keka — corporate HR only | Informal sector, zero-infrastructure |

**The moat is the data flywheel:**
More credentialed workers → more recruiter trust → more workers self-credential → richer assessment benchmarks → better scores → more recruiter trust.

Early entrant advantage is decisive in a trust network.

---

## Page 11 — Redrob AI Fit

Bharat Score is a direct extension of Redrob's core product:

| Redrob today | Bharat Score adds |
|---|---|
| Ranks candidates from structured profiles | Generates structured profiles from unstructured workers |
| Serves corporate recruiters | Expands TAM to informal sector (contractors, MSMEs) |
| 100K structured candidate pool | +135M previously invisible workers |
| Signals: skills, experience, OTW flag | New signal: verified tenure + employer rating |

This is not a pivot. It's the same ranking engine applied one layer upstream — creating the structured data that Redrob's ranker then uses.

---

## Page 12 — Go-to-Market

**90-Day Pilot Plan**

**Phase 1 — Pilot (Days 1–30)**
- Partner with 2 construction contractors in Noida/Pune
- Credential 500 workers in Hindi + Marathi
- Free recruiter access to 10 early-adopter MSMEs

**Phase 2 — Validate (Days 31–60)**
- Measure: time-to-hire, recruiter NPS, worker re-engagement rate
- Target: 60% of hired workers had a Bharat Score vs. none before

**Phase 3 — Scale (Days 61–90)**
- Add Tamil + Telugu assessment tracks
- Launch ₹49 pay-per-verify for recruiter background checks
- Integrate Bharat Score link into Redrob candidate card

---

## Page 13 — The Ask

We are building Bharat Score as an open credentialing layer for India.

**What we need from Redrob AI:**
- API access to Redrob's candidate signal infrastructure
- Pilot partnership with 2–3 of Redrob's enterprise recruiter clients
- Mentorship from the Redrob team on recruiter adoption patterns

**What Redrob gets:**
- First-mover position in informal-sector credentialing
- A new upstream data source that makes the existing ranker dramatically more powerful
- A mission that resonates: helping 450M Indians become visible to the economy

> *"The mason built an airport. It's time he could prove it."*

---

## Page 14 — Summary

Bharat Score is a WhatsApp-native AI credentialing system that turns a 5-minute voice conversation into a verifiable work credential for India's 450M informal workers — in 12 languages, with no app, no CV, no friction.

For the mason, the gig driver, the data-entry worker in Tier-3 India: **for the first time, their work has a verifiable record.**

For Redrob: it creates the structured data upstream that makes the existing ranker work on the largest untapped talent pool in the world.

---

*Team SignalSutra · India Runs Hackathon · Track 2 Ideathon · June 2026*
*Pushpender · rpyaduvanshi950@gmail.com · +91-9257009192*
*GitHub: github.com/rpyaduvanshi950/Indiaruns-redrob*
