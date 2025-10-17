"""
Utility per interrogare la documentazione ufficiale di Datapizza-AI
indicizzata in Qdrant.

Fornisce un'API asincrona che restituisce sia il testo combinato da usare
nei prompt RAG sia i metadati dei chunk per il debug dell'interfaccia.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from datapizza.embedders.openai.openai import OpenAIEmbedder
from datapizza.vectorstores.qdrant import QdrantVectorstore
from datapizza.type import Chunk

from qdrant_config import build_qdrant_vectorstore

# Configurazione tramite variabili d'ambiente (con default sensati)
OFFICIAL_DOCS_COLLECTION = os.getenv("OFFICIAL_DOCS_COLLECTION", "datapizza_official_docs")
OFFICIAL_DOCS_EMBED_MODEL = os.getenv("OFFICIAL_DOCS_EMBED_MODEL", "text-embedding-3-small")
OFFICIAL_DOCS_MAX_SECTION_CHARS = int(os.getenv("OFFICIAL_DOCS_MAX_SECTION_CHARS", "1200"))


@dataclass
class DocsResult:
    """Risultato formalizzato della ricerca documentazione."""

    combined_text: str
    chunk_previews: List[Dict[str, Any]]


_embedder: OpenAIEmbedder | None = None
_vectorstore: QdrantVectorstore | None = None


def _get_embedder() -> OpenAIEmbedder:
    """Restituisce (con caching) l'embedder OpenAI usato per le query."""
    global _embedder

    if _embedder is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY non configurata: impossibile interrogare la documentazione ufficiale."
            )

        _embedder = OpenAIEmbedder(
            api_key=api_key,
            model_name=OFFICIAL_DOCS_EMBED_MODEL,
        )

    return _embedder


def _get_vectorstore() -> QdrantVectorstore:
    """Restituisce (con caching) il vector store Qdrant configurato via qdrant_config."""
    global _vectorstore

    if _vectorstore is None:
        _vectorstore = build_qdrant_vectorstore()

    return _vectorstore


def _build_combined_context(chunks: List[Chunk]) -> Tuple[str, List[Dict[str, Any]]]:
    """Costruisce il testo da usare nei prompt e i preview per il debug."""
    if not chunks:
        return "", []

    section_lines: List[str] = []
    previews: List[Dict[str, Any]] = []

    section_lines.append("=== DOCUMENTAZIONE UFFICIALE ===\n")

    for idx, chunk in enumerate(chunks, start=1):
        metadata = getattr(chunk, "metadata", {}) or {}
        text = getattr(chunk, "text", "") or ""
        score = getattr(chunk, "score", None)

        file_path = metadata.get("file_path") or metadata.get("source") or "documentazione"
        filename = metadata.get("filename") or metadata.get("title") or file_path

        cleaned_text = text.strip()
        if len(cleaned_text) > OFFICIAL_DOCS_MAX_SECTION_CHARS:
            cleaned_text = cleaned_text[:OFFICIAL_DOCS_MAX_SECTION_CHARS] + "…"

        section_lines.append(f"[DOC #{idx}] {filename}")
        section_lines.append(f"Sorgente: {file_path}")
        section_lines.append(cleaned_text)
        section_lines.append("")  # Riga vuota di separazione

        previews.append(
            {
                "id": getattr(chunk, "id", None),
                "score": score,
                "metadata": metadata,
                "text": text,
            }
        )

    combined_text = "\n".join(section_lines).strip()
    return combined_text, previews


def _query_official_docs_sync(query: str, max_results: int = 5) -> DocsResult:
    """Esegue la ricerca sui documenti ufficiali (versione sincrona)."""
    embedder = _get_embedder()
    vectorstore = _get_vectorstore()

    query_vector = embedder.embed(query)

    chunks: List[Chunk] = vectorstore.search(
        collection_name=OFFICIAL_DOCS_COLLECTION,
        query_vector=query_vector,
        k=max_results,
    )

    combined_text, previews = _build_combined_context(chunks)
    return DocsResult(combined_text=combined_text, chunk_previews=previews)


async def query_official_docs(query: str, max_results: int = 5) -> DocsResult:
    """
    Interroga la documentazione ufficiale in maniera asincrona.

    Restituisce un DocsResult con:
    - combined_text: porzioni di documentazione pronte per essere inserite nel prompt
    - chunk_previews: lista di dizionari con metadati e testi grezzi per il debug
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        _query_official_docs_sync,
        query,
        max_results,
    )
