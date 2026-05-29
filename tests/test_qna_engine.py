"""Tests for the QnAEngine."""

import json

import pytest

from educhain.models.qna_models import (
    MCQList,
    MultipleChoiceQuestion,
    MCQListMath,
    MCQMath,
    Option,
    SolvedDoubt,
)


def _mcq_list(*questions):
    return MCQList(
        questions=[
            MultipleChoiceQuestion(question=q, answer="a", options=["a", "b", "c", "d"])
            for q in questions
        ]
    )


def test_generate_returns_mcq_list(educhain, fake_openai):
    fake_openai.set_parsed(_mcq_list("What is 2+2?"))
    out = educhain.qna.generate("math", num=1)
    assert isinstance(out, MCQList)
    assert out.questions[0].question == "What is 2+2?"


def test_generate_from_text_delegates(educhain, fake_openai):
    fake_openai.set_parsed(_mcq_list("From text?"))
    out = educhain.qna.generate_from_text("Some source content", num=1)
    assert out.questions[0].question == "From text?"


def test_unsupported_question_type_raises(educhain):
    with pytest.raises(ValueError):
        educhain.qna.generate("x", question_type="Essay")  # type: ignore[arg-type]


def test_deprecated_generate_questions_warns(educhain, fake_openai):
    fake_openai.set_parsed(_mcq_list("q"))
    with pytest.warns(DeprecationWarning):
        educhain.qna.generate_questions("topic", num=1)


def test_generate_math_verifies_answers(educhain, fake_openai):
    math_list = MCQListMath(
        questions=[
            MCQMath(
                question="2+2",
                requires_math=True,
                options=[Option(text="3", correct="false")],
                explanation="",
            )
        ]
    )
    fake_openai.set_parsed(math_list)
    fake_openai.set_content("Step 1: add. Final Answer: 4")
    out = educhain.qna.generate_math("addition", num=1)
    q = out.questions[0]
    # The correct option should now be the verified value 4.00.
    correct = [o.text for o in q.options if o.correct == "true"]
    assert correct == ["4.00"]
    assert len(q.options) == 4


def test_solve_doubt_error_path_returns_model(educhain, fake_openai):
    # No PIL / unreachable path -> returns a SolvedDoubt describing the error.
    fake_openai.fail_parse(Exception("vision error"))
    result = educhain.qna.solve_doubt("https://example.com/image.png")
    assert isinstance(result, SolvedDoubt)
    assert "Error" in result.explanation or result.steps == []


def test_generate_similar_options(educhain, fake_openai):
    fake_openai.set_content("Paris; Berlin; Madrid")
    opts = educhain.qna.generate_similar_options("Capital of France?", "London", 3)
    assert opts == ["Paris", "Berlin", "Madrid"]


def test_generate_bulk(tmp_path, educhain, fake_openai):
    topics = [
        {
            "topic": "Math",
            "subtopics": [
                {"name": "Algebra", "learning_objectives": ["Solve equations"]},
            ],
        }
    ]
    topics_file = tmp_path / "topics.json"
    topics_file.write_text(json.dumps(topics))

    # Each batch returns 2 BulkMCQ-compatible MCQs.
    from educhain.models.qna_models import BulkMCQ, BulkMCQList

    bulk = BulkMCQList(
        questions=[
            BulkMCQ(
                question=f"Q{i}",
                options=[Option(text="a", correct="true")],
                explanation="e",
                difficulty="easy",
            )
            for i in range(2)
        ]
    )
    fake_openai.set_parsed(bulk)

    result, output_file, total, failed = educhain.qna.generate_bulk(
        topics_file,
        questions_per_objective=2,
        max_workers=1,
        save_csv=False,
    )
    assert total == 2
    assert failed == 0
    assert len(result.questions) == 2
