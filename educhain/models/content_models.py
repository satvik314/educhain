from typing import List
from pydantic import BaseModel, Field

class ContentElement(BaseModel):
    type: str = Field(..., description="The type of content element, e.g., 'definition', 'example', 'explanation', 'activity'")
    content: str = Field(..., description="The actual content of the element")

class SubTopic(BaseModel):
    title: str = Field(..., description="The title of the subtopic")
    content_elements: List[ContentElement] = Field(..., description="A list of content elements that make up this subtopic")

class MainTopic(BaseModel):
    title: str = Field(..., description="The title of the main topic")
    subtopics: List[SubTopic] = Field(..., description="A list of subtopics that make up this main topic")

class LessonPlan(BaseModel):
    title: str = Field(..., description="The overall title of the lesson plan")
    subject: str = Field(..., description="The subject area of the lesson")
    main_topics: List[MainTopic] = Field(..., description="A list of main topics covered in the lesson")

    def show(self):
        print("=" * 80)
        print(f"Lesson Plan: {self.title}")
        print(f"Subject: {self.subject}")
        print("=" * 80)

        for i, main_topic in enumerate(self.main_topics, 1):
            print(f"\n{i}. {main_topic.title}")
            for j, subtopic in enumerate(main_topic.subtopics, 1):
                print(f"\n   {i}.{j} {subtopic.title}")
                for element in subtopic.content_elements:
                    print(f"      - {element.content}")

        print("\n" + "=" * 80)