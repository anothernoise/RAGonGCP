"""Chainlit demo app for the RAGonGCP API.

Run with:
  uv run --extra demo chainlit run examples/chainlit_app.py --watch

Environment variables:
  RAG_API_URL           (default: http://localhost:8080)
  RAG_DEMO_DOCS         (default: examples/sample_docs.json)
  RAG_DEMO_AUTO_INGEST  (default: true)
  RAG_DEMO_TOP_K        (optional int)
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import chainlit as cl
import httpx

API_URL = os.getenv("RAG_API_URL", "http://localhost:8080").rstrip("/")
DOCS_PATH = Path(os.getenv("RAG_DEMO_DOCS", "examples/sample_docs.json"))
AUTO_INGEST = os.getenv("RAG_DEMO_AUTO_INGEST", "true").lower() in {"1", "true", "yes", "on"}
TOP_K_RAW = os.getenv("RAG_DEMO_TOP_K", "").strip()
TOP_K = int(TOP_K_RAW) if TOP_K_RAW else None


def _build_ingest_documents(path: Path) -> list[dict[str, Any]]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("Sample docs JSON must contain a list of document objects.")

    docs: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Document #{i} is not a JSON object.")
        uri = row.get("uri")
        text = row.get("text")
        if not uri or not text:
            raise ValueError(f"Document #{i} must include non-empty 'uri' and 'text'.")
        docs.append(
            {
                "uri": uri,
                "title": row.get("title"),
                "mime_type": row.get("mime_type", "text/plain"),
                "metadata": {"text": text},
            }
        )
    return docs


async def _ingest_sample_docs() -> str:
    docs = _build_ingest_documents(DOCS_PATH)
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{API_URL}/ingest", json={"documents": docs})
        resp.raise_for_status()
        body = resp.json()
    return f"Imported {body['imported']} docs into {body['corpus']}."


def _format_citations(citations: list[dict[str, Any]]) -> str:
    if not citations:
        return "_No citations returned._"
    lines = ["### Citations"]
    for c in citations:
        idx = c.get("index")
        title = c.get("title") or c.get("source_uri")
        lines.append(f"- [{idx}] {title}")
    return "\n".join(lines)


@cl.on_chat_start
async def on_chat_start() -> None:
    greeting = (
        "RAGonGCP Chainlit demo is ready.\n\n"
        f"- API: `{API_URL}`\n"
        f"- Auto-ingest sample docs: `{AUTO_INGEST}`\n"
        "- Commands: `/ingest` to reload sample docs, `/help` for tips."
    )
    await cl.Message(content=greeting).send()

    if AUTO_INGEST:
        try:
            msg = await _ingest_sample_docs()
            await cl.Message(content=f"Sample docs ingested. {msg}").send()
        except Exception as exc:
            await cl.Message(content=f"Auto-ingest failed: `{exc}`").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    text = message.content.strip()
    if not text:
        return

    if text.lower() == "/help":
        await cl.Message(
            content=(
                "Ask any question and I will call `/query` on your RAG API.\n\n"
                "Commands:\n"
                "- `/ingest` reload `examples/sample_docs.json`\n"
                "- `/help` show this message\n\n"
                "Useful env vars:\n"
                "- `RAG_API_URL`\n"
                "- `RAG_DEMO_DOCS`\n"
                "- `RAG_DEMO_AUTO_INGEST`\n"
                "- `RAG_DEMO_TOP_K`"
            )
        ).send()
        return

    if text.lower() == "/ingest":
        try:
            msg = await _ingest_sample_docs()
            await cl.Message(content=f"Done. {msg}").send()
        except Exception as exc:
            await cl.Message(content=f"Ingest failed: `{exc}`").send()
        return

    payload: dict[str, Any] = {"question": text}
    if TOP_K is not None:
        payload["top_k"] = TOP_K

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{API_URL}/query", json=payload)
            resp.raise_for_status()
            result = resp.json()
    except Exception as exc:
        await cl.Message(content=f"Query failed: `{exc}`").send()
        return

    answer = result.get("answer", "").strip() or "(empty answer)"
    citations_md = _format_citations(result.get("citations", []))
    model = result.get("model")
    model_line = f"\n\n_Model: `{model}`_" if model else ""
    await cl.Message(content=f"{answer}\n\n{citations_md}{model_line}").send()
