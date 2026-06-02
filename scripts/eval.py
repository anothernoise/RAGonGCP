"""Tiny eval harness — run the golden set through the pipeline and report.

Checks, per question, whether the answer is non-empty, carries a citation, and
mentions any expected keyword. Works offline with the fake backend:

    RAGONGCP_BACKEND=fake python scripts/eval.py
    # or against a real corpus once ingested:
    RAGONGCP_PROFILE=bc_real_estate python scripts/eval.py
"""

from __future__ import annotations

import json
from pathlib import Path

from ragongcp.pipeline.rag_service import build_default

GOLDEN = Path(__file__).resolve().parents[1] / "eval" / "golden_set.jsonl"


def main() -> None:
    service = build_default()
    rows = [json.loads(line) for line in GOLDEN.read_text().splitlines() if line.strip()]

    answered = grounded = keyword_hit = 0
    for row in rows:
        answer = service.query(row["question"])
        text = (answer.text or "").lower()
        has_answer = bool(text.strip()) and "i don't know" not in text
        has_citation = len(answer.citations) > 0
        kw = [k.lower() for k in row.get("expected_keywords", [])]
        has_kw = any(k in text for k in kw) if kw else has_answer

        answered += has_answer
        grounded += has_citation
        keyword_hit += has_kw
        mark = "ok " if (has_answer and has_citation) else "   "
        print(f"[{mark}] {row['question'][:70]}")

    n = len(rows)
    print("\n--- summary ---")
    print(f"answered:    {answered}/{n}")
    print(f"grounded:    {grounded}/{n}  (answer carried >=1 citation)")
    print(f"keyword hit: {keyword_hit}/{n}")


if __name__ == "__main__":
    main()
