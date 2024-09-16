from typing import List, Optional, Any
from config import EduchainConfig, LLMConfig
from qna_engine import QnAEngine, AdaptiveQuiz
from content_engine import ContentEngine, DoubtSolver
from models import MCQList, LessonPlan, QuestionPaper, SolvedDoubt, QuestionList
import os

class Educhain:
    def __init__(self, config: Optional[EduchainConfig] = None):
        
        self.config = config or EduchainConfig()
        self.qna_engine = QnAEngine(self.config)
        self.content_engine = ContentEngine(self.config)
        self.doubt_solver = DoubtSolver(self.config)
        
    def generate_mcq(self, topic: str, num: int = 1, **kwargs) -> MCQList:
        return self.qna_engine.generate_mcq(topic, num, **kwargs)

    def generate_lesson_plan(self, topic: str, **kwargs) -> LessonPlan:
        return self.content_engine.generate_lesson_plan(topic, **kwargs)

    def generate_question_paper(self, subject: str, grade_level: int, num_questions: int, **kwargs) -> QuestionPaper:
        return self.content_engine.generate_question_paper(subject, grade_level, num_questions, **kwargs)

    def create_adaptive_quiz(self, topic: str, num_questions: int = 5, **kwargs) -> AdaptiveQuiz:
        return AdaptiveQuiz(self.config, self.qna_engine, topic, num_questions, **kwargs)

    def solve_doubt(self, img_path: str, prompt: str = "Explain this math problem", **kwargs) -> SolvedDoubt:
        return self.doubt_solver.solve(img_path, prompt, **kwargs)
    
    def generate_mcqs_from_data(self, data: str, source_type: str = "text", num: int = 1, **kwargs) -> MCQList:
        return self.qna_engine.generate_mcqs_from_data(data, source_type, num, **kwargs)
    
    def generate_questions_from_youtube(self, url: str, num: int = 1, **kwargs) -> QuestionList:
        return self.qna_engine.generate_questions_from_youtube(url, num, **kwargs)
    
    def generate_questions(self, topic: str, num: int = 1, type: str = "Multiple Choice", **kwargs) -> QuestionList:
        return self.qna_engine.generate_questions(topic, num, type, **kwargs)
