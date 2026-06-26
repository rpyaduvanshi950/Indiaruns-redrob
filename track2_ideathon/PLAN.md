# Track 2 — The Ideathon: Execution Plan
## Creating the Future of AI: An Ideathon Challenge

**Prize:** ₹30 Lakhs total | Track Champion: ₹2L | Runner Up: ₹2L (x2) | Merit: ₹2L (x5)
**Submission closes:** July 2, 2026 | **Evaluation:** July 3–16 | **Finale:** July 22

---

## What You're Submitting

A pitch — a product, strategy, or AI feature that should exist for India. No working code required. Judges want: a clear problem, a believable AI solution, and conviction that you understand the space.

The single question judges ask: **"Is this something Redrob should build?"**

---

## Chosen Pitch: Bharat Score — AI Credentialing for India's Invisible Workforce

### Why This Idea Wins

Redrob's stated mission is: *"An operating system that finally works for the way this country works, hires, learns, and earns."*

Every other team will pitch ideas that improve talent acquisition for English-speaking, LinkedIn-active, tier-1 city candidates — because that's the dataset they just worked with in Track 1. **The gap no one will pitch is the 450 million workers who don't exist in any database at all.**

This idea addresses Redrob's real problem: their platform has 0% coverage of India's informal workforce. Bharat Score creates the coverage.

---

## The Problem (Slide 1-2)

**India's workforce by the numbers:**
- 450M+ workers in the informal/unorganized sector
- 93% of India's total workforce has no verifiable employment record
- Only ~50M Indians have a LinkedIn profile (3.5% of population)
- A mason in Nagpur who has built 40 houses has zero proof of skill that a formal employer can verify
- A BPO worker with 8 years of customer service experience switches roles by word-of-mouth only — no resume, no digital trail

**The recruiter's blind spot:**
Platforms like Redrob, Naukri, LinkedIn operate on profiles. No profile = no discovery. Result: India's largest talent pool is invisible to companies that want to hire them. This isn't a niche problem — it's the central problem of Indian talent markets.

**Why existing solutions fail:**
- Resume builders require literacy and internet access
- LinkedIn requires a professional mindset to self-brand
- Skill assessments require sitting at a computer
- All of these assume the candidate already has a digital identity

---

## The Solution (Slide 3-4)

### Bharat Score: A WhatsApp-native AI that creates verifiable skill credentials via voice

**How it works (user journey, 10 minutes, zero friction):**

1. **Entry via WhatsApp** — Candidate receives or scans a link. Opens WhatsApp (used by 500M Indians, including informal workers).
2. **Language selection** — Choose from 12 Indian languages. The rest of the interaction is in that language.
3. **Voice-based skill assessment** — AI asks 8–12 spoken questions tailored to the claimed skill. For a driver: "Tell me about a time you handled an emergency on the road." For a welder: "Walk me through how you prepare a metal joint for TIG welding."
4. **Verification layer** — AI cross-checks answers for internal consistency. Asks follow-up questions on inconsistencies. Detects coached/memorized responses.
5. **Bharat Score generated** — A structured credential: skill name, verified proficiency level (1–5), confidence score, language of assessment, timestamp.
6. **Profile card created** — A shareable digital card (WhatsApp-shareable) that employers can scan to view verified skills. No English required. No resume required.

**What makes it AI (not just a questionnaire):**
- NLP in Indian languages: intent extraction, consistency checking, fluency-adjusted scoring
- Voice activity detection for low-signal audio (noisy construction sites, markets)
- Adaptive questioning: follow-up questions based on answers, not a fixed script
- Fraud detection: cross-checks claimed experience against time-in-role signals and answer patterns

---

## Why AI + Why Now (Slide 5)

**Three things became true in 2024–2025 that make this buildable:**

1. **Indian language LLMs are good enough** — Models like Sarvam AI, Krutrim, and multilingual fine-tunes of Llama/Mistral now handle Hindi, Tamil, Bengali, Marathi at conversational quality
2. **WhatsApp Business API is mature** — End-to-end voice + text flows are possible without a custom app. Zero install friction.
3. **Structured voice assessment + LLM scoring is a solved sub-problem** — The hard part is Indian language understanding + domain-specific rubrics, not the assessment framework itself

**Why no one has built this yet:**
- It requires deep integration of Indian language models + voice pipelines + domain knowledge bases
- The TAM wasn't clear until ONDC and PM Vishwakarma pushed formalization of informal workers
- Pure tech companies don't understand informal workforce needs; social sector orgs don't build AI

---

## Product Architecture (Slide 6, high-level)

