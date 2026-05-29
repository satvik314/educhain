"""Tests for the Pydantic content/question models."""

from educhain.models.qna_models import (
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    MCQList,
)
from educhain.models.content_models import FlashcardSet, Flashcard, PodcastScript, PodcastSegment


def test_mcq_show_runs(capsys):
    q = MultipleChoiceQuestion(
        question="Capital of France?",
        answer="Paris",
        options=["Paris", "London", "Rome", "Berlin"],
        explanation="It is Paris.",
    )
    q.show()
    out = capsys.readouterr().out
    assert "Paris" in out and "Capital of France?" in out


def test_true_false_answer_is_bool():
    q = TrueFalseQuestion(question="The sky is blue.", answer=True)
    assert q.answer is True


def test_mcq_list_show(capsys):
    ql = MCQList(
        questions=[
            MultipleChoiceQuestion(question="q1", answer="a", options=["a", "b"]),
        ]
    )
    ql.show()
    assert "q1" in capsys.readouterr().out


def test_flashcard_set_show_no_crash(capsys):
    # Regression: FlashcardSet.show() used to reference non-existent fields.
    fs = FlashcardSet(
        title="Set",
        flashcards=[Flashcard(front="f", back="b", explanation="e")],
    )
    fs.show()
    assert "Set" in capsys.readouterr().out


def test_podcast_full_script():
    script = PodcastScript(
        title="T",
        topic="Topic",
        introduction="Hello",
        segments=[PodcastSegment(title="S1", content="Body")],
        conclusion="Bye",
    )
    full = script.get_full_script()
    assert "Hello" in full and "Body" in full and "Bye" in full
