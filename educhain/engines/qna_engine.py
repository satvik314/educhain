"""
QnAEngine - question generation for Educhain.

Rewritten for Educhain 1.0 on top of the OpenAI SDK (via
:class:`~educhain.core.client.LLMClient`). No LangChain. Every feature from the
previous version is preserved; the public method names are cleaner, and the old
names remain available as thin deprecated aliases.
"""

from __future__ import annotations

import base64
import concurrent.futures
import csv
import io
import json
import random
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Type, Union

from pydantic import BaseModel, ValidationError

from educhain.core.client import LLMClient
from educhain.core.config import LLMConfig
from educhain.models.qna_models import (
    MCQList,
    ShortAnswerQuestionList,
    TrueFalseQuestionList,
    FillInBlankQuestionList,
    MCQListMath,
    Option,
    SolvedDoubt,
    VisualMCQList,
    BulkMCQ,
    BulkMCQList,
    BulkShortAnswerQuestion,
    BulkShortAnswerQuestionList,
    BulkTrueFalseQuestion,
    BulkTrueFalseQuestionList,
    BulkFillInBlankQuestion,
    BulkFillInBlankQuestionList,
)
from educhain.utils import prompts
from educhain.utils.loaders import PdfFileLoader, UrlLoader, YouTubeLoader

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]
OutputFormatType = Literal["pdf", "csv"]
SourceType = Literal["text", "pdf", "url"]

_QUESTION_MODELS: Dict[str, Type[BaseModel]] = {
    "Multiple Choice": MCQList,
    "Short Answer": ShortAnswerQuestionList,
    "True/False": TrueFalseQuestionList,
    "Fill in the Blank": FillInBlankQuestionList,
}

_BULK_MODELS: Dict[str, Tuple[Type[BaseModel], Type[BaseModel]]] = {
    "Multiple Choice": (BulkMCQ, BulkMCQList),
    "Short Answer": (BulkShortAnswerQuestion, BulkShortAnswerQuestionList),
    "True/False": (BulkTrueFalseQuestion, BulkTrueFalseQuestionList),
    "Fill in the Blank": (BulkFillInBlankQuestion, BulkFillInBlankQuestionList),
}


