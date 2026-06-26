"""
Streamlit sandbox for the Redrob Intelligent Candidate Discovery & Ranking system.

Submission spec (Section 10.5): sandbox must accept ≤100 candidates, run the
ranker end-to-end, and produce a ranked CSV — all within the 5-minute CPU budget.

Deploy on Streamlit Community Cloud:
  Main file path: track1_data_ai/app.py
  Requirements:   track1_data_ai/requirements.txt
"""

import csv
import io
import json
import sys
import time
from pathlib import Path

import streamlit as st

# ── path setup so src/ imports work from any CWD ─────────────────────────────
_ROOT = Path(__file__).parent
sys.path.insert(0, str(_ROOT / "src"))

from honeypot import is_honeypot
from scoring import composite_score, generate_reasoning

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SignalSutra — Candidate Ranker",
    page_icon="🎯",
    layout="wide",
)

# ── session state — candidates must survive the rerender triggered by "Run ranker"
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "source_label" not in st.session_state:
    st.session_state.source_label = ""

# ── header ────────────────────────────────────────────────────────────────────
st.title("🎯 SignalSutra — Intelligent Candidate Ranker")
st.caption(
    "India Runs Hackathon · Track 1 · Redrob AI  |  "
    "Ranks candidates for the Senior AI Engineer role using multi-signal scoring."
)
st.divider()

# ── sidebar: how it works ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("How it works")
    st.markdown("""
**6 scoring components:**

| Component | Weight |
|---|---|
| Role relevance | 25% |
| Skills match | 25% |
| Career descriptions | 20% |
| Experience quality | 15% |
| Location | 10% |
| Notice period | 5% |

**Career descriptions** — keyword analysis of what the candidate actually built:
production-deployment signals, retrieval/search/ranking work, LLM fine-tuning.
The JD's hardest check: *"Has shipped at least one end-to-end ranking/search/rec
system to real users."*

**Behavioural multiplier:** ×0.50–1.25
Activity recency · OTW flag · Response rate
Interview completion · GitHub · Profile completeness

**Honeypot detection:**
Duration mismatch · Expert + 0 months · Too many expert skills → forced to 0

**Runtime:** ~58 s for 100 K candidates on CPU.
No GPU · No network · No external packages for the ranker.
    """)
    st.divider()
    st.markdown("**Reproduce locally:**")
    st.code(
        "python rank.py \\\n"
        "  --candidates track1_data_ai/data/candidates.jsonl \\\n"
        "  --out submission.csv",
        language="bash",
    )

# ── 1 · Load candidates ───────────────────────────────────────────────────────
st.subheader("1 · Load candidates")

col_upload, col_sample = st.columns([3, 2])

with col_upload:
    uploaded = st.file_uploader(
        "Upload a JSONL file (one candidate per line, max 100 candidates)",
        type=["jsonl", "json"],
        help="Format: one JSON object per line, matching the Redrob candidate schema.",
    )

with col_sample:
    st.markdown("&nbsp;")
    use_sample = st.button("Use built-in sample (50 candidates)", use_container_width=True)

# ── populate session state when a source is chosen ───────────────────────────
if uploaded is not None:
    raw = uploaded.read().decode("utf-8").strip()
    parsed = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            st.error(f"Could not parse line: {line[:80]}…")
            st.stop()
    if len(parsed) > 100:
        st.warning(f"Truncating {len(parsed)} → 100 candidates (sandbox limit).")
        parsed = parsed[:100]
    st.session_state.candidates = parsed
    st.session_state.source_label = f"uploaded file · {len(parsed)} candidates"

elif use_sample:
    sample_path = _ROOT / "data" / "sample_candidates.json"
    if not sample_path.exists():
        st.error("sample_candidates.json not found in the repo. Please upload a JSONL file.")
        st.stop()
    with open(sample_path) as f:
        loaded = json.load(f)
    st.session_state.candidates = loaded
    st.session_state.source_label = f"built-in sample · {len(loaded)} candidates"

# ── read from session state (survives the rerender triggered by "Run ranker") ─
candidates = st.session_state.candidates

if candidates:
    st.success(f"✓ Loaded — {st.session_state.source_label}")

