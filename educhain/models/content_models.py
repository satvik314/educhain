from typing import Optional, Type, Any ,List, Dict
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown

class ContentElement(BaseModel):
    type: str = Field(..., description="The type of content element (e.g., definition, example, activity).")
    content: str = Field(..., description="The actual content of the element.")

class DiscussionQuestion(BaseModel):
    question: str = Field(..., description="A question to encourage critical thinking.")

class HandsOnActivity(BaseModel):
    title: str = Field(..., description="Title of the hands-on activity.")
    description: str = Field(..., description="Description of the hands-on activity.")

class ReflectiveQuestion(BaseModel):
    question: str = Field(..., description="A question to evaluate understanding.")

class AssessmentIdea(BaseModel):
    type: str = Field(..., description="Type of assessment (e.g., quiz, project, written task).")
    description: str = Field(..., description="Description of the assessment idea.")

class SubTopic(BaseModel):
    title: str = Field(..., description="The title of the subtopic.")
    key_concepts: List[ContentElement] = Field(..., description="List of key concepts under this subtopic.")
    discussion_questions: List[DiscussionQuestion] = Field(..., description="List of discussion questions.")
    hands_on_activities: List[HandsOnActivity] = Field(..., description="List of hands-on activities.")
    reflective_questions: List[ReflectiveQuestion] = Field(..., description="List of reflective questions.")
    assessment_ideas: List[AssessmentIdea] = Field(..., description="List of assessment ideas.")

class MainTopic(BaseModel):
    title: str = Field(..., description="The title of the main topic.")
    subtopics: List[SubTopic] = Field(..., description="List of subtopics under this main topic.")

class LessonPlan(BaseModel):
    title: str = Field(..., description="The overall title of the lesson plan.")
    subject: str = Field(..., description="The subject area of the lesson.")
    learning_objectives: List[str] = Field(..., description="List of learning objectives tailored to different learning levels.")
    lesson_introduction: str = Field(..., description="Introduction to the lesson including a hook and real-world applications.")
    main_topics: List[MainTopic] = Field(..., description="A list of main topics covered in the lesson.")
    learning_adaptations: Optional[str] = Field(None, description="Learning adaptations for different grade levels.")
    real_world_applications: Optional[str] = Field(None, description="Discussion of real-world applications, careers, and future learning paths.")
    ethical_considerations: Optional[str] = Field(None, description="Discussion of ethical considerations and societal impact.")

    def show(self):
        print("=" * 80)
        print(f"Lesson Plan: {self.title}")
        print(f"Subject: {self.subject}")
        print(f"Learning Objectives: {', '.join(self.learning_objectives)}")
        print(f"Lesson Introduction: {self.lesson_introduction}")
        print("=" * 80)

        for i, main_topic in enumerate(self.main_topics, 1):
            print(f"\nMain Topic {i}: {main_topic.title}")
            for j, subtopic in enumerate(main_topic.subtopics, 1):
                print(f"\n   Subtopic {i}.{j}: {subtopic.title}")
                print("   Key Concepts:")
                for element in subtopic.key_concepts:
                    print(f"      - {element.type.capitalize()}: {element.content}")

                print("   Discussion Questions:")
                for dq in subtopic.discussion_questions:
                    print(f"      - {dq.question}")

                print("   Hands-On Activities:")
                for activity in subtopic.hands_on_activities:
                    print(f"      - {activity.title}: {activity.description}")

                print("   Reflective Questions:")
                for rq in subtopic.reflective_questions:
                    print(f"      - {rq.question}")

                print("   Assessment Ideas:")
                for assessment in subtopic.assessment_ideas:
                    print(f"      - {assessment.type.capitalize()}: {assessment.description}")

        print("\n" + "=" * 80)


class Flashcard(BaseModel):
    front: str = Field(..., description="The front side of the flashcard with a question or key term")
    back: str = Field(..., description="The back side of the flashcard with the answer or definition")
    explanation: Optional[str] = Field(None, description="An optional explanation or additional context")