def _deprecated(old: str, new: str) -> None:
    warnings.warn(
        f"{old}() is deprecated and will be removed in a future release; "
        f"use {new}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class QnAEngine:
    """Generate questions of many kinds from topics, documents, media and images."""

    def __init__(self, config: Optional[LLMConfig] = None, client: Optional[LLMClient] = None):
        self.client = client or LLMClient(config)
        self.pdf_loader = PdfFileLoader()
        self.url_loader = UrlLoader()
        self.youtube_loader = YouTubeLoader()

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _model_for(question_type: str, response_model: Optional[Type[Any]]) -> Type[BaseModel]:
        if response_model is not None:
            return response_model
        if question_type not in _QUESTION_MODELS:
            raise ValueError(
                f"Unsupported question_type '{question_type}'. "
                f"Choose one of: {', '.join(_QUESTION_MODELS)}."
            )
        return _QUESTION_MODELS[question_type]

    def _save(self, data: Any, output_format: Optional[OutputFormatType]):
        if not output_format:
            return data
        from educhain.utils.output_formatter import OutputFormatter

        formatter = OutputFormatter()
        if output_format == "pdf":
            output_file = formatter.to_pdf(data)
        elif output_format == "csv":
            output_file = formatter.to_csv(data)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        return data, output_file

    def _load_source(self, source: str, source_type: str) -> str:
        if source_type == "text":
            return source
        if source_type == "pdf":
            return self.pdf_loader.load_data(source)
        if source_type == "url":
            return self.url_loader.load_data(source)
        raise ValueError("source_type must be one of: 'text', 'pdf', 'url'.")

    # ------------------------------------------------------------------ #
    # Core generation
    # ------------------------------------------------------------------ #
    def generate(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **context: Any,
    ) -> Any:
        """Generate ``num`` questions about ``topic``.

        ``**context`` (e.g. ``subtopic=...``, ``learning_objective=...``,
        ``difficulty_level=...``) is woven into the prompt.
        """
        model = self._model_for(question_type, response_model)
        prompt = prompts.question_prompt(
            topic=topic,
            num=num,
            question_type=question_type,
            custom_template=prompt_template,
            custom_instructions=custom_instructions,
            **context,
        )
        result = self.client.generate(model, prompt, system=prompts.QUESTION_SYSTEM_PROMPT)
        return self._save(result, output_format)

    def generate_from_source(
        self,
        source: str,
        source_type: SourceType,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **context: Any,
    ) -> Any:
        """Generate questions from text, a PDF path, or a URL."""
        content = self._load_source(source, source_type)
        return self.generate(
            topic=content,
            num=num,
            question_type=question_type,
            prompt_template=prompt_template,
            custom_instructions=custom_instructions,
            response_model=response_model,
            output_format=output_format,
            **context,
        )

    def generate_from_text(self, text: str, num: int = 1, **kwargs) -> Any:
        return self.generate_from_source(text, "text", num=num, **kwargs)

    def generate_from_pdf(self, path: str, num: int = 1, **kwargs) -> Any:
        return self.generate_from_source(path, "pdf", num=num, **kwargs)

    def generate_from_url(self, url: str, num: int = 1, **kwargs) -> Any:
        return self.generate_from_source(url, "url", num=num, **kwargs)

    def generate_from_youtube(
        self,
        url: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        target_language: str = "en",
        preserve_original_language: bool = False,
        **context: Any,
    ) -> Any:
        """Generate questions from a YouTube video's transcript."""
        transcript, detected = self.youtube_loader.load_data(url, target_language)
        if not transcript:
            raise ValueError("No transcript content retrieved from the video.")

        note = f"\nThis content is from a YouTube video. Content language: {detected}."
        if detected != target_language and not preserve_original_language:
            note += f" Generate the questions in {target_language}."
        custom_instructions = (note + "\n" + custom_instructions) if custom_instructions else note

        return self.generate_from_source(
            source=transcript,
            source_type="text",
            num=num,
            question_type=question_type,
            prompt_template=prompt_template,
            custom_instructions=custom_instructions,
            response_model=response_model,
            output_format=output_format,
            **context,
        )

    # ------------------------------------------------------------------ #
    # Visual (chart-based) questions
    # ------------------------------------------------------------------ #
    def generate_visual(
        self,
        topic: str,
        num: int = 1,
        custom_instructions: Optional[str] = None,
        render: bool = True,
        **context: Any,
    ) -> Optional[VisualMCQList]:
        """Generate questions that require reading a chart or table."""
        prompt = prompts.visual_prompt(topic, num, custom_instructions)
        result = self.client.generate(VisualMCQList, prompt, system=prompts.VISUAL_SYSTEM_PROMPT)
        if render and result and result.questions:
            from educhain.utils.visualize import display_visual_question

            for q in result.questions:
                if q.graph_instruction:
                    display_visual_question(q, q.graph_instruction.model_dump())
        return result

    # ------------------------------------------------------------------ #
    # Math MCQs (with verified numerical answers)
    # ------------------------------------------------------------------ #
    def generate_math(
        self,
        topic: str,
        num: int = 1,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> Any:
        """Generate computation-based MCQs, recomputing each numerical answer."""
        model = response_model or MCQListMath
        prompt = prompts.math_prompt(topic, num, custom_instructions)
        result = self.client.generate(model, prompt, system=prompts.MATH_SYSTEM_PROMPT)

        for question in getattr(result, "questions", []):
            if getattr(question, "requires_math", False):
                self._verify_math_question(question)
        return result

    def _verify_math_question(self, question) -> None:
        try:
            answer = self.client.complete(
                "Solve this problem step by step, then give ONLY the final "
                f"numerical answer after 'Final Answer:'.\n\n{question.question}",
                system="You are a careful mathematician.",
                temperature=0,
            )
            value = self._extract_number(answer)
            formatted = f"{value:.2f}"
            question.explanation = (question.explanation or "") + f"\n\nVerified answer: {formatted}"
            options = [Option(text=formatted, correct="true")]
            for factor in (0.9, 1.1, 1.2):
                options.append(Option(text=f"{value * factor:.2f}", correct="false"))
            random.shuffle(options)
            question.options = options
        except Exception as exc:  # noqa: BLE001
            question.explanation = (question.explanation or "") + f"\n\n(Could not verify: {exc})"

    @staticmethod
    def _extract_number(text: str) -> float:
        import re

        if "Final Answer:" in text:
            text = text.split("Final Answer:")[-1]
        elif "Answer:" in text:
            text = text.split("Answer:")[-1]
        matches = re.findall(r"-?\d+\.?\d*", text)
        if not matches:
            raise ValueError("No numerical answer found.")
        return float(matches[0])

    # ------------------------------------------------------------------ #
    # Image doubt solving (vision)
    # ------------------------------------------------------------------ #
    def solve_doubt(
        self,
        image_source: str,
        prompt: str = "Explain how to solve this problem",
        custom_instructions: Optional[str] = None,
        detail_level: Literal["low", "medium", "high"] = "medium",
        focus_areas: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> SolvedDoubt:
        """Analyse an image (e.g. a homework problem) and explain the solution."""
        if not image_source:
            raise ValueError("image_source (path, URL, or data URI) is required.")
        try:
            image_url = self._load_image(image_source)
            user_text = f"Analyze the image and {prompt}."
            if focus_areas:
                user_text += f" Focus on: {', '.join(focus_areas)}."
            user_text += f" Provide a {detail_level}-detail explanation, "
            user_text += "step-by-step solution, and any helpful notes."
            if custom_instructions:
                user_text += f"\n{custom_instructions}"

            message = self.client.image_message(
                user_text, image_url, detail="high" if detail_level == "high" else "auto"
            )
            return self.client.generate(
                SolvedDoubt,
                system=prompts.DOUBT_SYSTEM_PROMPT,
                messages=[message],
                **kwargs,
            )
        except Exception as exc:  # noqa: BLE001
            return SolvedDoubt(
                explanation=f"Error in solve_doubt: {type(exc).__name__}: {exc}",
                steps=[],
                additional_notes="An error occurred during processing.",
            )

    @staticmethod
    def _load_image(source: str) -> str:
        if source.startswith(("http://", "https://", "data:image")):
            return source
        try:
            from PIL import Image
        except ImportError:
            raise ImportError(
                "Pillow is required to load local images. "
                "Install with:  pip install educhain[visual]"
            )
        image = Image.open(source)
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

    # ------------------------------------------------------------------ #
    # Retrieval-augmented generation
    # ------------------------------------------------------------------ #
    def generate_with_rag(
        self,
        source: str,
        source_type: SourceType,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        response_model: Optional[Type[Any]] = None,
        learning_objective: Optional[str] = None,
        difficulty_level: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        output_format: Optional[OutputFormatType] = None,
        k: int = 4,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        retrieval_query: Optional[str] = None,
        **context: Any,
    ) -> Any:
        """Generate questions grounded in retrieved chunks of a document."""
        from educhain.utils.text_splitter import split_text
        from educhain.utils.vectorstore import InMemoryVectorStore

        content = self._load_source(source, source_type)
        chunks = split_text(content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if not chunks:
            raise ValueError("No content could be extracted from the source.")

        store = InMemoryVectorStore.from_texts(chunks, self.client.embed)
        query = retrieval_query or learning_objective or "key concepts and important facts"
        retrieved = store.similarity_search(query, k=k)
        retrieved_context = "\n\n".join(retrieved)

        model = self._model_for(question_type, response_model)
        prompt = prompts.rag_prompt(
            num=num,
            question_type=question_type,
            context=retrieved_context,
            learning_objective=learning_objective,
            difficulty_level=difficulty_level,
            custom_instructions=custom_instructions,
        )
        result = self.client.generate(model, prompt, system=prompts.QUESTION_SYSTEM_PROMPT)
        return self._save(result, output_format)

    # ------------------------------------------------------------------ #
    # Misc
    # ------------------------------------------------------------------ #
    def generate_similar_options(self, question: str, correct_answer: str, num_options: int = 3) -> List[str]:
        """Generate plausible distractor options for a known correct answer."""
        text = self.client.complete(
            f"Generate {num_options} incorrect but plausible options similar to the "
            f"correct answer '{correct_answer}' for the question '{question}'. "
            "Return only the options, separated by semicolons, with no extra symbols.",
        )
        return [opt.strip() for opt in text.split(";") if opt.strip()]

    # ================================================================== #
    # Bulk generation
    # ================================================================== #
    def generate_bulk(
        self,
        topics_file: Union[str, Path],
        total_questions: Optional[int] = None,
        questions_per_objective: Optional[int] = None,
        max_workers: Optional[int] = None,
        output_format: Optional[str] = None,
        prompt_template: Optional[str] = None,
        question_type: QuestionType = "Multiple Choice",
        question_model: Optional[Type[BaseModel]] = None,
        question_list_model: Optional[Type[BaseModel]] = None,
        min_questions_per_batch: int = 3,
        max_retries: int = 3,
        save_csv: bool = True,
        **kwargs: Any,
    ) -> Tuple[BaseModel, Optional[str], int, int]:
        """Generate many questions from a JSON topic structure, in parallel.

        The JSON file must contain a list of topics, each with ``subtopics``,
        each with ``learning_objectives`` (strings, or ``{"objective",
        "num_questions"}`` objects).

        Returns ``(question_list_model(questions=...), output_file,
        total_generated, failed_objectives)``.
        """
        if question_model is None or question_list_model is None:
            default_model, default_list = _BULK_MODELS.get(
                question_type, (BulkMCQ, BulkMCQList)
            )
            question_model = question_model or default_model
            question_list_model = question_list_model or default_list

        path = Path(topics_file)
        if not path.exists():
            raise ValueError("topics_file must be a path to a JSON file.")
        with open(path) as f:
            topics_data = json.load(f)

        combinations = self._process_topics_data(topics_data)
        if not combinations:
            raise ValueError("No (topic, subtopic, objective) combinations found.")

        distribution = self._distribute_questions(
            combinations, total_questions, questions_per_objective, min_questions_per_batch
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"questions_{timestamp}.csv" if save_csv else None
        if csv_file:
            self._init_csv(csv_file, question_model)

        all_questions: List[BaseModel] = []
        failed = 0
        seen: set = set()

        def worker(combo):
            key = self._combo_key(combo)
            target = distribution[key]
            return combo, self._generate_for_objective(
                combo, target, prompt_template, question_model,
                question_list_model, question_type, max_retries, **kwargs
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(worker, combo) for combo in combinations]
            for future in concurrent.futures.as_completed(futures):
                try:
                    combo, questions = future.result()
                except Exception as exc:  # noqa: BLE001
                    print(f"Error generating for an objective: {exc}")
                    failed += 1
                    continue
                fresh = self._dedupe(questions, seen)
                if not fresh:
                    failed += 1
                if fresh and csv_file:
                    self._append_csv(fresh, csv_file, question_model)
                all_questions.extend(fresh)

        output_file: Optional[str] = csv_file
        if output_format == "json":
            output_file = f"questions_{timestamp}.json"
            with open(output_file, "w") as f:
                json.dump([q.model_dump() for q in all_questions], f, indent=2)

        print(
            f"\n--- Bulk generation summary ---\n"
            f"Objectives: {len(combinations)} | Generated: {len(all_questions)} | "
            f"Failed objectives: {failed}"
        )
        return question_list_model(questions=all_questions), output_file, len(all_questions), failed

    # --- bulk helpers --------------------------------------------------- #
    @staticmethod
    def _combo_key(combo: Dict[str, Any]) -> str:
        return f"{combo['topic']}:{combo['subtopic']}:{combo['learning_objective']}"

    @staticmethod
    def _process_topics_data(topics_data) -> List[Dict[str, Any]]:
        combinations = []
        for topic in topics_data:
            for subtopic in topic.get("subtopics", []):
                for objective in subtopic.get("learning_objectives", []):
                    if isinstance(objective, dict) and "objective" in objective:
                        combinations.append({
                            "topic": topic["topic"],
                            "subtopic": subtopic["name"],
                            "learning_objective": objective["objective"],
                            "num_questions": objective.get("num_questions"),
                        })
                    else:
                        combinations.append({
                            "topic": topic["topic"],
                            "subtopic": subtopic["name"],
                            "learning_objective": objective,
                            "num_questions": None,
                        })
        return combinations

    def _distribute_questions(
        self, combinations, total_questions, questions_per_objective, min_per_batch
    ) -> Dict[str, int]:
        distribution: Dict[str, int] = {}
        if questions_per_objective is not None:
            for combo in combinations:
                distribution[self._combo_key(combo)] = questions_per_objective
            return distribution

        if any(c["num_questions"] for c in combinations):
            for combo in combinations:
                distribution[self._combo_key(combo)] = combo["num_questions"] or min_per_batch
            return distribution

        n = len(combinations)
        if total_questions is None:
            total_questions = n * min_per_batch
        base = max(min_per_batch, total_questions // n)
        remainder = total_questions % n
        for i, combo in enumerate(combinations):
            distribution[self._combo_key(combo)] = base + (1 if i < remainder else 0)
        return distribution

    def _generate_for_objective(
        self, combo, target, prompt_template, question_model,
        question_list_model, question_type, max_retries, **kwargs
    ) -> List[BaseModel]:
        collected: List[BaseModel] = []
        attempts = 0
        while len(collected) < target and attempts < max_retries:
            attempts += 1
            try:
                batch = self.generate(
                    topic=combo["topic"],
                    num=target - len(collected),
                    question_type=question_type,
                    prompt_template=prompt_template,
                    response_model=question_list_model,
                    subtopic=combo["subtopic"],
                    learning_objective=combo["learning_objective"],
                    **kwargs,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"  batch error ({self._combo_key(combo)}): {exc}")
                continue
            for q in getattr(batch, "questions", []):
                data = q.model_dump() if hasattr(q, "model_dump") else q
                if "metadata" in getattr(question_model, "model_fields", {}):
                    data.setdefault("metadata", {})
                    data["metadata"].update({
                        "topic": combo["topic"],
                        "subtopic": combo["subtopic"],
                        "learning_objective": combo["learning_objective"],
                    })
                validated = self._validate(data, question_model)
                if validated is not None:
                    collected.append(validated)
                if len(collected) >= target:
                    break
        return collected[:target]

    @staticmethod
    def _validate(data: dict, model: Type[BaseModel]) -> Optional[BaseModel]:
        try:
            return model(**data)
        except (ValidationError, TypeError):
            return None

    @staticmethod
    def _dedupe(questions: List[BaseModel], seen: set) -> List[BaseModel]:
        fresh = []
        for q in questions:
            text = getattr(q, "question", None)
            key = (text or "").strip()
            if key and key in seen:
                continue
            if key:
                seen.add(key)
            fresh.append(q)
        return fresh

    @staticmethod
    def _init_csv(csv_file: str, model: Type[BaseModel]) -> None:
        fields = list(model.model_fields.keys())
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()

    @staticmethod
    def _append_csv(questions: List[BaseModel], csv_file: str, model: Type[BaseModel]) -> None:
        fields = list(model.model_fields.keys())
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            for q in questions:
                data = q.model_dump() if hasattr(q, "model_dump") else dict(q)
                row = {}
                for field in fields:
                    value = data.get(field)
                    if isinstance(value, (dict, list)):
                        row[field] = json.dumps(value)
                    else:
                        row[field] = value
                writer.writerow(row)

    # ================================================================== #
    # Deprecated aliases (pre-1.0 API)
    # ================================================================== #
    def generate_questions(self, *args, **kwargs):
        _deprecated("generate_questions", "generate")
        return self.generate(*args, **kwargs)

    def generate_questions_from_data(self, source, source_type, num, *args, **kwargs):
        _deprecated("generate_questions_from_data", "generate_from_source")
        return self.generate_from_source(source, source_type, num, *args, **kwargs)

    def generate_questions_from_youtube(self, *args, **kwargs):
        _deprecated("generate_questions_from_youtube", "generate_from_youtube")
        return self.generate_from_youtube(*args, **kwargs)

    def generate_visual_questions(self, topic, num=1, custom_instructions=None, **kwargs):
        _deprecated("generate_visual_questions", "generate_visual")
        return self.generate_visual(topic, num, custom_instructions=custom_instructions)

    def generate_mcq_math(self, topic, num=1, *args, **kwargs):
        _deprecated("generate_mcq_math", "generate_math")
        kwargs.pop("question_type", None)
        kwargs.pop("prompt_template", None)
        return self.generate_math(topic, num, **kwargs)

    def generate_questions_with_rag(self, *args, **kwargs):
        _deprecated("generate_questions_with_rag", "generate_with_rag")
        return self.generate_with_rag(*args, **kwargs)

    def bulk_generate_questions(self, topic, *args, **kwargs):
        _deprecated("bulk_generate_questions", "generate_bulk")
        return self.generate_bulk(topic, *args, **kwargs)


__all__ = ["QnAEngine", "QuestionType", "OutputFormatType"]
