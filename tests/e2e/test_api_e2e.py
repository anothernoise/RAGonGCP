from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from contextlib import contextmanager

import httpx


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@contextmanager
def _run_api_server():
    port = _free_port()
    base_url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env["RAGONGCP_BACKEND"] = "fake"
    env["RAGONGCP_PROFILE"] = "bc_real_estate"

    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "ragongcp.api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_until_healthy(base_url)
        yield base_url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def _wait_until_healthy(base_url: str, timeout_s: float = 10.0) -> None:
    started = time.time()
    while time.time() - started < timeout_s:
        try:
            r = httpx.get(f"{base_url}/healthz", timeout=1)
            if r.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.1)
    raise AssertionError("API server did not become healthy in time")


def test_e2e_healthz_and_query():
    with _run_api_server() as base_url:
        health = httpx.get(f"{base_url}/healthz", timeout=5)
        assert health.status_code == 200
        assert health.json()["backend"] == "fake"

        query = httpx.post(
            f"{base_url}/query",
            json={"question": "What duties does a brokerage owe its clients?"},
            timeout=10,
        )
        assert query.status_code == 200
        body = query.json()
        assert body["answer"]
        assert len(body["citations"]) >= 1


def test_e2e_ingest_then_query_new_document():
    with _run_api_server() as base_url:
        ingest = httpx.post(
            f"{base_url}/ingest",
            json={
                "documents": [
                    {
                        "uri": "sample://e2e/commission-policy",
                        "title": "Commission Policy",
                        "metadata": {
                            "text": (
                                "Brokerage policy states that commission adjustments "
                                "must be approved in writing by the managing broker."
                            )
                        },
                    }
                ]
            },
            timeout=10,
        )
        assert ingest.status_code == 200
        assert ingest.json()["imported"] == 1

        query = httpx.post(
            f"{base_url}/query",
            json={"question": "How must commission adjustments be approved?"},
            timeout=10,
        )
        assert query.status_code == 200
        text = query.json()["answer"].lower()
        assert "approved" in text
        assert "managing broker" in text
