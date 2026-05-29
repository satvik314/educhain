"""
ContentEngine - rich educational content for Educhain.

Rewritten for Educhain 1.0 on top of the OpenAI SDK (no LangChain). Generates
lesson plans, study guides, career connections, flashcards, pedagogy-driven
content (8 approaches), and podcasts (script + audio). Old method names remain
as deprecated aliases.
"""

from __future__ import annotations

import warnings
from datetime import datetime
from typing import Any, Dict, Optional, Type

from educhain.core.client import LLMClient
from educhain.core.config import LLMConfig
from educhain.models.content_models import (
    StudyGuide,
    CareerConnections,
    LessonPlan,
    FlashcardSet,
    PodcastScript,
    PodcastContent,
)
from educhain.models.pedagogy_models import (
    BloomsTaxonomyContent,
    SocraticQuestioningContent,
    ProjectBasedLearningContent,
    FlippedClassroomContent,
    InquiryBasedLearningContent,
    ConstructivistContent,
    GamificationContent,
    PeerLearningContent,
)

CONTENT_SYSTEM_PROMPT = (
    "You are an expert instructional designer. You create well-structured, "
    "accurate, engaging educational content grounded in sound pedagogy."
)


def _deprecated(old: str, new: str) -> None:
    warnings.warn(
        f"{old}() is deprecated and will be removed in a future release; "
        f"use {new}() instead.",
        DeprecationWarning,
        stacklevel=3,
    )


# --------------------------------------------------------------------------- #
# Pedagogy configuration: model + prompt + default parameters.
# --------------------------------------------------------------------------- #
_PEDAGOGY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "blooms_taxonomy": {
        "model": BloomsTaxonomyContent,
        "description": "Six cognitive levels: Remember, Understand, Apply, Analyze, Evaluate, Create.",
        "defaults": {"target_level": "All levels", "grade_level": "General"},
        "template": (
            "Create comprehensive, study-ready content for the topic '{topic}' "
            "using Bloom's Taxonomy (target level: {target_level}, grade level: "
            "{grade_level}). For each of the six cognitive levels - Remember, "
            "Understand, Apply, Analyze, Evaluate, Create - provide detailed "
            "content students can learn from, key concepts, learning objectives, "
            "activities, assessment questions, and real-world examples. Also "
            "describe the learning progression and an overall assessment strategy."
        ),
    },
    "socratic_questioning": {
        "model": SocraticQuestioningContent,
        "description": "Guided self-discovery through strategic questioning.",
        "defaults": {"depth_level": "Intermediate", "student_level": "High School"},
        "template": (
            "Create Socratic questioning content for '{topic}' (depth: "
            "{depth_level}, student level: {student_level}). Cover foundational, "
            "analytical, perspective, implication, and meta-cognitive questions. "
            "For each category give a content overview, thought-provoking "
            "questions, follow-up probes, example student responses, and "
            "facilitation notes."
        ),
    },
    "project_based_learning": {
        "model": ProjectBasedLearningContent,
        "description": "Complex, real-world projects that build deep, practical understanding.",
        "defaults": {"project_duration": "4-6 weeks", "team_size": "3-4 students", "industry_focus": "General"},
        "template": (
            "Design a project-based learning experience for '{topic}' "
            "(duration: {project_duration}, team size: {team_size}, industry "
            "focus: {industry_focus}). Include a driving question, project "
            "overview, learning objectives, detailed project phases (with "
            "materials, procedures, resources and assessment criteria), "
            "deliverables, and real-world connections."
        ),
    },
    "flipped_classroom": {
        "model": FlippedClassroomContent,
        "description": "Learn foundations at home; apply actively in class.",
        "defaults": {"class_duration": "50 minutes", "prep_time": "30-45 minutes", "technology_level": "Moderate"},
        "template": (
            "Design a flipped classroom experience for '{topic}' (class "
            "duration: {class_duration}, prep time: {prep_time}, technology "
            "level: {technology_level}). Provide complete pre-class content "
            "students can study independently, detailed in-class active-learning "
            "activities, and post-class reinforcement materials."
        ),
    },
    "inquiry_based_learning": {
        "model": InquiryBasedLearningContent,
        "description": "Understanding through questioning, investigation and discovery.",
        "defaults": {"inquiry_type": "Guided", "investigation_scope": "Moderate", "student_autonomy": "Balanced"},
        "template": (
            "Design an inquiry-based learning experience for '{topic}' (inquiry "
            "type: {inquiry_type}, scope: {investigation_scope}, autonomy: "
            "{student_autonomy}). Include essential questions, investigation "
            "phases, inquiry activities, research methods, scaffold supports, and "
            "presentation formats."
        ),
    },
    "constructivist": {
        "model": ConstructivistContent,
        "description": "Build understanding through experience, reflection and social interaction.",
        "defaults": {"prior_knowledge_level": "Mixed", "social_interaction_focus": "High", "reflection_emphasis": "Strong"},
        "template": (
            "Design a constructivist learning experience for '{topic}' (prior "
            "knowledge: {prior_knowledge_level}, social interaction: "
            "{social_interaction_focus}, reflection: {reflection_emphasis}). "
            "Include prior-knowledge activation, experiential learning, social "
            "construction activities, reflective practices, knowledge-building "
            "tools, and authentic assessment."
        ),
    },
    "gamification": {
        "model": GamificationContent,
        "description": "Game design elements to boost engagement and motivation.",
        "defaults": {"game_mechanics": "Points, badges, levels", "competition_level": "Moderate", "technology_platform": "Web-based"},
        "template": (
            "Design a gamified learning experience for '{topic}' (mechanics: "
            "{game_mechanics}, competition: {competition_level}, platform: "
            "{technology_platform}). Include game mechanics, game dynamics, "
            "learning integration, player-motivation strategies, progression "
            "design, and platform considerations."
        ),
    },
    "peer_learning": {
        "model": PeerLearningContent,
        "description": "Structured collaborative learning between students.",
        "defaults": {"group_size": "3-4 students", "collaboration_type": "Mixed", "skill_diversity": "Moderate"},
        "template": (
            "Design a peer learning experience for '{topic}' (group size: "
            "{group_size}, collaboration: {collaboration_type}, skill diversity: "
            "{skill_diversity}). Include peer learning structures, group "
            "formation strategies, collaboration activities, communication "
            "protocols, accountability measures, and instructor facilitation."
        ),
    },
}