```
Candidate (WhatsApp)
        │
        ▼
WhatsApp Business API
        │
        ▼
Conversation Engine (LangGraph / state machine)
  ├── Language Detection + TTS/STT (Sarvam AI / Azure Cognitive)
  ├── Assessment Question Generator (LLM, domain-tuned)
  ├── Answer Evaluator (LLM scoring rubric per skill domain)
  └── Fraud/Consistency Detector
        │
        ▼
Bharat Score Generator
  ├── Proficiency level (1–5) per claimed skill
  ├── Confidence score (0–1)
  └── Verified timestamp + language flag
        │
        ▼
Redrob Candidate Pool
  └── New "unorganized sector" segment with verified Bharat Scores
        │
        ▼
Recruiter Dashboard
  └── Filter by Bharat Score when LinkedIn/resume data is unavailable
```

---

## Business Model (Slide 7)

**Who pays, and how much:**

| Revenue stream | Mechanism | Est. unit economics |
|---|---|---|
| Employer verification | Company pays ₹50 per Bharat Score verification when hiring | ₹50/hire × 10M hires/yr = ₹500Cr TAM |
| Government / skilling partnerships | NSDC, PM Vishwakarma, PMKVY pay per assessment to digitize workers | ₹30/assessment, bulk contracts |
| Redrob platform premium | Companies pay a premium to access verified informal-sector talent pool | Subscription layer on existing Redrob pricing |
| Candidate score renewal | Yearly re-assessment to keep scores current | ₹0 for candidate (employer-funded) |

**Why this is a defensible moat for Redrob:**
- Every Bharat Score assessment trains Redrob's domain models
- The scored candidate database is exclusive — not replicable by Naukri/LinkedIn in the informal segment
- Network effects: more assessments → better rubrics → higher confidence scores → more employer trust

---

## The Ask / Next Step (Slide 8)

Winning this ideathon gives us:
- ₹2L seed to build the first MVP: WhatsApp bot + Hindi assessment for 3 skill domains (driving, construction, customer service)
- Redrob platform access to test with 100 real employers
- Credit and collaboration on Redrob's product roadmap if the idea is integrated

**6-month roadmap post-win:**
1. Month 1-2: Build WhatsApp bot + Hindi STT/TTS pipeline + 3 skill rubrics
2. Month 3: Pilot with 500 candidates via NSDC partner NGO
3. Month 4-5: Refine scoring model, add 10 more skill domains
4. Month 6: Present employer-verified success cases, pitch government skilling bodies

---

## Pitch Deck Outline (for `pitch/` folder)

```
Slide 1: The Hook       — "450M workers. Zero digital proof. One WhatsApp message away."
Slide 2: The Problem    — India's invisible workforce + recruiter blind spot (data, numbers)
Slide 3: The Solution   — Bharat Score overview, user journey in 4 steps
Slide 4: The Demo Flow  — Mockup of WhatsApp conversation (screenshots or wireframes)
Slide 5: Why Now        — Indian LLMs + WhatsApp API + formalization push
Slide 6: Architecture   — Simple diagram (not deep technical)
Slide 7: Business Model — Who pays, how much, why Redrob wins
Slide 8: The Ask        — What winning enables, 6-month plan
```

Keep each slide to ONE idea. No bullets walls. Use visuals where possible.

---

## Backup Pitch: AI for India's Non-Linear Careers

If Bharat Score feels too infrastructural, this is the second-strongest idea:

**Problem:** Standard ATS systems penalize India's non-linear career paths. A candidate who took 2 years off to care for parents, then rejoined in a different role, then moved cities for a spouse's job — looks like a red flag to keyword-based screening. This is culturally specific to India (joint families, arranged marriages, tier-2 to tier-1 migration).

**Solution:** A career-context AI that reads a career timeline and identifies the *reason* for non-linearity from patterns and optional self-reported context, then translates it into a neutral, skills-based score that removes cultural bias from screening.

**Why this is weaker than Bharat Score:** It improves existing coverage but doesn't expand Redrob's TAM. Bharat Score is a bigger strategic bet.

---

## Submission Checklist

- [ ] Pitch deck (8 slides, PDF or Google Slides link)
- [ ] One-paragraph summary (for submission form)
- [ ] Problem statement with at least 2 real statistics
- [ ] Clear explanation of how AI is essential (not optional) to the solution
- [ ] Business model: who pays
- [ ] Team intro slide (optional but recommended)
- [ ] Submit via Hack2Skill portal before July 2, 2026

---

## What Wins vs. What Loses

| Winners | Losers |
|---|---|
| Specific Indian problem with real numbers | Vague "AI will help hiring" pitch |
| Explains WHY AI (not just "we'll use AI") | AI is a black box in the pitch |
| Aligns with Redrob's actual business | Generic SaaS idea unrelated to talent |
| Shows you understand the user (informal worker) | Assumes all users are LinkedIn-active |
| Clear business model | "We'll figure out monetization later" |
| 8 tight slides | 20-slide deck trying to cover everything |
