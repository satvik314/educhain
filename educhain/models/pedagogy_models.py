from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class CognitiveLevel(BaseModel):
    """Represents a cognitive level in Bloom's Taxonomy."""
    level_name: str = Field(..., description="Name of the cognitive level")
    description: str = Field(..., description="Description of the cognitive level")
    content: str = Field(default="", description="Detailed educational content for this cognitive level")
    learning_objectives: List[str] = Field(..., description="Learning objectives for this level")
    activities: List[str] = Field(..., description="Activities that engage this cognitive level")
    assessment_questions: List[str] = Field(..., description="Questions that assess this level")
    real_world_examples: List[str] = Field(..., description="Real-world applications")
    key_concepts: List[str] = Field(default_factory=list, description="Key concepts covered at this level")


class BloomsTaxonomyContent(BaseModel):
    """Content structured according to Bloom's Taxonomy."""
    topic: str = Field(..., description="The learning topic")
    target_level: Optional[str] = Field(None, description="Primary cognitive level focus")
    grade_level: Optional[str] = Field(None, description="Target grade level")
    cognitive_levels: List[CognitiveLevel] = Field(default_factory=list, description="Content for each cognitive level")
    learning_progression: str = Field("", description="How to progress through the levels")
    assessment_strategy: str = Field("", description="Overall assessment approach")

    def show(self):
        print(f"=== Bloom's Taxonomy Content: {self.topic} ===\n")
        if self.target_level:
            print(f"Target Level: {self.target_level}")
        if self.grade_level:
            print(f"Grade Level: {self.grade_level}\n")
        
        for level in self.cognitive_levels:
            print(f"--- {level.level_name.upper()} ---")
            print(f"Description: {level.description}")
            print("Learning Objectives:")
            for obj in level.learning_objectives:
                print(f"  • {obj}")
            print("Activities:")
            for activity in level.activities:
                print(f"  • {activity}")
            print()


class QuestionSequence(BaseModel):
    """Represents a sequence of Socratic questions."""
    category: str = Field(..., description="Category of questions")
    description: str = Field(..., description="Purpose of this question category")
    content_overview: str = Field(default="", description="Content overview for this question category")
    questions: List[str] = Field(..., description="List of questions in this category")
    follow_up_probes: List[str] = Field(..., description="Follow-up questions for deeper inquiry")
    example_responses: List[str] = Field(default_factory=list, description="Example student responses and guidance")
    facilitation_notes: str = Field("", description="Notes for educators on facilitation")


class SocraticQuestioningContent(BaseModel):
    """Content for Socratic questioning approach."""
    topic: str = Field(..., description="The learning topic")
    depth_level: Optional[str] = Field(None, description="Depth of inquiry")
    student_level: Optional[str] = Field(None, description="Student level")
    question_sequences: List[QuestionSequence] = Field(default_factory=list, description="Sequences of questions")
    discussion_guidelines: str = Field("", description="Guidelines for facilitating discussions")
    assessment_approach: str = Field("", description="How to assess learning through dialogue")

    def show(self):
        print(f"=== Socratic Questioning: {self.topic} ===\n")
        for sequence in self.question_sequences:
            print(f"--- {sequence.category.upper()} ---")
            print(f"Purpose: {sequence.description}")
            print("Key Questions:")
            for question in sequence.questions:
                print(f"  ? {question}")
            print()


class ProjectPhase(BaseModel):
    """Represents a phase in a project."""
    phase_name: str = Field(..., description="Name of the project phase")
    duration: str = Field(..., description="Expected duration of this phase")
    content_description: str = Field(default="", description="Detailed content and materials for this phase")
    objectives: List[str] = Field(..., description="Objectives for this phase")
    activities: List[str] = Field(..., description="Activities in this phase")
    deliverables: List[str] = Field(..., description="Expected deliverables")
    resources_needed: List[str] = Field(default_factory=list, description="Resources and materials needed")
    assessment_criteria: List[str] = Field(..., description="How this phase is assessed")


