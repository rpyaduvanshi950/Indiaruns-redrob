#!/usr/bin/env python3
"""
Main ranker for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

Usage:
    python rank.py --candidates ../data/candidates.jsonl --out ../submission/submission.csv

Constraints (from submission_spec):
    - Must complete in ≤5 minutes on CPU with 16GB RAM
    - No network calls during ranking
    - No GPU

Strategy:
    Pure rule-based scoring with pre-defined skill taxonomy and behavioral
    multiplier. Runs 100K candidates in ~20-40 seconds on a modern CPU.
    No embeddings or model inference needed during ranking.
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

# Make src imports work whether called from src/ or repo root
sys.path.insert(0, str(Path(__file__).parent))

from honeypot import is_honeypot
from scoring import composite_score, generate_reasoning


def load_candidates(path: str) -> list[dict]:
    candidates = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                candidates.append(json.loads(line))
    return candidates


def rank_candidates(candidates: list[dict]) -> list[dict]:
    """Score all candidates, flag honeypots, return sorted list."""
    results = []
    honeypot_count = 0

    for c in candidates:
        flagged, hp_reasons = is_honeypot(c)

        if flagged:
            final_score = 0.0
            components = {"final": 0.0, "honeypot_reasons": hp_reasons}
            honeypot_count += 1
        else:
            final_score, components = composite_score(c)

        results.append({
            "candidate": c,
            "score": final_score,
            "components": components,
            "is_honeypot": flagged,
        })

    print(f"  Flagged {honeypot_count} honeypot candidates (score forced to 0)")

    # Sort by raw score descending (no clipping — full differentiation),
    # then candidate_id ascending for deterministic tie-breaking per spec.
    results.sort(key=lambda x: (-x["score"], x["candidate"]["candidate_id"]))
    return results


def _normalise_scores(ranked: list[dict]) -> None:
    """
    Linearly rescale raw scores for the top 100 into [0.2000, 0.9920].
    Rank order is already determined; this only affects the CSV score column.
    Equal raw scores map to equal normalised scores (ties preserved).
    """
    top100 = ranked[:100]
    hi = top100[0]["score"]
    lo = top100[-1]["score"]
    span = hi - lo if hi != lo else 1.0
    out_hi, out_lo = 0.9920, 0.2000
    for entry in top100:
        norm = out_lo + (entry["score"] - lo) / span * (out_hi - out_lo)
        entry["score_rounded"] = round(norm, 4)


def write_submission(ranked: list[dict], out_path: str, team_id: str = "submission") -> None:
    """Write top 100 to CSV matching the submission spec exactly."""
    top100 = ranked[:100]
    _normalise_scores(ranked)  # sets score_rounded on top 100 in-place

    # Verify score is non-increasing (spec requirement)
    scores = [r["score_rounded"] for r in top100]
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1], f"Score inversion at rank {i+1} vs {i+2}"

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])

        for rank, entry in enumerate(top100, start=1):
            c = entry["candidate"]
            cid = c["candidate_id"]
            score = entry["score_rounded"]
            reasoning = generate_reasoning(c, entry["components"])
            writer.writerow([cid, rank, score, reasoning])

    print(f"  Written {len(top100)} rows → {out_path}")


def print_top_n(ranked: list[dict], n: int = 20) -> None:
    """Print a human-readable summary of the top N candidates."""
    print(f"\n{'='*90}")
    print(f"{'RANK':<5} {'SCORE':<7} {'CANDIDATE_ID':<14} {'TITLE':<38} {'YOE':<5} {'LOC'}")
    print(f"{'='*90}")
    for rank, entry in enumerate(ranked[:n], start=1):
        c = entry["candidate"]
        p = c["profile"]
        comp = entry["components"]
        role_s  = comp.get("role", 0)
        skill_s = comp.get("skills", 0)
        exp_s   = comp.get("experience", 0)
        bm      = comp.get("behavioral_mult", 0)
        title = p["current_title"][:37]
        loc = f"{p.get('location','')[:15]}, {p.get('country','')[:6]}"
        print(
            f"{rank:<5} {entry['score']:<7.4f} {c['candidate_id']:<14} "
            f"{title:<38} {p['years_of_experience']:<5.1f} {loc}"
        )
        print(
            f"      role={role_s:.3f} skills={skill_s:.3f} exp={exp_s:.3f} bm={bm:.3f}"
            + (f"  [HONEYPOT-but-scored?]" if entry["is_honeypot"] else "")
        )
    print(f"{'='*90}\n")


def main():
    parser = argparse.ArgumentParser(description="Redrob candidate ranker")
    parser.add_argument(
        "--candidates",
        default="../data/candidates.jsonl",
        help="Path to candidates.jsonl",
    )
    parser.add_argument(
        "--out",
        default="../submission/submission.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--team-id",
        default="submission",
        help="Team ID for filename (used in output path only)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top candidates to print (default 20)",
    )
    args = parser.parse_args()

    t0 = time.time()

    print(f"[1/4] Loading candidates from {args.candidates} ...")
    candidates = load_candidates(args.candidates)
    print(f"  Loaded {len(candidates):,} candidates  ({time.time()-t0:.1f}s)")

    t1 = time.time()
    print(f"[2/4] Scoring all candidates ...")
    ranked = rank_candidates(candidates)
    print(f"  Scored {len(ranked):,} candidates  ({time.time()-t1:.1f}s)")

    print(f"[3/4] Top {args.top} candidates:")
    print_top_n(ranked, n=args.top)

    print(f"[4/4] Writing submission CSV ...")
    out_path = args.out
    if args.team_id != "submission":
        out_path = str(Path(args.out).parent / f"{args.team_id}.csv")
    write_submission(ranked, out_path)

    total = time.time() - t0
    print(f"\nDone in {total:.1f}s  (limit: 300s)")
    if total > 300:
        print("WARNING: exceeded 5-minute compute budget!")
    else:
        print(f"Budget remaining: {300 - total:.0f}s")


if __name__ == "__main__":
    main()
