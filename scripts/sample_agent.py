"""Sample RAG agent CLI that talks to the RAGonGCP API.

This is an intentionally small reference app for local demos. It can:
1) optionally ingest a local JSON file of sample documents into `/ingest`
2) run an interactive question loop against `/query`
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import httpx


def _load_sample_docs(path: Path) -> list[dict[str, Any]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Sample docs JSON must be a list of objects.")

    payload_docs = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Document #{i} must be an object.")
        uri = row.get("uri")
        text = row.get("text")
        if not uri or not text:
            raise ValueError(f"Document #{i} must include non-empty 'uri' and 'text'.")
        payload_docs.append(
            {
                "uri": uri,
                "title": row.get("title"),
                "mime_type": row.get("mime_type", "text/plain"),
                "metadata": {"text": text},
            }
        )
    return payload_docs


def ingest_docs(api_base_url: str, docs_path: Path) -> None:
    docs = _load_sample_docs(docs_path)
    with httpx.Client(timeout=30) as client:
        resp = client.post(f"{api_base_url}/ingest", json={"documents": docs})
        resp.raise_for_status()
        body = resp.json()
    print(f"[ingest] imported={body['imported']} corpus={body['corpus']}")


def ask_question(api_base_url: str, question: str, top_k: int | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"question": question}
    if top_k:
        payload["top_k"] = top_k
    with httpx.Client(timeout=60) as client:
        resp = client.post(f"{api_base_url}/query", json=payload)
        resp.raise_for_status()
        return resp.json()


def _print_answer(result: dict[str, Any]) -> None:
    print("\nAgent answer:\n")
    print(result.get("answer", "").strip() or "(empty)")
    citations = result.get("citations", [])
    if citations:
        print("\nCitations:")
        for c in citations:
            idx = c.get("index")
            title = c.get("title") or c.get("source_uri")
            snippet = c.get("snippet") or ""
            print(f"- [{idx}] {title}")
            if snippet:
                print(f"  {snippet}")
    print("")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample RAG agent CLI for RAGonGCP.")
    parser.add_argument(
        "--api-url",
        default="http://localhost:8080",
        help="Base URL of the running RAGonGCP API.",
    )
    parser.add_argument(
        "--docs",
        default="examples/sample_docs.json",
        help="Path to sample docs JSON for optional ingestion.",
    )
    parser.add_argument(
        "--skip-ingest",
        action="store_true",
        help="Skip ingestion step and query existing corpus only.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Optional retrieval top_k override for each query.",
    )
    args = parser.parse_args()

    api_url = args.api_url.rstrip("/")
    docs_path = Path(args.docs)

    if not args.skip_ingest:
        ingest_docs(api_url, docs_path)

    print("RAG sample agent ready. Type a question, or 'exit' to quit.")
    while True:
        try:
            question = input("> ").strip()
        except EOFError:
            print("\nbye")
            return
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("bye")
            return
        try:
            result = ask_question(api_url, question, top_k=args.top_k)
        except httpx.HTTPError as exc:
            print(f"query failed: {exc}")
            continue
        _print_answer(result)


if __name__ == "__main__":
    main()