class ProjectBasedLearningContent(BaseModel):
    """Content for project-based learning."""
    topic: str = Field(..., description="The learning topic")
    driving_question: str = Field("", description="Central question that drives the project")
    project_overview: str = Field("", description="Overview of the project")
    learning_objectives: List[str] = Field(default_factory=list, description="What students will learn")
    project_phases: List[ProjectPhase] = Field(default_factory=list, description="Phases of the project")
    final_deliverables: List[str] = Field(default_factory=list, description="Final project outputs")
    real_world_connections: str = Field("", description="How project connects to real world")
    collaboration_strategy: str = Field("", description="How students will work together")

    def show(self):
        print(f"=== Project-Based Learning: {self.topic} ===\n")
        print(f"Driving Question: {self.driving_question}\n")
        print(f"Overview: {self.project_overview}\n")
        for i, phase in enumerate(self.project_phases, 1):
            print(f"--- Phase {i}: {phase.phase_name} ---")
            print(f"Duration: {phase.duration}")
            print("Activities:")
            for activity in phase.activities:
                print(f"  • {activity}")
            print()


class PreClassContent(BaseModel):
    """Pre-class preparation content."""
    content_type: str = Field(..., description="Type of content (video, reading, etc.)")
    title: str = Field(..., description="Title of the content")
    description: str = Field(..., description="Description of the content")
    full_content: str = Field(default="", description="Complete content for students to study")
    estimated_time: str = Field(..., description="Estimated time to complete")
    learning_objectives: List[str] = Field(..., description="What students should learn")
    key_points: List[str] = Field(default_factory=list, description="Key points to remember")


class InClassActivity(BaseModel):
    """In-class activity for flipped classroom."""
    activity_name: str = Field(..., description="Name of the activity")
    duration: str = Field(..., description="Duration of the activity")
    description: str = Field(..., description="Description of the activity")
    detailed_instructions: str = Field(default="", description="Step-by-step instructions for the activity")
    materials_needed: List[str] = Field(..., description="Materials required")
    assessment_method: str = Field("", description="How to assess this activity")


class FlippedClassroomContent(BaseModel):
    """Content for flipped classroom approach."""
    topic: str = Field(..., description="The learning topic")
    class_duration: Optional[str] = Field(None, description="Duration of class session")
    pre_class_content: List[PreClassContent] = Field(default_factory=list, description="Content for home study")
    in_class_activities: List[InClassActivity] = Field(default_factory=list, description="In-class activities")
    post_class_reinforcement: List[str] = Field(default_factory=list, description="Post-class activities")
    assessment_strategy: str = Field("", description="Overall assessment approach")
    technology_tools: List[str] = Field(default_factory=list, description="Technology tools used")

    def show(self):
        print(f"=== Flipped Classroom: {self.topic} ===\n")
        print("Pre-Class Content:")
        for content in self.pre_class_content:
            print(f"  • {content.title} ({content.content_type}) - {content.estimated_time}")
        print("\nIn-Class Activities:")
        for activity in self.in_class_activities:
            print(f"  • {activity.activity_name} ({activity.duration})")
        print()


class InvestigationPhase(BaseModel):
    """Phase of inquiry-based investigation."""
    phase_name: str = Field(..., description="Name of the investigation phase")
    content_guide: str = Field(default="", description="Detailed content guide for this investigation phase")
    objectives: List[str] = Field(..., description="Objectives for this phase")
    activities: List[str] = Field(..., description="Activities in this phase")
    research_methods: List[str] = Field(..., description="Research methods to use")
    support_materials: List[str] = Field(..., description="Materials to support students")
    example_investigations: List[str] = Field(default_factory=list, description="Example investigations students can conduct")


class InquiryBasedLearningContent(BaseModel):
    """Content for inquiry-based learning."""
    topic: str = Field(..., description="The learning topic")
    essential_questions: List[str] = Field(default_factory=list, description="Essential questions driving inquiry")
    investigation_phases: List[InvestigationPhase] = Field(default_factory=list, description="Phases of investigation")
    research_skills: List[str] = Field(default_factory=list, description="Research skills students will develop")
    presentation_formats: List[str] = Field(default_factory=list, description="Ways students can present findings")
    assessment_rubric: str = Field("", description="How to assess inquiry learning")

    def show(self):
        print(f"=== Inquiry-Based Learning: {self.topic} ===\n")
        print("Essential Questions:")
        for question in self.essential_questions:
            print(f"  ? {question}")
        print("\nInvestigation Phases:")
        for phase in self.investigation_phases:
            print(f"  • {phase.phase_name}")
        print()