# ── 2 · Rank ──────────────────────────────────────────────────────────────────
if candidates:
    st.divider()
    st.subheader("2 · Rank")

    if st.button("▶  Run ranker", type="primary", use_container_width=True):
        t0 = time.time()

        results = []
        hp_count = 0
        progress = st.progress(0, text="Scoring candidates…")

        for i, c in enumerate(candidates):
            flagged, reasons = is_honeypot(c)
            if flagged:
                score = 0.0
                components = {"final": 0.0, "honeypot_reasons": reasons}
                hp_count += 1
            else:
                score, components = composite_score(c)

            results.append({
                "candidate": c,
                "score": score,
                "components": components,
                "is_honeypot": flagged,
            })
            progress.progress(
                (i + 1) / len(candidates),
                text=f"Scored {i + 1}/{len(candidates)}",
            )

        progress.empty()

        # Sort: descending score, ascending candidate_id for ties
        results.sort(key=lambda x: (-x["score"], x["candidate"]["candidate_id"]))

        # Normalise top-N scores to [0.20, 0.992]
        top_n = min(100, len(results))
        top = results[:top_n]
        hi, lo = top[0]["score"], top[-1]["score"]
        span = hi - lo if hi != lo else 1.0
        for entry in top:
            entry["score_out"] = round(
                0.20 + (entry["score"] - lo) / span * (0.992 - 0.20), 4
            )

        elapsed = time.time() - t0

        # ── metrics ──────────────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Candidates scored", len(candidates))
        m2.metric("Honeypots detected", hp_count)
        m3.metric("Showing top", top_n)
        m4.metric("Runtime", f"{elapsed:.1f}s")

        st.divider()
        st.subheader("3 · Results")

        # ── table ─────────────────────────────────────────────────────────────
        table_rows = []
        csv_rows = []

        for rank, entry in enumerate(top, start=1):
            c = entry["candidate"]
            p = c["profile"]
            sig = c["redrob_signals"]
            comp = entry["components"]
            reasoning = generate_reasoning(c, comp)

            hp_flag = "🚨" if entry["is_honeypot"] else ""
            table_rows.append({
                "Rank": rank,
                "Score": entry["score_out"],
                "": hp_flag,
                "ID": c["candidate_id"],
                "Title": p["current_title"],
                "YoE": p["years_of_experience"],
                "Location": f"{p.get('location', '')}, {p.get('country', '')}",
                "OTW": "✓" if sig.get("open_to_work_flag") else "—",
                "Resp %": f"{sig.get('recruiter_response_rate', 0) * 100:.0f}%",
                "Notice (d)": sig.get("notice_period_days", "—"),
                "Reasoning": reasoning,
            })
            csv_rows.append([c["candidate_id"], rank, entry["score_out"], reasoning])

        st.dataframe(
            table_rows,
            use_container_width=True,
            height=600,
            column_config={
                "Rank": st.column_config.NumberColumn(width="small"),
                "Score": st.column_config.NumberColumn(format="%.4f", width="small"),
                "": st.column_config.TextColumn(width="small"),
                "YoE": st.column_config.NumberColumn(format="%.1f", width="small"),
                "OTW": st.column_config.TextColumn(width="small"),
                "Resp %": st.column_config.TextColumn(width="small"),
                "Notice (d)": st.column_config.NumberColumn(width="small"),
                "Reasoning": st.column_config.TextColumn(width="large"),
            },
        )

        # ── CSV download ──────────────────────────────────────────────────────
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        writer.writerows(csv_rows)

        st.download_button(
            label="⬇  Download submission.csv",
            data=buf.getvalue().encode("utf-8"),
            file_name="submission.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary",
        )

        # ── score distribution ────────────────────────────────────────────────
        with st.expander("Score distribution"):
            st.bar_chart(
                {"Score": [r["score_out"] for r in top]},
                x_label="Rank",
                y_label="Score",
            )

        # ── component breakdown for top 10 ────────────────────────────────────
        with st.expander("Component breakdown — top 10"):
            breakdown = []
            for entry in top[:10]:
                comp = entry["components"]
                c = entry["candidate"]
                breakdown.append({
                    "ID": c["candidate_id"],
                    "Title": c["profile"]["current_title"][:28],
                    "Role": round(comp.get("role", 0), 3),
                    "Skills": round(comp.get("skills", 0), 3),
                    "Desc": round(comp.get("career_desc", 0), 3),
                    "Exp": round(comp.get("experience", 0), 3),
                    "Loc": round(comp.get("location", 0), 3),
                    "Notice": round(comp.get("notice", 0), 3),
                    "Beh×": round(comp.get("behavioral_mult", 0), 3),
                    "Final": round(entry["score_out"], 4),
                })
            st.dataframe(breakdown, use_container_width=True)

else:
    st.info("Upload a JSONL file or click **Use built-in sample** to get started.")
