"""
A tiny in-memory vector store for retrieval-augmented generation.

Replaces the LangChain + Chroma stack used in the old QnA engine. For
Educhain's use case - embedding a single document and retrieving the most
relevant chunks for question generation - an in-process cosine-similarity
search over NumPy arrays is more than enough, and it removes the heavy
``chromadb`` dependency entirely.

The store is embedding-backend agnostic: it just needs a callable that turns a
list of strings into a list of vectors (``LLMClient.embed`` fits perfectly).
"""

from __future__ import annotations

from typing import Callable, List, Sequence, Tuple

EmbedFn = Callable[[Sequence[str]], List[List[float]]]


class InMemoryVectorStore:
    """Cosine-similarity nearest-neighbour search over embedded text chunks."""

    def __init__(self, embed_fn: EmbedFn, batch_size: int = 64):
        self._embed_fn = embed_fn
        self._batch_size = batch_size
        self._texts: List[str] = []
        self._matrix = None  # lazily-created numpy array of normalized vectors

    @classmethod
    def from_texts(cls, texts: Sequence[str], embed_fn: EmbedFn, **kwargs) -> "InMemoryVectorStore":
        store = cls(embed_fn, **kwargs)
        store.add_texts(texts)
        return store

    def add_texts(self, texts: Sequence[str]) -> None:
        texts = [t for t in texts if t and t.strip()]
        if not texts:
            return
        import numpy as np

        vectors: List[List[float]] = []
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i : i + self._batch_size]
            vectors.extend(self._embed_fn(batch))

        new = np.asarray(vectors, dtype="float32")
        new = _normalize(new, np)
        self._texts.extend(texts)
        self._matrix = new if self._matrix is None else np.vstack([self._matrix, new])

    def similarity_search(self, query: str, k: int = 4) -> List[str]:
        """Return the ``k`` chunks most similar to ``query``."""
        results = self.similarity_search_with_score(query, k)
        return [text for text, _ in results]

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        if self._matrix is None or not self._texts:
            return []
        import numpy as np

        q = np.asarray(self._embed_fn([query]), dtype="float32")
        q = _normalize(q, np)[0]
        scores = self._matrix @ q  # cosine similarity (vectors are normalized)
        k = min(k, len(self._texts))
        # argpartition for top-k, then sort those by score descending.
        top = np.argpartition(-scores, k - 1)[:k]
        top = top[np.argsort(-scores[top])]
        return [(self._texts[i], float(scores[i])) for i in top]

    def __len__(self) -> int:
        return len(self._texts)


def _normalize(matrix, np):
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


__all__ = ["InMemoryVectorStore"]