class FlashcardSet(BaseModel):
    title: str = Field(..., description="The title or topic of the flashcard set")
    flashcards: List[Flashcard] = Field(..., description="A list of flashcards in this set")

    def show(self):
        print("=" * 80)
        print(f"Flashcard Set: {self.title}")
        print("=" * 80)
        for i, flashcard in enumerate(self.flashcards, 1):
            print(f"\n{i}. Front: {flashcard.front}")
            print(f"   Back: {flashcard.back}")
            if flashcard.explanation:
                print(f"   Explanation: {flashcard.explanation}")
        print("\n" + "=" * 80)
        print("\nLearning Adaptations: ", self.learning_adaptations or "None")
        print("Real-World Applications: ", self.real_world_applications or "None")
        print("Ethical Considerations: ", self.ethical_considerations or "None")

class CaseStudy(BaseModel):
    title: str
    scenario: str
    challenge: str
    solution: str
    outcome: str
    lessons_learned: List[str]
    related_concepts: List[str]

class StudyGuide(BaseModel):
    topic: str
    difficulty_level: Optional[str] = Field(None, description="Difficulty level of the study material (e.g., Beginner, Intermediate, Advanced)")
    estimated_study_time: Optional[str] = Field(None, description="Estimated time needed to cover the material")
    prerequisites: Optional[List[str]] = Field(default_factory=list, description="Required prerequisite knowledge")
    learning_objectives: List[str] = Field(default_factory=list, description="Specific learning objectives for the study guide")
    overview: str
    key_concepts: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary mapping concept names to their detailed explanations"
    )
    important_dates: Optional[Dict[str, str]] = Field(
        None,
        description="Dictionary mapping dates to their significance"
    )
    practice_exercises: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of practice exercises with solutions"
    )
    case_studies: Optional[List[CaseStudy]] = Field(
        None,
        description="Real-world case studies demonstrating practical applications"
    )
    study_tips: Optional[List[str]] = Field(
        None,
        description="Study strategies specific to this topic"
    )
    additional_resources: Optional[Dict[str, str]] = Field(
        None,
        description="Dictionary mapping resource names to their descriptions/URLs"
    )
    summary: Optional[str] = Field(None, description="Brief summary of key takeaways")

    def show(self, format: str = "text"):
        """
        Display the study guide in various formats.
        
        Args:
            format (str): Output format - "text", "markdown", or "rich"
        """
        if format == "markdown":
            return self._generate_markdown()
        elif format == "rich":
            console = Console()
            console.print(Markdown(self._generate_markdown()))
        else:
            self._print_text_format()

    def _generate_markdown(self) -> str:
        """Generate a markdown representation of the study guide."""
        md = [f"# Study Guide: {self.topic}\n"]
        
        if self.difficulty_level:
            md.append(f"**Difficulty Level:** {self.difficulty_level}")
        if self.estimated_study_time:
            md.append(f"**Estimated Study Time:** {self.estimated_study_time}\n")
            
        if self.prerequisites:
            md.append("## Prerequisites")
            for prereq in self.prerequisites:
                md.append(f"- {prereq}")
            md.append("")
            
        md.append("## Learning Objectives")
        for obj in self.learning_objectives:
            md.append(f"- {obj}")
        md.append("")
            
        md.append("## Overview")
        md.append(f"{self.overview}\n")
        
        md.append("## Key Concepts")
        for concept, explanation in self.key_concepts.items():
            md.append(f"### {concept}")
            md.append(f"{explanation}\n")
            
        if self.important_dates:
            md.append("## Important Dates")
            for date, significance in self.important_dates.items():
                md.append(f"- **{date}**: {significance}")
            md.append("")
            
        if self.practice_exercises:
            md.append("## Practice Exercises")
            for i, exercise in enumerate(self.practice_exercises, 1):
                md.append(f"### Exercise {i}")
                md.append(f"**Problem:** {exercise['problem']}")
                md.append(f"**Solution:** {exercise['solution']}\n")

        if self.case_studies:
            md.append("## Real-World Case Studies")
            for i, case in enumerate(self.case_studies, 1):
                md.append(f"### Case Study {i}: {case.title}")
                md.append(f"**Scenario:** {case.scenario}")
                md.append(f"**Challenge:** {case.challenge}")
                md.append(f"**Solution:** {case.solution}")
                md.append(f"**Outcome:** {case.outcome}")
                md.append("\n**Key Lessons Learned:**")
                for lesson in case.lessons_learned:
                    md.append(f"- {lesson}")
                md.append("\n**Related Concepts:**")
                for concept in case.related_concepts:
                    md.append(f"- {concept}")
                md.append("")
                
        if self.study_tips:
            md.append("## Study Tips")
            for tip in self.study_tips:
                md.append(f"- {tip}")
            md.append("")
            
        if self.additional_resources:
            md.append("## Additional Resources")
            for resource, description in self.additional_resources.items():
                md.append(f"- **{resource}**: {description}")
            md.append("")
            
        if self.summary:
            md.append("## Summary")
            md.append(self.summary)
            
        return "\n".join(md)

    def _print_text_format(self):
        """Print the study guide in plain text format."""
        print(f"=== Study Guide: {self.topic} ===\n")
        
        if self.difficulty_level:
            print(f"Difficulty Level: {self.difficulty_level}")
        if self.estimated_study_time:
            print(f"Estimated Study Time: {self.estimated_study_time}\n")
            
        if self.prerequisites:
            print("Prerequisites:")
            for prereq in self.prerequisites:
                print(f"- {prereq}")
            print()
            
        print("Learning Objectives:")
        for obj in self.learning_objectives:
            print(f"- {obj}")
        print()
            
        print(f"Overview:\n{self.overview}\n")
        
        print("Key Concepts:")
        for concept, explanation in self.key_concepts.items():
            print(f"\n{concept}:")
            print(f"{explanation}")
            
        if self.important_dates:
            print("\nImportant Dates:")
            for date, significance in self.important_dates.items():
                print(f"- {date}: {significance}")
            
        if self.practice_exercises:
            print("\nPractice Exercises:")
            for i, exercise in enumerate(self.practice_exercises, 1):
                print(f"\nExercise {i}:")
                print(f"Problem: {exercise['problem']}")
                print(f"Solution: {exercise['solution']}")

        if self.case_studies:
            print("\nReal-World Case Studies:")
            for i, case in enumerate(self.case_studies, 1):
                print(f"\nCase Study {i}: {case.title}")
                print(f"Scenario: {case.scenario}")
                print(f"Challenge: {case.challenge}")
                print(f"Solution: {case.solution}")
                print(f"Outcome: {case.outcome}")
                print("\nKey Lessons Learned:")
                for lesson in case.lessons_learned:
                    print(f"- {lesson}")
                print("\nRelated Concepts:")
                for concept in case.related_concepts:
                    print(f"- {concept}")
                print("-" * 50)
                
        if self.study_tips:
            print("\nStudy Tips:")
            for tip in self.study_tips:
                print(f"- {tip}")
                
        if self.additional_resources:
            print("\nAdditional Resources:")
            for resource, description in self.additional_resources.items():
                print(f"- {resource}: {description}")
                
        if self.summary:
            print(f"\nSummary:\n{self.summary}")

