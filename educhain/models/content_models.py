from typing import List, Optional
from pydantic import BaseModel, Field

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

        print("\nLearning Adaptations: ", self.learning_adaptations or "None")
        print("Real-World Applications: ", self.real_world_applications or "None")
        print("Ethical Considerations: ", self.ethical_considerations or "None")