class ContentEngine:
    """Generate lesson plans, study guides, flashcards, pedagogy content, podcasts."""

    def __init__(self, config: Optional[LLMConfig] = None, client: Optional[LLMClient] = None):
        self.client = client or LLMClient(config)

    # ------------------------------------------------------------------ #
    # Internal helper
    # ------------------------------------------------------------------ #
    def _generate(
        self,
        model: Type[Any],
        prompt: str,
        custom_instructions: Optional[str] = None,
        system: str = CONTENT_SYSTEM_PROMPT,
        **gen_kwargs: Any,
    ):
        if custom_instructions:
            prompt += f"\n\nAdditional instructions:\n{custom_instructions}"
        return self.client.generate(model, prompt, system=system, **gen_kwargs)

    # ------------------------------------------------------------------ #
    # Lesson plan
    # ------------------------------------------------------------------ #
    def lesson_plan(
        self,
        topic: str,
        grade_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> Any:
        """Generate a structured, engaging lesson plan."""
        model = response_model or LessonPlan
        prompt = prompt_template or (
            f"Create a comprehensive, engaging lesson plan for the topic: {topic}.\n"
            f"{'Grade level: ' + grade_level if grade_level else ''}\n"
            "Include a title, subject, learning objectives, an engaging "
            "introduction (with a hook), 2-3 main topics each with subtopics "
            "(key concepts, discussion questions, hands-on activities, "
            "reflective questions, assessment ideas), learning adaptations, "
            "real-world applications, and ethical considerations. Follow Bloom's "
            "Taxonomy and cater to diverse learning styles."
        )
        for key, value in context.items():
            if value:
                prompt += f"\n{key.replace('_', ' ').title()}: {value}"
        return self._generate(model, prompt, custom_instructions)

    # ------------------------------------------------------------------ #
    # Study guide
    # ------------------------------------------------------------------ #
    def study_guide(
        self,
        topic: str,
        difficulty_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> Any:
        """Generate a comprehensive study guide."""
        model = response_model or StudyGuide
        prompt = prompt_template or (
            f"Create a comprehensive study guide for the topic: {topic}.\n"
            f"Difficulty level: {difficulty_level or 'Intermediate'}.\n"
            "Include estimated study time, prerequisites, clear learning "
            "objectives, an overview, key concepts with detailed explanations, "
            "important dates (if relevant), practice exercises (with solutions), "
            "real-world case studies, study tips, additional resources, and a "
            "summary of key takeaways."
        )
        return self._generate(model, prompt, custom_instructions)

    # ------------------------------------------------------------------ #
    # Career connections
    # ------------------------------------------------------------------ #
    def career_connections(
        self,
        topic: str,
        industry_focus: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> Any:
        """Connect an academic topic to real-world careers."""
        model = response_model or CareerConnections
        prompt = prompt_template or (
            f"Create comprehensive career connections for the topic: {topic}.\n"
            f"Industry focus: {industry_focus or 'General'}.\n"
            "Include an industry overview, detailed career paths (responsibilities, "
            "education, salary range, growth potential, how the topic applies, "
            "required skills), industry trends, professional insights, preparation "
            "paths, resources, and categorised skills."
        )
        return self._generate(model, prompt, custom_instructions)

    # ------------------------------------------------------------------ #
    # Flashcards
    # ------------------------------------------------------------------ #
    def flashcards(
        self,
        topic: str,
        num: int = 10,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> FlashcardSet:
        """Generate a set of flashcards."""
        model = response_model or FlashcardSet
        prompt = prompt_template or (
            f"Generate a set of {num} flashcards on the topic: {topic}. Use the "
            "topic as the set title. For each flashcard provide a front (question "
            "or key term), a back (answer or definition), and an optional "
            "explanation. Cover key concepts, terminology, and important facts."
        )
        return self._generate(model, prompt, custom_instructions)

    # ------------------------------------------------------------------ #
    # Pedagogy-driven content
    # ------------------------------------------------------------------ #
    def pedagogy(
        self,
        topic: str,
        approach: str,
        custom_instructions: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Generate content using a named pedagogical approach.

        See :meth:`list_pedagogies` for available approaches and parameters.
        """
        if approach not in _PEDAGOGY_CONFIGS:
            raise ValueError(
                f"Unknown pedagogy '{approach}'. Available: "
                f"{', '.join(_PEDAGOGY_CONFIGS)}."
            )
        config = _PEDAGOGY_CONFIGS[approach]
        params = dict(config["defaults"])
        params.update({k: v for k, v in kwargs.items() if k in params})
        prompt = config["template"].format(topic=topic, **params)
        return self._generate(config["model"], prompt, custom_instructions)

    @staticmethod
    def list_pedagogies() -> Dict[str, Dict[str, Any]]:
        """Describe the available pedagogy approaches and their parameters."""
        return {
            name: {
                "description": cfg["description"],
                "parameters": cfg["defaults"],
            }
            for name, cfg in _PEDAGOGY_CONFIGS.items()
        }

    # ------------------------------------------------------------------ #
    # Podcasts
    # ------------------------------------------------------------------ #
    def podcast_script(
        self,
        topic: str,
        target_audience: Optional[str] = None,
        duration: Optional[str] = None,
        tone: Optional[str] = None,
        num_segments: int = 3,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **context: Any,
    ) -> PodcastScript:
        """Generate a structured, audio-ready podcast script."""
        model = response_model or PodcastScript
        prompt = prompt_template or (
            f"Create an engaging, educational podcast script on: {topic}.\n"
            f"Target audience: {target_audience or 'General audience'}.\n"
            f"Estimated duration: {duration or '10-15 minutes'}.\n"
            f"Tone: {tone or 'conversational'}.\n"
            f"Use {num_segments} main segments. Include a warm introduction with "
            "a hook, segments (each with a title, audio-friendly content, "
            "estimated duration, speaker and tone), a conclusion, 3-5 key "
            "takeaways, and a call to action. Write for the ear - conversational "
            "and easy to follow when spoken aloud."
        )
        return self._generate(model, prompt, custom_instructions)

    def podcast_from_script(
        self,
        script: str,
        output_path: str,
        language: str = "en",
        enhance_audio: bool = True,
        voice_settings: Optional[Dict[str, Any]] = None,
        tts_provider: str = "google",
        tts_voice: Optional[str] = None,
        tts_model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> PodcastContent:
        """Synthesise audio from a podcast script string."""
        import os

        from educhain.utils.audio_utils import AudioProcessor

        audio_processor = AudioProcessor(default_provider=tts_provider)
        settings: Dict[str, Any] = {
            "slow": False,
            "tld": "com",
            "volume_adjustment": 0.0,
            "fade_in": 1000,
            "fade_out": 1000,
            "normalize": True,
            "provider": tts_provider,
        }
        if voice_settings:
            settings.update(voice_settings)
        if tts_voice:
            settings["voice"] = tts_voice
        if tts_model:
            settings["model"] = tts_model

        result = audio_processor.text_to_speech(
            text=script,
            output_path=output_path,
            language=language,
            slow=settings.get("slow", False),
            tld=settings.get("tld", "com"),
            provider=tts_provider,
            voice=tts_voice,
            model=tts_model,
            api_key=api_key,
        )
        if not result.get("success"):
            raise Exception(f"TTS generation failed: {result.get('error', 'Unknown error')}")

        if enhance_audio:
            enhanced = output_path.replace(".mp3", "_enhanced.mp3")
            enhance_result = audio_processor.enhance_audio(
                input_path=output_path,
                output_path=enhanced,
                volume_adjustment=settings["volume_adjustment"],
                fade_in=settings["fade_in"],
                fade_out=settings["fade_out"],
                normalize=settings["normalize"],
            )
            if enhance_result.get("success"):
                os.remove(output_path)
                os.rename(enhanced, output_path)
                result.update(enhance_result)

        script_obj = PodcastScript(
            title="Generated Podcast",
            topic="Custom Script",
            introduction=script[:200] + "..." if len(script) > 200 else script,
            segments=[],
            conclusion="Thank you for listening.",
        )
        return PodcastContent(
            script=script_obj,
            audio_file_path=output_path,
            audio_format="mp3",
            voice_settings=settings,
            generation_timestamp=datetime.now().isoformat(),
            file_size=result.get("file_size", "Unknown"),
        )

    def podcast(
        self,
        topic: str,
        output_path: str,
        target_audience: Optional[str] = None,
        duration: Optional[str] = None,
        tone: Optional[str] = None,
        language: str = "en",
        enhance_audio: bool = True,
        voice_settings: Optional[Dict[str, Any]] = None,
        custom_instructions: Optional[str] = None,
        tts_provider: str = "google",
        tts_voice: Optional[str] = None,
        tts_model: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> PodcastContent:
        """Generate a complete podcast (script + audio) for a topic."""
        script = self.podcast_script(
            topic=topic,
            target_audience=target_audience,
            duration=duration,
            tone=tone,
            custom_instructions=custom_instructions,
            **kwargs,
        )
        content = self.podcast_from_script(
            script=script.get_full_script(),
            output_path=output_path,
            language=language,
            enhance_audio=enhance_audio,
            voice_settings=voice_settings,
            tts_provider=tts_provider,
            tts_voice=tts_voice,
            tts_model=tts_model,
            api_key=api_key,
        )
        content.script = script
        return content

    # ================================================================== #
    # Deprecated aliases (pre-1.0 API)
    # ================================================================== #
    def generate_lesson_plan(self, topic, *args, **kwargs):
        _deprecated("generate_lesson_plan", "lesson_plan")
        kwargs.pop("llm", None)
        kwargs.pop("output_format", None)
        return self.lesson_plan(topic, *args, **kwargs)

    def generate_study_guide(self, topic, *args, **kwargs):
        _deprecated("generate_study_guide", "study_guide")
        kwargs.pop("llm", None)
        kwargs.pop("output_format", None)
        return self.study_guide(topic, *args, **kwargs)

    def generate_career_connections(self, topic, *args, **kwargs):
        _deprecated("generate_career_connections", "career_connections")
        kwargs.pop("llm", None)
        kwargs.pop("output_format", None)
        return self.career_connections(topic, *args, **kwargs)

    def generate_flashcards(self, topic, *args, **kwargs):
        _deprecated("generate_flashcards", "flashcards")
        kwargs.pop("llm", None)
        return self.flashcards(topic, *args, **kwargs)

    def generate_pedagogy_content(self, topic, pedagogy, custom_instructions=None, **kwargs):
        _deprecated("generate_pedagogy_content", "pedagogy")
        return self.pedagogy(topic, pedagogy, custom_instructions=custom_instructions, **kwargs)

    def get_available_pedagogies(self):
        _deprecated("get_available_pedagogies", "list_pedagogies")
        return self.list_pedagogies()

    def generate_podcast_script(self, topic, *args, **kwargs):
        _deprecated("generate_podcast_script", "podcast_script")
        kwargs.pop("llm", None)
        return self.podcast_script(topic, *args, **kwargs)

    def generate_podcast_from_script(self, script, output_path, *args, **kwargs):
        _deprecated("generate_podcast_from_script", "podcast_from_script")
        return self.podcast_from_script(script, output_path, *args, **kwargs)

    def generate_complete_podcast(self, topic, output_path, *args, **kwargs):
        _deprecated("generate_complete_podcast", "podcast")
        return self.podcast(topic, output_path, *args, **kwargs)


__all__ = ["ContentEngine", "CONTENT_SYSTEM_PROMPT"]