# Carrer Connection
class Skill(BaseModel):
    name: str = Field(..., description="Name of the skill")
    description: str = Field(..., description="Detailed description of the skill")
    importance_level: str = Field(..., description="How important this skill is for the career (Essential/Important/Helpful)")
    acquisition_methods: List[str] = Field(..., description="Ways to acquire or develop this skill")

class CareerPath(BaseModel):
    title: str = Field(..., description="Job title or role name")
    description: str = Field(..., description="Detailed description of the career path")
    typical_responsibilities: List[str] = Field(..., description="List of typical job responsibilities")
    required_education: str = Field(..., description="Required educational qualifications")
    salary_range: str = Field(..., description="Typical salary range for this role")
    growth_potential: str = Field(..., description="Career growth and advancement opportunities")
    topic_application: str = Field(..., description="How the academic topic is applied in this role")
    required_skills: List[Skill] = Field(..., description="Skills required for this career path")

class ProfessionalInsight(BaseModel):
    role: str = Field(..., description="Professional's current role")
    experience_level: str = Field(..., description="Years of experience in the field")
    company_type: str = Field(..., description="Type of company or industry sector")
    key_insights: List[str] = Field(..., description="Key insights about the career path")
    daily_applications: List[str] = Field(..., description="How they apply the topic in daily work")
    advice_for_students: List[str] = Field(..., description="Professional advice for students")
    career_journey: str = Field(..., description="Brief description of their career journey")

