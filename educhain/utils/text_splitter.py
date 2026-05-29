"""
A small, dependency-free text splitter.

Replaces ``langchain_text_splitters.RecursiveCharacterTextSplitter`` for the
chunking Educhain needs (RAG ingestion). It splits on a descending list of
separators so chunks fall on natural boundaries (paragraphs, then lines, then
sentences, then words) while respecting a target size and overlap.
"""

from __future__ import annotations

from typing import List, Sequence

_DEFAULT_SEPARATORS: Sequence[str] = ["\n\n", "\n", ". ", " ", ""]


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Sequence[str] = _DEFAULT_SEPARATORS,
) -> List[str]:
    """Split ``text`` into overlapping chunks of roughly ``chunk_size`` chars.

    ``chunk_overlap`` is clamped to be strictly smaller than ``chunk_size`` so
    that callers who shrink ``chunk_size`` don't have to remember to shrink the
    overlap too.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))

    splits = _split_recursive(text, chunk_size, list(separators))
    return _merge_splits(splits, chunk_size, chunk_overlap)


def _split_recursive(text: str, chunk_size: int, separators: List[str]) -> List[str]:
    """Break text into pieces no larger than chunk_size where possible."""
    if len(text) <= chunk_size:
        return [text]
    if not separators:
        # Hard split as a last resort.
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    sep = separators[0]
    rest = separators[1:]
    if sep == "":
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    pieces = text.split(sep)
    out: List[str] = []
    for piece in pieces:
        candidate = piece + sep
        if len(candidate) <= chunk_size:
            out.append(candidate)
        else:
            out.extend(_split_recursive(piece, chunk_size, rest))
    return [p for p in out if p]


def _merge_splits(splits: List[str], chunk_size: int, chunk_overlap: int) -> List[str]:
    """Greedily merge small splits into ~chunk_size chunks with overlap."""
    chunks: List[str] = []
    current = ""
    for split in splits:
        if not current:
            current = split
        elif len(current) + len(split) <= chunk_size:
            current += split
        else:
            chunks.append(current.strip())
            # Start the next chunk with a tail of the previous one (overlap).
            overlap = current[-chunk_overlap:] if chunk_overlap else ""
            current = overlap + split
    if current.strip():
        chunks.append(current.strip())
    return [c for c in chunks if c]


__all__ = ["split_text"]
