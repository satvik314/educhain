"""Tests for the ContentEngine."""

import pytest

from educhain.engines.content_engine import _PEDAGOGY_CONFIGS
from educhain.models.content_models import (
    FlashcardSet,
    Flashcard,
    LessonPlan,
)
from educhain.models.pedagogy_models import BloomsTaxonomyContent


def test_flashcards(educhain, fake_openai):
    fs = FlashcardSet(
        title="Cells",
        flashcards=[Flashcard(front="What is a cell?", back="Unit of life")],
    )
    fake_openai.set_parsed(fs)
    out = educhain.content.flashcards("Cells", num=1)
    assert out.title == "Cells"
    assert out.flashcards[0].front == "What is a cell?"


def test_lesson_plan(educhain, fake_openai):
    lp = LessonPlan(
        title="Photosynthesis",
        subject="Biology",
        learning_objectives=["Understand it"],
        lesson_introduction="Intro",
        main_topics=[],
    )
    fake_openai.set_parsed(lp)
    out = educhain.content.lesson_plan("Photosynthesis", grade_level="High School")
    assert out.title == "Photosynthesis"


def test_list_pedagogies_has_eight():
    peds = _PEDAGOGY_CONFIGS
    assert len(peds) == 8
    assert "blooms_taxonomy" in peds


def test_all_pedagogy_templates_format_cleanly():
    # A KeyError here means a template references an undefined variable.
    for cfg in _PEDAGOGY_CONFIGS.values():
        cfg["template"].format(topic="Fractions", **cfg["defaults"])


def test_pedagogy_generates(educhain, fake_openai):
    content = BloomsTaxonomyContent(topic="Fractions")
    fake_openai.set_parsed(content)
    out = educhain.content.pedagogy("Fractions", "blooms_taxonomy")
    assert out.topic == "Fractions"


def test_unknown_pedagogy_raises(educhain):
    with pytest.raises(ValueError):
        educhain.content.pedagogy("X", "not_a_pedagogy")


def test_list_pedagogies_method(educhain):
    info = educhain.content.list_pedagogies()
    assert set(info) == set(_PEDAGOGY_CONFIGS)
    assert "description" in info["gamification"]


def test_deprecated_aliases_warn(educhain, fake_openai):
    fake_openai.set_parsed(
        FlashcardSet(title="t", flashcards=[Flashcard(front="f", back="b")])
    )
    with pytest.warns(DeprecationWarning):
        educhain.content.generate_flashcards("t", num=1)
