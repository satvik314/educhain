from typing import Optional, Type, Any
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from educhain.core.config import LLMConfig

from educhain.models.content_models import StudyGuide, CareerConnections
import json
from educhain.models.content_models import LessonPlan
from educhain.models.content_models import FlashcardSet
from educhain.models.pedagogy_models import (
    BloomsTaxonomyContent, 
    SocraticQuestioningContent, 
    ProjectBasedLearningContent,
    FlippedClassroomContent,
    InquiryBasedLearningContent,
    ConstructivistContent,
    GamificationContent,
    PeerLearningContent
) 


class ContentEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()
        self.llm = self._initialize_llm(llm_config)

    def _initialize_llm(self, llm_config: LLMConfig):
        if llm_config.custom_model:
            return llm_config.custom_model
        else:
            return ChatOpenAI(
                model=llm_config.model_name,
                api_key=llm_config.api_key,
                max_tokens=llm_config.max_tokens,
                temperature=llm_config.temperature,
                base_url=llm_config.base_url,
                default_headers=llm_config.default_headers
            )

    # Lesson Plan
    def generate_lesson_plan(
        self,
        topic: str,
        grade_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        output_format: Optional[str] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            response_model = LessonPlan

        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Create a highly engaging and comprehensive lesson plan for the following topic:
            Topic: {topic}

            The lesson plan should be structured in a way that engages students through a variety of methods.
            The structure should include the following elements:
            1. Title of the lesson
            2. Subject area
            3. Learning objectives (at least 3, tailored to different learning levels or grades)
            4. Lesson introduction (including a hook to grab attention, real-world applications, or provocative questions)
            5. Main topics (2-3), each should include:
                a. Title
                b. Subtopics (2-3)
                c. For each subtopic:
                    - Key Concepts (definitions, examples, illustrations, multimedia)
                    - Discussion Questions (to encourage critical thinking and engagement)
                    - Hands-on Activities or Project-Based Learning (interactive, real-world tasks)
                    - Reflective Questions (to evaluate understanding)
                    - Assessment Ideas (quiz, project, or written task to assess mastery)
            6. Learning adaptations for different grade levels (if applicable)
            7. A section on real-world applications, including careers and future learning paths
            8. Ethical considerations and societal impact (if applicable)

            Ensure that the lesson plan follows Bloom's Taxonomy principles with activities addressing different cognitive levels: remember, understand, apply, analyze, evaluate, and create.

            The lesson plan should cater to diverse learning styles (visual, auditory, kinesthetic, etc.) and include modern teaching methods such as collaborative learning and technology integration.

            Output the response in a structured and professional format.

            Response format: 
            {format_instructions}
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\n{format_instructions}"

        lesson_plan_prompt = PromptTemplate(
            input_variables=["topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm

        # Use LLM to generate lesson plan based on the topic
        lesson_plan_chain = lesson_plan_prompt | llm_to_use
        results = lesson_plan_chain.invoke(
            {"topic": topic, **kwargs},
        )
        results = results.content

        # Print raw output for debugging
        print("Raw output from LLM:")
        print(results)

        try:
            # Parse results to match the new LessonPlan structure
            structured_output = parser.parse(results)

            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return response_model()
        
    # Study Guide
    def generate_study_guide(
        self,
        topic: str,
        difficulty_level: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        output_format: Optional[str] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            response_model = StudyGuide

        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Create a comprehensive study guide for the following topic:
            Topic: {topic}
            Difficulty Level: {difficulty_level}

            The study guide should be engaging, well-structured, and suitable for self-study or classroom use.
            Include the following elements in your response:

            1. Difficulty level and estimated study time
            2. Prerequisites (if any)
            3. Clear learning objectives (3-5 specific, measurable objectives)
            4. Comprehensive overview of the topic
            5. Key concepts with detailed explanations
            6. Important dates and events (if applicable)
            8. Practice exercises formatted as:
            "practice_exercises": [
                {{
                    "title": "Exercise Title",
                    "problem": "Detailed problem description",
                    "solution": "Step-by-step solution",
                    "difficulty": "beginner|intermediate|advanced"
                }}
            ]
            9. Real-world case studies formatted as:
            "case_studies": [
                {{
                    "title": "Case Study Title",
                    "scenario": "Description of the real-world situation",
                    "challenge": "Specific problems or challenges faced",
                    "solution": "How the challenges were addressed",
                    "outcome": "Results and impact",
                    "lessons_learned": ["Key lesson 1", "Key lesson 2"],
                    "related_concepts": ["Concept 1", "Concept 2"]
                }}
            ]
            10. Study tips and strategies specific to the topic
            11. Additional resources for deeper learning
            12. Brief summary of key takeaways

            For the case studies:
            - Include at least one detailed real-world example
            - Focus on recent and relevant scenarios
            - Highlight practical applications of the concepts
            - Connect the case study to specific learning objectives
            - Emphasize problem-solving approaches
            - Include both successes and lessons learned
            - Make sure the examples are appropriate for the difficulty level

            Make sure all content is hands-on and directly related to real-world applications of {topic}.
            The study guide should accommodate different learning styles and include various types of learning activities.
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        study_guide_prompt = PromptTemplate(
            input_variables=["topic", "difficulty_level"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm

        study_guide_chain = study_guide_prompt | llm_to_use
        results = study_guide_chain.invoke(
            {
                "topic": topic,
                "difficulty_level": difficulty_level or "Intermediate",
                **kwargs
            },
        )
        results = results.content

        try:
            # Handle empty practice exercises
            if '"practice_exercises": []' in results or '"practice_exercises":[]' in results:
                results = results.replace(
                    '"practice_exercises": []',
                    '"practice_exercises": [{"title": "Basic Exercise", "problem": "No exercises provided", "solution": "N/A", "difficulty": "beginner"}]'
                )
                
            # Handle empty case studies
            if '"case_studies": []' in results or '"case_studies":[]' in results:
                results = results.replace(
                    '"case_studies": []',
                    '"case_studies": [{"title": "Sample Case", "scenario": "No case studies provided", "challenge": "N/A", "solution": "N/A", "outcome": "N/A", "lessons_learned": ["N/A"], "related_concepts": ["N/A"]}]'
                )

            # Parse results to match the new LessonPlan structure
            structured_output = parser.parse(results)

            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            # Return an instance with default values including case studies
            return response_model(
                topic=topic,
                overview="Error generating content",
                key_concepts={"Basic Concept": "Error generating concepts"},
                example_questions=[{"question": "Error generating questions", "answer": "N/A", "difficulty": "beginner"}],
                practice_exercises=[{
                    "title": "Basic Exercise",
                    "problem": "Error generating exercises",
                    "solution": "N/A",
                    "difficulty": "beginner"
                }],
                case_studies=[{
                    "title": "Sample Case",
                    "scenario": "Error generating case studies",
                    "challenge": "N/A",
                    "solution": "N/A",
                    "outcome": "N/A",
                    "lessons_learned": ["N/A"],
                    "related_concepts": ["N/A"]
                }]
            )
        
    # Career Connections
    def generate_career_connections(
        self,
        topic: str,
        industry_focus: Optional[str] = None,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        output_format: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Generates connections between academic topics and real-world careers,
        including insights from professionals in the field.
        """
        if response_model is None:
            response_model = CareerConnections

        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Create comprehensive career connections for the following academic topic:
            Topic: {topic}
            Industry Focus: {industry_focus}

            Generate detailed information about how this topic connects to real-world careers and professional opportunities.
            Include:

            1. Industry Overview
            - Current state of the industry
            - Future outlook
            - Key trends and developments

            2. Career Paths formatted as:
            "career_paths": [
                {{
                    "title": "Job Title",
                    "description": "Role description",
                    "typical_responsibilities": ["responsibility1", "responsibility2"],
                    "required_education": "Education requirements",
                    "salary_range": "Typical salary range",
                    "growth_potential": "Career growth opportunities",
                    "topic_application": "How this topic is used in the role"
                }}
            ]

            3. Professional Insights formatted as:
            "professional_insights": [
                {{
                    "role": "Professional's role",
                    "experience_level": "Years of experience",
                    "key_insights": ["insight1", "insight2"],
                    "daily_applications": ["application1", "application2"],
                    "advice_for_students": ["advice1", "advice2"]
                }}
            ]

            4. Required Skills
            - Technical skills
            - Soft skills
            - Industry-specific skills
            - Future skills needed

            5. Preparation Steps
            - Educational pathways
            - Certifications
            - Experience building
            - Networking opportunities

            6. Resources
            - Professional organizations
            - Learning platforms
            - Industry publications
            - Networking opportunities

            Make sure to:
            - Focus on current and emerging career opportunities
            - Include both traditional and non-traditional career paths
            - Highlight the practical applications of the topic
            - Provide actionable steps for students
            - Include diverse perspectives and roles

            Response format:
            {format_instructions}
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt = PromptTemplate(
            input_variables=["topic", "industry_focus"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm
        
        career_chain = prompt | llm_to_use
        results = career_chain.invoke(
            {
                "topic": topic,
                "industry_focus": industry_focus or "General",
                **kwargs
            },
        )
        results = results.content

        try:
            # Parse results to match the new LessonPlan structure
            structured_output = parser.parse(results)
            
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return response_model(
                topic=topic,
                industry_overview="Error generating content",
                career_paths=[{
                    "title": "Sample Career",
                    "description": "Error generating career paths",
                    "typical_responsibilities": ["N/A"],
                    "required_education": "N/A",
                    "salary_range": "N/A",
                    "growth_potential": "N/A",
                    "topic_application": "N/A"
                }],
                required_skills={
                    "technical": ["Error generating skills"],
                    "soft": ["Error generating skills"]
                },
                industry_trends=["Error generating trends"],
                professional_insights=[{
                    "role": "Sample Professional",
                    "experience_level": "N/A",
                    "key_insights": ["Error generating insights"],
                    "daily_applications": ["N/A"],
                    "advice_for_students": ["N/A"]
                }],
                preparation_steps={
                    "education": ["Error generating steps"],
                    "experience": ["Error generating steps"]
                },
                resources=[{
                    "name": "Sample Resource",
                    "url": "N/A"
                }]
            )
          
            return response_model()
    
    def generate_flashcards(
        self,
        topic: str,
        num: int = 10,
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        llm: Optional[Any] = None,
        **kwargs
    ) -> FlashcardSet:
        if response_model is None:
            response_model = FlashcardSet
        parser = PydanticOutputParser(pydantic_object=response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            Generate a set of {num} flashcards on the topic: {topic}.

            For each flashcard, provide:
            1. A front side with a question or key term
            2. A back side with the answer or definition
            3. An optional explanation or additional context

            The flashcards should cover key concepts, terminology, and important facts related to the topic.

            Ensure that the output follows this structure:
            - A title for the flashcard set (the main topic)
            - A list of flashcards, each containing:
              - front: The question or key term
              - back: The answer or definition
              - explanation: Additional context or explanation (optional)
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        flashcard_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        llm_to_use = llm if llm is not None else self.llm
        flashcard_chain = flashcard_prompt | llm_to_use
        results = flashcard_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )

        try:
            structured_output = parser.parse(results.content)
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results.content)
            return FlashcardSet(title=topic, flashcards=[])
    
    # Pedagogy-Based Content Generation Method
    
    def generate_pedagogy_content(
        self,
        topic: str,
        pedagogy: str,
        custom_instructions: Optional[str] = None,
        **kwargs
    ) -> Any:
        """
        Generate educational content using a specific pedagogical approach.
        
        Args:
            topic (str): The subject or topic for the content
            pedagogy (str): The pedagogical approach to use. Available options:
                - 'blooms_taxonomy': Bloom's Taxonomy cognitive levels
                - 'socratic_questioning': Socratic questioning method
                - 'project_based_learning': Project-based learning
                - 'flipped_classroom': Flipped classroom approach
                - 'inquiry_based_learning': Inquiry-based learning
                - 'constructivist': Constructivist learning
                - 'gamification': Gamified learning
                - 'peer_learning': Peer learning activities
            custom_instructions (str, optional): Additional instructions for content generation
            **kwargs: Pedagogy-specific parameters (see documentation for each pedagogy)
        
        Returns:
            Content object based on the selected pedagogy
        """
        
        # Pedagogy configurations
        pedagogy_configs = {
            "blooms_taxonomy": {
                "model": BloomsTaxonomyContent,
                "prompt_template": """
                Create educational content for the topic "{topic}" using Bloom's Taxonomy framework.
                Target cognitive level: {target_level}
                Grade level: {grade_level}
                
                Structure the content across all six cognitive levels of Bloom's Taxonomy:
                
                1. REMEMBER (Knowledge): Basic recall of information
                2. UNDERSTAND (Comprehension): Explaining ideas or concepts
                3. APPLY (Application): Using information in new situations
                4. ANALYZE (Analysis): Breaking down information to understand relationships
                5. EVALUATE (Evaluation): Justifying decisions or making judgments
                6. CREATE (Synthesis): Producing new or original work
                
                For each level, provide:
                - Learning objectives appropriate to that cognitive level
                - Activities that engage students at that level
                - Assessment questions that test that cognitive level
                - Real-world examples or applications
                
                Ensure progression from lower-order thinking (Remember, Understand, Apply) to 
                higher-order thinking (Analyze, Evaluate, Create).
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "target_level", "grade_level", "custom_instructions"],
                "defaults": {"target_level": "All levels", "grade_level": "General"}
            },
            
            "socratic_questioning": {
                "model": SocraticQuestioningContent,
                "prompt_template": """
                Create a Socratic questioning sequence for the topic "{topic}".
                Depth level: {depth_level}
                Student level: {student_level}
                
                Design a sequence of questions that guide students to discover knowledge about {topic} through:
                
                1. FOUNDATIONAL QUESTIONS: Questions that establish basic understanding
                2. ANALYTICAL QUESTIONS: Questions that probe assumptions and evidence
                3. PERSPECTIVE QUESTIONS: Questions that explore different viewpoints
                4. IMPLICATION QUESTIONS: Questions about consequences and implications
                5. META-COGNITIVE QUESTIONS: Questions about thinking and learning process
                
                For each question category, provide:
                - Multiple example questions
                - Follow-up probes for deeper inquiry
                - Potential student responses and how to guide them further
                - Connection to the main topic
                
                Include guidance for educators on:
                - How to facilitate discussions
                - When to ask follow-up questions
                - How to handle different types of student responses
                - Assessment strategies for Socratic dialogue
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "depth_level", "student_level", "custom_instructions"],
                "defaults": {"depth_level": "Intermediate", "student_level": "High School"}
            },
            
            "project_based_learning": {
                "model": ProjectBasedLearningContent,
                "prompt_template": """
                Design a comprehensive project-based learning experience for "{topic}".
                Project duration: {project_duration}
                Team size: {team_size}
                Industry focus: {industry_focus}
                
                Create a complete PBL framework including:
                
                1. DRIVING QUESTION: An engaging, open-ended question that guides the entire project
                2. PROJECT OVERVIEW: Clear description of what students will accomplish
                3. LEARNING OBJECTIVES: Specific knowledge and skills students will develop
                4. PROJECT PHASES: Detailed breakdown of project stages with timelines
                5. DELIVERABLES: Tangible outcomes students will produce
                6. ASSESSMENT RUBRICS: Criteria for evaluating student work
                7. RESOURCES: Materials, tools, and support needed
                8. REAL-WORLD CONNECTIONS: How the project relates to professional practice
                
                Ensure the project:
                - Addresses authentic, real-world problems
                - Requires sustained inquiry and research
                - Involves student choice and voice
                - Includes reflection and revision
                - Has a public audience for student work
                - Develops 21st-century skills (collaboration, communication, critical thinking, creativity)
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "project_duration", "team_size", "industry_focus", "custom_instructions"],
                "defaults": {"project_duration": "4-6 weeks", "team_size": "3-4 students", "industry_focus": "General"}
            },
            
            "flipped_classroom": {
                "model": FlippedClassroomContent,
                "prompt_template": """
                Design a flipped classroom approach for "{topic}".
                Class duration: {class_duration}
                Prep time available: {prep_time}
                Technology level: {technology_level}
                
                Create a complete flipped classroom design with:
                
                1. PRE-CLASS PREPARATION:
                - Content delivery materials (videos, readings, interactive modules)
                - Pre-class assessment to check understanding
                - Preparation guidelines for students
                
                2. IN-CLASS ACTIVITIES:
                - Warm-up activities to address pre-class questions
                - Active learning exercises (discussions, problem-solving, labs)
                - Collaborative work and peer learning
                - Instructor-guided practice and application
                
                3. POST-CLASS REINFORCEMENT:
                - Extended practice activities
                - Reflection assignments
                - Application projects
                
                4. ASSESSMENT STRATEGY:
                - Formative assessments throughout the cycle
                - Summative assessments of learning outcomes
                - Peer assessment opportunities
                
                5. TECHNOLOGY INTEGRATION:
                - Tools for content delivery
                - Platforms for collaboration
                - Assessment technologies
                
                Ensure the design maximizes active learning during face-to-face time while 
                providing effective independent learning experiences.
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "class_duration", "prep_time", "technology_level", "custom_instructions"],
                "defaults": {"class_duration": "50 minutes", "prep_time": "30-45 minutes", "technology_level": "Moderate"}
            },
            
            "inquiry_based_learning": {
                "model": InquiryBasedLearningContent,
                "prompt_template": """
                Design an inquiry-based learning experience for "{topic}".
                Inquiry type: {inquiry_type}
                Investigation scope: {investigation_scope}
                Student autonomy level: {student_autonomy}
                
                Create a comprehensive IBL framework including:
                
                1. ESSENTIAL QUESTIONS: Open-ended questions that drive inquiry
                2. INVESTIGATION PHASES:
                   - Question formulation
                   - Research and data collection
                   - Analysis and interpretation
                   - Conclusion and communication
                
                3. INQUIRY ACTIVITIES:
                - Guided investigations for skill building
                - Open investigations for independent exploration
                - Collaborative inquiry projects
                - Real-world problem investigations
                
                4. RESEARCH METHODS:
                - Primary research techniques
                - Secondary research strategies
                - Data collection methods
                - Analysis approaches
                
                5. SCAFFOLD SUPPORT:
                - Question stems and frameworks
                - Research organizers
                - Thinking protocols
                - Reflection prompts
                
                6. PRESENTATION FORMATS:
                - Research presentations
                - Scientific posters
                - Digital storytelling
                - Peer teaching sessions
                
                Balance student autonomy with appropriate guidance to ensure productive inquiry.
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "inquiry_type", "investigation_scope", "student_autonomy", "custom_instructions"],
                "defaults": {"inquiry_type": "Guided", "investigation_scope": "Moderate", "student_autonomy": "Balanced"}
            },
            
            "constructivist": {
                "model": ConstructivistContent,
                "prompt_template": """
                Design a constructivist learning experience for "{topic}".
                Prior knowledge level: {prior_knowledge_level}
                Social interaction focus: {social_interaction_focus}
                Reflection emphasis: {reflection_emphasis}
                
                Create a constructivist framework that includes:
                
                1. PRIOR KNOWLEDGE ACTIVATION:
                - Activities to surface existing understanding
                - Misconception identification
                - Knowledge mapping exercises
                
                2. EXPERIENTIAL LEARNING:
                - Hands-on activities and experiments
                - Real-world problem scenarios
                - Exploration and discovery tasks
                
                3. SOCIAL CONSTRUCTION:
                - Collaborative learning activities
                - Peer discussion and debate
                - Knowledge sharing protocols
                - Community of practice development
                
                4. REFLECTIVE PRACTICES:
                - Metacognitive questioning
                - Learning journals and portfolios
                - Self-assessment strategies
                - Peer feedback systems
                
                5. KNOWLEDGE BUILDING TOOLS:
                - Concept mapping
                - Knowledge construction frameworks
                - Collaborative annotation
                - Iterative design processes
                
                6. AUTHENTIC ASSESSMENT:
                - Performance-based evaluation
                - Portfolio assessment
                - Self and peer evaluation
                - Real-world application demonstrations
                
                Emphasize active knowledge construction, multiple perspectives, and continuous reflection.
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "prior_knowledge_level", "social_interaction_focus", "reflection_emphasis", "custom_instructions"],
                "defaults": {"prior_knowledge_level": "Mixed", "social_interaction_focus": "High", "reflection_emphasis": "Strong"}
            },
            
            "gamification": {
                "model": GamificationContent,
                "prompt_template": """
                Design a gamified learning experience for "{topic}".
                Preferred game mechanics: {game_mechanics}
                Competition level: {competition_level}
                Technology platform: {technology_platform}
                
                Create a comprehensive gamification design including:
                
                1. GAME MECHANICS:
                - Points and scoring systems
                - Levels and progression paths
                - Badges and achievements
                - Leaderboards and rankings
                - Challenges and quests
                
                2. GAME DYNAMICS:
                - Competition and collaboration balance
                - Narrative and storytelling elements
                - Player agency and choice
                - Feedback loops
                - Social interaction features
                
                3. LEARNING INTEGRATION:
                - Curriculum-aligned objectives
                - Assessment through gameplay
                - Knowledge application scenarios
                - Skill development pathways
                
                4. PLAYER MOTIVATION:
                - Intrinsic motivation strategies
                - Extrinsic reward systems
                - Personalization options
                - Social recognition features
                
                5. GAME PROGRESSION:
                - Onboarding and tutorial design
                - Difficulty scaling
                - Mastery indicators
                - Unlock systems
                
                6. PLATFORM CONSIDERATIONS:
                - Technology requirements
                - Accessibility features
                - Multi-device compatibility
                - Data analytics integration
                
                Balance fun and learning while maintaining educational rigor.
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "game_mechanics", "competition_level", "technology_platform", "custom_instructions"],
                "defaults": {"game_mechanics": "Points, badges, levels", "competition_level": "Moderate", "technology_platform": "Web-based"}
            },
            
            "peer_learning": {
                "model": PeerLearningContent,
                "prompt_template": """
                Design a peer learning experience for "{topic}".
                Group size: {group_size}
                Collaboration type: {collaboration_type}
                Skill diversity level: {skill_diversity}
                
                Create a comprehensive peer learning framework including:
                
                1. PEER LEARNING STRUCTURES:
                - Think-Pair-Share activities
                - Jigsaw method implementation
                - Peer tutoring arrangements
                - Reciprocal teaching protocols
                - Collaborative problem-solving
                
                2. GROUP FORMATION STRATEGIES:
                - Skill-based grouping
                - Interest-based partnerships
                - Random group formation
                - Self-selected teams
                - Rotating group structures
                
                3. COLLABORATION ACTIVITIES:
                - Knowledge sharing sessions
                - Peer review processes
                - Joint problem-solving tasks
                - Teaching role rotations
                - Debate and discussion formats
                
                4. COMMUNICATION PROTOCOLS:
                - Active listening guidelines
                - Constructive feedback frameworks
                - Conflict resolution strategies
                - Digital collaboration tools
                - Discussion facilitation techniques
                
                5. ACCOUNTABILITY MEASURES:
                - Individual responsibility within groups
                - Peer assessment rubrics
                - Group reflection processes
                - Progress monitoring systems
                - Quality assurance checkpoints
                
                6. INSTRUCTOR FACILITATION:
                - Monitoring and intervention strategies
                - Guidance provision techniques
                - Process observation methods
                - Support for struggling groups
                - Enhancement of successful collaboration
                
                Ensure equitable participation and mutual learning benefits for all students.
                
                {custom_instructions}
                
                {format_instructions}
                """,
                "input_variables": ["topic", "group_size", "collaboration_type", "skill_diversity", "custom_instructions"],
                "defaults": {"group_size": "3-4 students", "collaboration_type": "Mixed", "skill_diversity": "Moderate"}
            }
        }
        
        # Validate pedagogy
        if pedagogy not in pedagogy_configs:
            available = list(pedagogy_configs.keys())
            raise ValueError(f"Unknown pedagogy '{pedagogy}'. Available options: {available}")
        
        config = pedagogy_configs[pedagogy]
        
        # Set up parser and format instructions
        parser = PydanticOutputParser(pydantic_object=config["model"])
        format_instructions = parser.get_format_instructions()
        
        # Prepare prompt variables with defaults
        prompt_vars = {"topic": topic, "custom_instructions": custom_instructions or ""}
        
        # Apply defaults and user-provided values
        for var in config["input_variables"]:
            if var not in ["topic", "custom_instructions"]:
                default_value = config["defaults"].get(var, "")
                prompt_vars[var] = kwargs.get(var, default_value)
        
        # Create prompt template
        prompt = PromptTemplate(
            input_variables=config["input_variables"],
            template=config["prompt_template"],
            partial_variables={"format_instructions": format_instructions}
        )
        
        # Generate content
        chain = prompt | self.llm
        result = chain.invoke(prompt_vars)
        
        try:
            return parser.parse(result.content)
        except Exception as e:
            print(f"Error parsing {pedagogy} content: {e}")
            return config["model"](topic=topic)
    
    def get_available_pedagogies(self) -> dict:
        """Get information about all available pedagogy methods and their parameters."""
        return {
            "blooms_taxonomy": {
                "description": "Structures learning through six cognitive levels - Remember, Understand, Apply, Analyze, Evaluate, and Create.",
                "parameters": {
                    "target_level": "Cognitive level to focus on (default: 'All levels')",
                    "grade_level": "Target grade level (default: 'General')"
                }
            },
            "socratic_questioning": {
                "description": "Guides learning through strategic questioning that promotes critical thinking and self-discovery.",
                "parameters": {
                    "depth_level": "Depth of inquiry (default: 'Intermediate')",
                    "student_level": "Student level (default: 'High School')"
                }
            },
            "project_based_learning": {
                "description": "Engages students in complex, real-world projects that develop deep understanding and practical skills.",
                "parameters": {
                    "project_duration": "Project duration (default: '4-6 weeks')",
                    "team_size": "Team size (default: '3-4 students')",
                    "industry_focus": "Industry focus (default: 'General')"
                }
            },
            "flipped_classroom": {
                "description": "Students learn foundational content at home and engage in active learning during class time.",
                "parameters": {
                    "class_duration": "Class duration (default: '50 minutes')",
                    "prep_time": "Preparation time (default: '30-45 minutes')",
                    "technology_level": "Technology level (default: 'Moderate')"
                }
            },
            "inquiry_based_learning": {
                "description": "Students develop understanding through questioning, investigation, and discovery.",
                "parameters": {
                    "inquiry_type": "Type of inquiry (default: 'Guided')",
                    "investigation_scope": "Investigation scope (default: 'Moderate')",
                    "student_autonomy": "Student autonomy level (default: 'Balanced')"
                }
            },
            "constructivist": {
                "description": "Students actively build understanding through experience, reflection, and social interaction.",
                "parameters": {
                    "prior_knowledge_level": "Prior knowledge level (default: 'Mixed')",
                    "social_interaction_focus": "Social interaction focus (default: 'High')",
                    "reflection_emphasis": "Reflection emphasis (default: 'Strong')"
                }
            },
            "gamification": {
                "description": "Applies game design elements to increase engagement, motivation, and learning outcomes.",
                "parameters": {
                    "game_mechanics": "Game mechanics (default: 'Points, badges, levels')",
                    "competition_level": "Competition level (default: 'Moderate')",
                    "technology_platform": "Technology platform (default: 'Web-based')"
                }
            },
            "peer_learning": {
                "description": "Students learn from and with each other through structured collaborative activities.",
                "parameters": {
                    "group_size": "Group size (default: '3-4 students')",
                    "collaboration_type": "Collaboration type (default: 'Mixed')",
                    "skill_diversity": "Skill diversity level (default: 'Moderate')"
                }
            }
        }
