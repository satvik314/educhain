"""Tests for the dependency-free text splitter and in-memory vector store."""

import pytest

from educhain.utils.text_splitter import split_text
from educhain.utils.vectorstore import InMemoryVectorStore


def test_split_empty_returns_empty():
    assert split_text("") == []


def test_short_text_single_chunk():
    assert split_text("hello", chunk_size=100) == ["hello"]


def test_chunks_respect_size_with_overlap():
    text = ("Sentence number one. " * 60).strip()
    chunks = split_text(text, chunk_size=200, chunk_overlap=40)
    assert len(chunks) > 1
    assert all(len(c) <= 240 for c in chunks)  # size + overlap headroom


def test_overlap_is_clamped_below_size():
    # Overlap >= size is clamped (not an error); splitting still succeeds.
    text = "word " * 200
    chunks = split_text(text, chunk_size=50, chunk_overlap=100)
    assert len(chunks) > 1


def test_non_positive_chunk_size_raises():
    with pytest.raises(ValueError):
        split_text("abc", chunk_size=0)


def test_paragraph_boundaries_preferred():
    text = "First paragraph here.\n\nSecond paragraph here."
    chunks = split_text(text, chunk_size=30, chunk_overlap=5)
    assert any("First paragraph" in c for c in chunks)


def _toy_embed(texts):
    # 3-dim toy embedding by keyword counts.
    keys = ("python", "java", "rust")
    return [[float(t.lower().count(k)) for k in keys] for t in texts]


def test_vector_store_retrieves_relevant_chunk():
    store = InMemoryVectorStore.from_texts(
        ["python is great", "java runs everywhere", "rust is fast"], _toy_embed
    )
    assert len(store) == 3
    top = store.similarity_search("i love python python", k=1)
    assert top == ["python is great"]


def test_vector_store_with_scores_sorted_desc():
    store = InMemoryVectorStore.from_texts(
        ["python python", "java", "python java"], _toy_embed
    )
    results = store.similarity_search_with_score("python", k=3)
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)


def test_empty_store_returns_empty():
    store = InMemoryVectorStore(_toy_embed)
    assert store.similarity_search("anything") == []