class IndustryTrend(BaseModel):
    name: str = Field(..., description="Name of the trend")
    description: str = Field(..., description="Detailed description of the trend")
    impact: str = Field(..., description="Expected impact on the industry")
    timeframe: str = Field(..., description="Expected timeframe for this trend")
    related_skills: List[str] = Field(..., description="Skills related to this trend")

class Resource(BaseModel):
    name: str = Field(..., description="Name of the resource")
    type: str = Field(..., description="Type of resource (Organization/Platform/Publication)")
    description: str = Field(..., description="Description of the resource")
    url: Optional[str] = Field(None, description="URL for the resource if applicable")
    cost: Optional[str] = Field(None, description="Cost information if applicable")

class PreparationPath(BaseModel):
    stage: str = Field(..., description="Stage of preparation (e.g., Education, Early Career)")
    requirements: List[str] = Field(..., description="Requirements for this stage")
    duration: str = Field(..., description="Expected duration of this stage")
    milestones: List[str] = Field(..., description="Key milestones to achieve")
    resources_needed: List[str] = Field(..., description="Resources needed for this stage")

class CareerConnections(BaseModel):
    topic: str = Field(..., description="The academic topic being connected to careers")
    industry_overview: str = Field(..., description="Overview of the industry landscape")
    career_paths: List[CareerPath] = Field(..., description="Detailed career paths related to the topic")
    industry_trends: List[IndustryTrend] = Field(..., description="Current and emerging industry trends")
    professional_insights: List[ProfessionalInsight] = Field(..., description="Insights from industry professionals")
    preparation_paths: List[PreparationPath] = Field(..., description="Steps to prepare for these careers")
    resources: List[Resource] = Field(..., description="Useful resources for career preparation")
    skill_categories: Dict[str, List[Skill]] = Field(..., description="Categorized skills required across careers")

    def show(self):
        print("=" * 80)
        print(f"Career Connections: {self.topic}")
        print("=" * 80)
        print("\nIndustry Overview:")
        print(self.industry_overview)
        
        print("\nCareer Paths:")
        for i, path in enumerate(self.career_paths, 1):
            print(f"\n{i}. {path.title}")
            print(f"   Description: {path.description}")
            print("   Responsibilities:")
            for resp in path.typical_responsibilities:
                print(f"   - {resp}")
            print(f"   Education: {path.required_education}")
            print(f"   Salary Range: {path.salary_range}")
            print(f"   Growth Potential: {path.growth_potential}")
            print("   Required Skills:")
            for skill in path.required_skills:
                print(f"   - {skill.name} ({skill.importance_level})")

        print("\nIndustry Trends:")
        for trend in self.industry_trends:
            print(f"\n- {trend.name}")
            print(f"  Impact: {trend.impact}")
            print(f"  Timeframe: {trend.timeframe}")

        print("\nProfessional Insights:")
        for insight in self.professional_insights:
            print(f"\nFrom {insight.role} ({insight.experience_level})")
            print("Key Insights:")
            for key_insight in insight.key_insights:
                print(f"- {key_insight}")
            print("Advice for Students:")
            for advice in insight.advice_for_students:
                print(f"- {advice}")

        print("\nPreparation Paths:")
        for path in self.preparation_paths:
            print(f"\n{path.stage}")
            print("Requirements:")
            for req in path.requirements:
                print(f"- {req}")
            print(f"Duration: {path.duration}")

        print("\nResources:")
        for resource in self.resources:
            print(f"\n- {resource.name} ({resource.type})")
            print(f"  Description: {resource.description}")
            if resource.url:
                print(f"  URL: {resource.url}")
            if resource.cost:
                print(f"  Cost: {resource.cost}")

        print("\nSkill Categories:")
        for category, skills in self.skill_categories.items():
            print(f"\n{category}:")
            for skill in skills:
                print(f"- {skill.name}: {skill.description}")
