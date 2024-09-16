from educhain import Educhain, EduchainConfig, LLMConfig ,DoubtSolver , AdaptiveQuiz
import os

##Optional!
llm_config = LLMConfig(
        api_key=os.environ["OPENAI_API_KEY"],
        max_tokens=1500,
        temperature=0.7,  # Controls randomness: 0.0 is deterministic, 1.0 is very random
        model_name="gpt-4o-mini"
    )

    # Create Educhain configuration
config = EduchainConfig(llm_config=llm_config)
#If custom config is needed

educhain = Educhain(config) 

#Default model used
# educhain = Educhain()

## Testing Question Generation
print("Testing Question Generation")
ques = educhain.generate_mcq("Python programming", num=2 , custom_instructions="Please provide a detailed lesson plan for a 60-minute lesson on machine learning.")
print(ques)

#Testing generate mcq_from data
print("Testing generate mcq_from data")
mcqs = educhain.generate_mcqs_from_data(
        "The Earth is the third planet from the Sun and the only astronomical object known to harbor life.",
        source_type="text",
        num=2
)
print(mcqs)

Testing generate questions
print("Testing generate questions")
ques = educhain.generate_questions("Python programming", num=2, type="Fill in the Blank")
print(ques)


# Testing Doubt Solver
print("Testing Doubt Solver")
img = r"C:\Users\admin\Downloads\cat.4005.jpg"
prompt = "Explain this image"
doubt_solver = DoubtSolver(config)
ans = doubt_solver.solve(img,prompt)
print(ans)

print("Testing Lesson Plan Generation")
lesson_plan = educhain.generate_lesson_plan(
        topic="Introduction to Machine Learning",
        custom_instructions="Please provide a detailed lesson plan for a 60-minute lesson on machine learning."
        
    )
    
print(lesson_plan)

print("Generating questions from youtube video")
ques = educhain.generate_questions_from_youtube(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", num=2)
print(ques)


#Testing Adaptive Quiz
adaptive_quiz = AdaptiveQuiz(
    config=config,
    qna_engine=
    topic="Python programming",
    num_questions=5,
    custom_instruction="Focus on basic Python concepts",
    show_options=True
)

# Start the quiz
print("Starting Adaptive Quiz")
adaptive_quiz.start_quiz()
