"""
Utility helpers to configure the Qdrant vector store based on environment variables.

Supports different deployment scenarios:
- Local Docker (`QDRANT_HOST`/`QDRANT_PORT`)
- Qdrant Cloud (`QDRANT_URL`/`QDRANT_API_KEY`)
- Embedded Qdrant (`QDRANT_LOCATION`, e.g. ':memory:' or a filesystem path)
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

from datapizza.vectorstores.qdrant import QdrantVectorstore

COLLECTION_NAME = os.getenv("FAQ_COLLECTION_NAME", "datapizza_faq")
EMBEDDING_DIM = int(os.getenv("FAQ_EMBEDDING_DIM", "768"))


def _bool_from_env(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() in {"1", "true", "yes", "on"}


def describe_qdrant_target() -> str:
    """Human-readable description of the configured Qdrant endpoint."""
    location = os.getenv("QDRANT_LOCATION")
    if location:
        return f"embedded Qdrant at '{location}'"

    url = os.getenv("QDRANT_URL")
    if url:
        parsed = urlparse(url)
        host = parsed.hostname or "unknown-host"
        port = parsed.port or ("443" if parsed.scheme == "https" else "80")
        return f"{parsed.scheme or 'http'}://{host}:{port}"

    host = os.getenv("QDRANT_HOST", "localhost")
    port = os.getenv("QDRANT_PORT", "6333")
    scheme = "https" if _bool_from_env(os.getenv("QDRANT_HTTPS")) else "http"
    return f"{scheme}://{host}:{port}"


def build_qdrant_vectorstore() -> QdrantVectorstore:
    """Instantiate a QdrantVectorstore based on environment configuration."""
    api_key = os.getenv("QDRANT_API_KEY")
    location = os.getenv("QDRANT_LOCATION")
    url = os.getenv("QDRANT_URL")
    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")
    https_flag = _bool_from_env(os.getenv("QDRANT_HTTPS"))

    kwargs: dict[str, object] = {}
    if https_flag is not None:
        kwargs["https"] = https_flag

    if location:
        return QdrantVectorstore(
            api_key=api_key,
            location=location,
            **kwargs,
        )

    if url:
        parsed = urlparse(url)
        host = parsed.hostname or host
        # Determine port from URL scheme if not explicitly provided
        if not port:
            if parsed.port:
                port = str(parsed.port)
            elif parsed.scheme == "https":
                port = "443"
            else:
                port = "80"
        if https_flag is None and parsed.scheme == "https":
            kwargs["https"] = True

    # Fallback to defaults if host/port missing
    host = host or "localhost"
    port = int(port) if port else 6333

    return QdrantVectorstore(
        host=host,
        port=port,
        api_key=api_key,
        **kwargs,
    )
