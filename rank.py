#!/usr/bin/env python3
"""
Root-level entry point for the SignalSutra ranker.

Usage (from repo root):
    python rank.py --candidates track1_data_ai/data/candidates.jsonl \
                   --out submission.csv

Delegates to track1_data_ai/src/rank.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "track1_data_ai" / "src"))

from rank import main

if __name__ == "__main__":
    main()
