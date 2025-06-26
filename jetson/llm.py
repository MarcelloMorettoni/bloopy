"""Local and remote LLM interface for Bloopy.

This module uses ``ollama`` to run a local Llama 3.3 model. If local
inference fails or the system is under heavy load, it falls back to an
external LLM service via HTTP. The external service URL should be
configured in the ``REMOTE_API_URL`` environment variable.
"""

from __future__ import annotations

import os
import subprocess
from typing import Optional

try:
    import requests
except Exception:  # pragma: no cover - requests may not be installed
    requests = None  # type: ignore

LOCAL_MODEL = "llama3.3"
REMOTE_API_URL = os.environ.get("REMOTE_API_URL", "http://example.com/api")


def _run_ollama(prompt: str, timeout: int = 60) -> str:
    """Run the prompt through ``ollama`` using the local model."""
    result = subprocess.run(
        ["ollama", "run", LOCAL_MODEL, prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout.strip()


def _run_remote(prompt: str, timeout: int = 30) -> str:
    """Send the prompt to the remote LLM service."""
    if requests is None:
        raise RuntimeError("requests library not available")
    resp = requests.post(REMOTE_API_URL, json={"prompt": prompt}, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "")


def generate_response(prompt: str) -> str:
    """Generate a response using the local model with remote fallback."""
    try:
        return _run_ollama(prompt)
    except Exception:
        try:
            return _run_remote(prompt)
        except Exception as exc:
            return f"Error contacting LLM: {exc}"