class ConstructivistActivity(BaseModel):
    """Activity for constructivist learning."""
    activity_name: str = Field(..., description="Name of the activity")
    type: str = Field(..., description="Type of activity (experiential, social, reflective)")
    description: str = Field(..., description="Description of the activity")
    detailed_content: str = Field(default="", description="Detailed content and materials for the activity")
    step_by_step_guide: List[str] = Field(..., description="Step-by-step guide to conduct the activity")
    learning_outcome: str = Field(..., description="Expected learning outcome")
    facilitation_notes: str = Field("", description="Notes for facilitators")


class ConstructivistContent(BaseModel):
    """Content for constructivist learning approach."""
    topic: str = Field(..., description="The learning topic")
    prior_knowledge_activities: List[ConstructivistActivity] = Field(default_factory=list, description="Activities to activate prior knowledge")
    experiential_activities: List[ConstructivistActivity] = Field(default_factory=list, description="Hands-on learning activities")
    social_construction_activities: List[ConstructivistActivity] = Field(default_factory=list, description="Collaborative learning activities")
    reflection_activities: List[ConstructivistActivity] = Field(default_factory=list, description="Reflection and metacognition activities")
    assessment_approach: str = Field("", description="Constructivist assessment strategy")

    def show(self):
        print(f"=== Constructivist Learning: {self.topic} ===\n")
        print("Experiential Activities:")
        for activity in self.experiential_activities:
            print(f"  • {activity.activity_name}: {activity.description}")
        print("\nSocial Construction Activities:")
        for activity in self.social_construction_activities:
            print(f"  • {activity.activity_name}: {activity.description}")
        print()


class GameMechanic(BaseModel):
    """Game mechanic for gamification."""
    mechanic_name: str = Field(..., description="Name of the game mechanic")
    description: str = Field(..., description="How the mechanic works")
    detailed_implementation: str = Field(default="", description="Detailed implementation guide")
    learning_connection: str = Field(..., description="How it connects to learning")
    content_integration: str = Field(default="", description="How content is integrated into this mechanic")
    implementation_notes: str = Field("", description="Notes on implementation")


class GamificationContent(BaseModel):
    """Content for gamified learning."""
    topic: str = Field(..., description="The learning topic")
    game_narrative: str = Field("", description="Overarching story or theme")
    game_mechanics: List[GameMechanic] = Field(default_factory=list, description="Game mechanics used")
    progression_system: str = Field("", description="How players progress through the game")
    assessment_integration: str = Field("", description="How assessment is integrated into gameplay")
    motivation_strategy: str = Field("", description="Strategy for maintaining motivation")
    technology_requirements: List[str] = Field(default_factory=list, description="Technology needed")

    def show(self):
        print(f"=== Gamified Learning: {self.topic} ===\n")
        print(f"Game Narrative: {self.game_narrative}\n")
        print("Game Mechanics:")
        for mechanic in self.game_mechanics:
            print(f"  • {mechanic.mechanic_name}: {mechanic.description}")
        print()


class CollaborationStructure(BaseModel):
    """Structure for peer collaboration."""
    structure_name: str = Field(..., description="Name of the collaboration structure")
    group_size: str = Field(..., description="Recommended group size")
    process_description: str = Field(..., description="How the collaboration works")
    detailed_content: str = Field(default="", description="Detailed content and materials for this collaboration")
    step_by_step_process: List[str] = Field(..., description="Step-by-step process for the collaboration")
    roles_and_responsibilities: List[str] = Field(..., description="Student roles in the collaboration")
    assessment_method: str = Field("", description="How to assess this collaboration")


class PeerLearningContent(BaseModel):
    """Content for peer learning approaches."""
    topic: str = Field(..., description="The learning topic")
    collaboration_structures: List[CollaborationStructure] = Field(default_factory=list, description="Different collaboration approaches")
    group_formation_strategy: str = Field("", description="How to form groups")
    communication_protocols: List[str] = Field(default_factory=list, description="Guidelines for peer communication")
    accountability_measures: List[str] = Field(default_factory=list, description="Ways to ensure accountability")
    facilitation_guidelines: str = Field("", description="How instructors should facilitate")

    def show(self):
        print(f"=== Peer Learning: {self.topic} ===\n")
        print("Collaboration Structures:")
        for structure in self.collaboration_structures:
            print(f"  • {structure.structure_name} ({structure.group_size})")
            print(f"    {structure.process_description}")
        print()