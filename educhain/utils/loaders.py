"""
Data loaders for turning external sources into plain text.

All third-party imports are performed lazily so that the base Educhain install
stays light: a user who only generates questions from text never needs
``pypdf``, ``beautifulsoup4`` or ``youtube-transcript-api`` installed.
"""

from __future__ import annotations

import re
from typing import Tuple


def _missing(package: str, extra: str) -> ImportError:
    return ImportError(
        f"'{package}' is required for this loader. "
        f"Install it with:  pip install educhain[{extra}]"
    )


def clean_text(text: str) -> str:
    """Collapse whitespace and trim."""
    return re.sub(r"\s+", " ", text or "").strip()


class PdfFileLoader:
    """Extract text from a local PDF file or file-like object."""

    def load_data(self, file_path) -> str:
        try:
            from pypdf import PdfReader
        except ImportError:
            try:
                from PyPDF2 import PdfReader  # type: ignore
            except ImportError:
                raise _missing("pypdf", "pdf")
        reader = PdfReader(file_path)
        parts = [clean_text(page.extract_text() or "") for page in reader.pages]
        return " ".join(p for p in parts if p)


class UrlLoader:
    """Fetch a URL and extract its visible text."""

    def load_data(self, url: str) -> str:
        try:
            import requests
        except ImportError:
            raise _missing("requests", "web")
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise _missing("beautifulsoup4", "web")
        response = requests.get(url, timeout=30, headers={"User-Agent": "Educhain/1.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return clean_text(soup.get_text())


class YouTubeLoader:
    """Fetch a transcript for a YouTube video."""

    _VIDEO_ID = re.compile(
        r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/"
        r"(?:watch\?v=|embed\/|v\/|shorts\/|live\/|feature=player_embedded&v=|e\/)?"
        r"([A-Za-z0-9_-]{11})"
    )

    def extract_video_id(self, url: str) -> str:
        match = self._VIDEO_ID.search(url or "")
        if not match:
            raise ValueError(f"Could not extract a YouTube video ID from: {url}")
        return match.group(1)

    def load_data(self, url: str, target_language: str = "en") -> Tuple[str, str]:
        """Return ``(transcript_text, detected_language)``."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            from youtube_transcript_api.formatters import TextFormatter
        except ImportError:
            raise _missing("youtube-transcript-api", "youtube")

        video_id = self.extract_video_id(url)
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        available = [t.language_code for t in transcript_list]
        if not available:
            raise ValueError("No transcripts available for this video.")

        formatter = TextFormatter()
        try:
            transcript = transcript_list.find_transcript([target_language])
            return formatter.format_transcript(transcript.fetch()), target_language
        except Exception:
            transcript = transcript_list.find_transcript(available)
            original = transcript.language_code
            if transcript.is_translatable and target_language != original:
                translated = transcript.translate(target_language)
                return formatter.format_transcript(translated.fetch()), target_language
            return formatter.format_transcript(transcript.fetch()), original


__all__ = ["PdfFileLoader", "UrlLoader", "YouTubeLoader", "clean_text"]
