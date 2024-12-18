# educhain/engines/qna_engine.py

from typing import Optional, Type, Any, List, Literal, Union, Tuple
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA, LLMMathChain
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.callbacks.manager import get_openai_callback
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from langchain_core.messages import SystemMessage
from langchain.schema import HumanMessage
from educhain.core.config import LLMConfig
from educhain.models.qna_models import (
    MCQList, ShortAnswerQuestionList, TrueFalseQuestionList, 
    FillInBlankQuestionList, MCQListMath, Option ,SolvedDoubt, SpeechInstructions
)
from educhain.utils.loaders import PdfFileLoader, UrlLoader
from educhain.utils.output_formatter import OutputFormatter
import base64
import os
from PIL import Image
import io

# Update the QuestionType definition

import random

QuestionType = Literal["Multiple Choice", "Short Answer", "True/False", "Fill in the Blank"]
OutputFormatType = Literal["pdf", "csv"]

class QnAEngine:
    def __init__(self, llm_config: Optional[LLMConfig] = None):
        if llm_config is None:
            llm_config = LLMConfig()  # Use default OpenAI configuration
        self.llm = self._initialize_llm(llm_config)
        self.pdf_loader = PdfFileLoader()
        self.url_loader = UrlLoader()
        self.embeddings = None  # Initialize as None

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

    def _get_parser_and_model(self, question_type: QuestionType, response_model: Optional[Type[Any]] = None):
        if response_model:
            return PydanticOutputParser(pydantic_object=response_model), response_model
        if question_type == "Multiple Choice":
            return PydanticOutputParser(pydantic_object=MCQList), MCQList
        elif question_type == "Short Answer":
            return PydanticOutputParser(pydantic_object=ShortAnswerQuestionList), ShortAnswerQuestionList
        elif question_type == "True/False":
            return PydanticOutputParser(pydantic_object=TrueFalseQuestionList), TrueFalseQuestionList
        elif question_type == "Fill in the Blank":
            return PydanticOutputParser(pydantic_object=FillInBlankQuestionList), FillInBlankQuestionList
        else:
            raise ValueError(f"Unsupported question type: {question_type}")

    def _get_prompt_template(self, question_type: QuestionType, custom_template: Optional[str] = None):
        if custom_template:
            return custom_template

        base_template = f"""
        Generate {{num}} {question_type} question(s) based on the given topic.
        Topic: {{topic}}

        For each question, provide:
        1. The question
        2. The correct answer
        3. An explanation (optional)
        """

        if question_type == "Multiple Choice":
            base_template += "\n4. A list of options (including the correct answer)"
        elif question_type == "Short Answer":
            base_template += "\n4. A list of relevant keywords"
        elif question_type == "True/False":
            base_template += "\n4. The correct answer as a boolean (true/false)"
        elif question_type == "Fill in the Blank":
            base_template += "\n4. The word or phrase to be filled in the blank"

        return base_template

    def _create_vector_store(self, content: str) -> Chroma:
        # Ensure embeddings are initialized
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(content)

        # Create the vector store
        vectorstore = Chroma.from_texts(texts, self.embeddings)

        return vectorstore

    def _setup_retrieval_qa(self, vector_store: Chroma) -> RetrievalQA:
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
        )

    def _load_data(self, source: str, source_type: str) -> str:
        if source_type == 'pdf':
            return self.pdf_loader.load_data(source)
        elif source_type == 'url':
            return self.url_loader.load_data(source)
        elif source_type == 'text':
            return source
        else:
            raise ValueError("Unsupported source type. Please use 'pdf', 'url', or 'text'.")
        
    def _handle_output_format(self, data: Any, output_format: Optional[OutputFormatType]) -> Union[Any, Tuple[Any, str]]:
        """Handle output format conversion if specified"""
        if output_format is None:
            return data
            
        formatter = OutputFormatter()
        if output_format == "pdf":
            output_file = formatter.to_pdf(data)
        elif output_format == "csv":
            output_file = formatter.to_csv(data)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
            
        return data, output_file

    def generate_questions(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()

        if response_model:
            if prompt_template:
                template = prompt_template
            else:
                template = """
                Generate {num} questions based on the given topic.
                Topic: {topic}

                Ensure that each question follows the structure specified in the format instructions.
                """
        else:
            template = self._get_prompt_template(question_type, prompt_template)

        if custom_instructions:
            template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        template += "\n\nThe response should be in JSON format.\n{format_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=template,
            partial_variables={"format_instructions": format_instructions}
        )

        question_chain = question_prompt | self.llm
        results = question_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)

            if output_format:
                self._handle_output_format(structured_output, output_format)
                
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return model()

    def generate_questions_from_data(
        self,
        source: str,
        source_type: str,
        num: int,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        content = self._load_data(source, source_type)
        return self.generate_questions(
            topic=content,
            num=num,
            question_type=question_type,
            prompt_template=prompt_template,
            custom_instructions=custom_instructions,
            response_model=response_model,
            **kwargs
        )

    def generate_questions_with_rag(
        self,
        source: str,
        source_type: str,
        num: int,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        learning_objective: str = "",
        difficulty_level: str = "",
        output_format: Optional[OutputFormatType] = None,
        **kwargs
    ) -> Any:
        # Initialize embeddings only when this method is called
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

        content = self._load_data(source, source_type)

        vector_store = self._create_vector_store(content)
        qa_chain = self._setup_retrieval_qa(vector_store)

        parser, model = self._get_parser_and_model(question_type, response_model)
        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = self._get_prompt_template(question_type)

        prompt_template += """
        Learning Objective: {learning_objective}
        Difficulty Level: {difficulty_level}

        Ensure that the questions are relevant to the learning objective and match the specified difficulty level.

        The response should be in JSON format.
        {format_instructions}
        """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic", "learning_objective", "difficulty_level"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        query = question_prompt.format(
            num=num,
            topic=content[:1000],  # Use a subset of content to fit in context
            learning_objective=learning_objective,
            difficulty_level=difficulty_level,
            **kwargs
        )

        results = qa_chain.invoke({"query": query, "n_results": 3})

        try:
            structured_output = parser.parse(results["result"])

            if output_format:
                self._handle_output_format(structured_output, output_format)
            
            return structured_output
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:", results)
            return model()

    def generate_similar_options(self, question, correct_answer, num_options=3):
        llm = self.llm
        prompt = f"Generate {num_options} incorrect but plausible options similar to this correct answer: {correct_answer} for this question: {question}. Provide only the options, separated by semicolons. The options should not precede or end with any symbols, it should be similar to the correct answer."
        response = llm.predict(prompt)
        return response.split(';')

    def _process_math_result(self, math_result: Any) -> str:
        """Helper method to process and extract numerical answer from LLMMathChain result"""
        if isinstance(math_result, dict):
            if 'answer' in math_result:
                return math_result['answer'].split('Answer: ')[-1].strip()
            elif 'result' in math_result:
                return math_result['result'].strip()
        
        # Handle string response
        result_str = str(math_result)
        if 'Answer:' in result_str:
            return result_str.split('Answer:')[-1].strip()
        
        # Remove any question repetition and extract the numerical result
        lines = result_str.split('\n')
        for line in reversed(lines):
            if line.strip().replace('.', '').isdigit():
                return line.strip()
        
        raise ValueError("Could not extract numerical result from LLMMathChain response")
    
    def generate_mcq_math(
        self,
        topic: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        **kwargs
    ) -> Any:
        if response_model is None:
            parser = PydanticOutputParser(pydantic_object=MCQListMath)
        else:
            parser = PydanticOutputParser(pydantic_object=response_model)

        format_instructions = parser.get_format_instructions()

        if prompt_template is None:
            prompt_template = """
            You are an Academic AI assistant specialized in generating multiple-choice math questions.
            Generate {num} multiple-choice questions (MCQ) based on the given topic.
            Each question MUST be a mathematical computation question.
            
            For each question:
            1. Make sure it requires mathematical calculation
            2. Set requires_math to true
            3. Provide clear numerical values
            4. Ensure the question has a single, unambiguous answer
            
            Topic: {topic}
            
            Format each question to include:
            - A clear mathematical problem
            - Four distinct numerical options
            - The correct answer
            - A step-by-step explanation
            """

        if custom_instructions:
            prompt_template += f"\n\nAdditional Instructions:\n{custom_instructions}"

        prompt_template += "\nThe response should be in JSON format.\n{format_instructions}"

        question_prompt = PromptTemplate(
            input_variables=["num", "topic"],
            template=prompt_template,
            partial_variables={"format_instructions": format_instructions}
        )

        question_chain = question_prompt | self.llm
        results = question_chain.invoke(
            {"num": num, "topic": topic, **kwargs},
        )
        results = results.content

        try:
            structured_output = parser.parse(results)
        except Exception as e:
            print(f"Error parsing output: {e}")
            print("Raw output:")
            print(results)
            return MCQListMath()

        llm_math = LLMMathChain.from_llm(llm=self.llm, verbose=True)

        for question in structured_output.questions:
            if question.requires_math:
                try:
                    # Extract numerical expression from the question
                    math_result = llm_math.invoke({"question": question.question})
                    
                    try:
                        # Process the result using the helper method
                        solution = self._process_math_result(math_result)
                        
                        # Convert to float and format
                        numerical_solution = float(solution)
                        formatted_solution = f"{numerical_solution:.2f}"
                        
                        question.explanation += f"\n\nMath solution: {formatted_solution}"
                        
                        # Generate options with the correct string format
                        correct_option = Option(text=formatted_solution, correct='true')
                        
                        # Generate incorrect options
                        variations = [0.9, 1.1, 1.2]
                        incorrect_options = []
                        
                        for var in variations:
                            wrong_val = numerical_solution * var
                            incorrect_options.append(
                                Option(
                                    text=f"{wrong_val:.2f}",
                                    correct='false'
                                )
                            )
                        
                        # Combine and shuffle options
                        question.options = [correct_option] + incorrect_options
                        random.shuffle(question.options)
                        
                    except (ValueError, TypeError) as e:
                        print(f"Error processing numerical result: {e}")
                        raise
                        
                except Exception as e:
                    print(f"LLMMathChain failed to answer: {str(e)}")
                    question.explanation += "\n\nMath solution: Unable to compute."
                    question.options = [
                        Option(text="Unable to compute", correct='true'),
                        Option(text="N/A", correct='false'),
                        Option(text="N/A", correct='false'),
                        Option(text="N/A", correct='false')
                    ]

        return structured_output

    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?:feature=player_embedded&v=)?(?:e\/)?(?:\/)?([^\s&amp;?#]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        raise ValueError("Invalid YouTube URL")

    def _get_youtube_transcript(self, video_id: str, target_language: str = 'en') -> tuple[str, str]:
        """
        Get and format YouTube video transcript with multi-language support.
        Returns tuple of (transcript, language_code)
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get all available languages
            available_languages = [transcript.language_code for transcript in transcript_list]
            
            if not available_languages:
                raise ValueError("No transcripts available for this video")
            
            # First try to get transcript in target language
            try:
                transcript = transcript_list.find_transcript([target_language])
                return TextFormatter().format_transcript(transcript.fetch()), target_language
            except:
                # If target language not found, get any available transcript
                transcript = transcript_list.find_transcript(available_languages)
                original_language = transcript.language_code
                
                # If translation to target language is available and requested
                if transcript.is_translatable and target_language != original_language:
                    translated = transcript.translate(target_language)
                    return TextFormatter().format_transcript(translated.fetch()), target_language
                
                # Return original language transcript if no translation needed/available
                return TextFormatter().format_transcript(transcript.fetch()), original_language
                
        except Exception as e:
            error_message = str(e).lower()
            if "transcriptsdisabled" in error_message:
                raise ValueError(
                    "This video does not have subtitles/closed captions enabled. "
                    "Available languages: " + ", ".join(available_languages)
                )
            elif "notranscriptfound" in error_message:
                raise ValueError(
                    f"No transcript found for language '{target_language}'. "
                    f"Available languages: {', '.join(available_languages)}"
                )
            else:
                raise ValueError(f"Error fetching transcript: {str(e)}")

    def generate_questions_from_youtube(
        self,
        url: str,
        num: int = 1,
        question_type: QuestionType = "Multiple Choice",
        prompt_template: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        response_model: Optional[Type[Any]] = None,
        output_format: Optional[OutputFormatType] = None,
        target_language: str = 'en',
        preserve_original_language: bool = False,
        **kwargs
    ) -> Any:
        """
        Generate questions from a YouTube video transcript in specified language.
        
        Args:
            url: YouTube video URL
            num: Number of questions to generate
            question_type: Type of questions to generate
            prompt_template: Optional custom prompt template
            custom_instructions: Optional additional instructions
            response_model: Optional custom response model
            output_format: Optional output format (pdf/csv)
            target_language: Target language for questions (e.g., 'hi' for Hindi)
            preserve_original_language: If True, keeps original language even if different from target
            **kwargs: Additional arguments
        """
        try:
            video_id = self._extract_video_id(url)
            transcript, detected_language = self._get_youtube_transcript(video_id, target_language)
            
            if not transcript:
                raise ValueError("No transcript content retrieved from the video")

            # Language-specific instructions
            language_context = f"\nContent language: {detected_language}"
            if detected_language != target_language and not preserve_original_language:
                language_context += f"\nGenerate questions in {target_language}"
            
            # Update custom instructions
            video_context = f"\nThis content is from a YouTube video (ID: {video_id}). {language_context}"
            if custom_instructions:
                custom_instructions = video_context + "\n" + custom_instructions
            else:
                custom_instructions = video_context

            return self.generate_questions_from_data(
                source=transcript,
                source_type="text",
                num=num,
                question_type=question_type,
                prompt_template=prompt_template,
                custom_instructions=custom_instructions,
                response_model=response_model,
                output_format=output_format,
                target_language=target_language,
                **kwargs
            )
            
        except ValueError as ve:
            raise ValueError(f"YouTube processing error: {str(ve)}")
        except Exception as e:
            raise Exception(f"Unexpected error processing YouTube video: {str(e)}")

    def _load_image(self, source: str) -> str:
        """Load and encode image from file or URL"""
        try:
            if source.startswith(('http://', 'https://')):
                return source
            elif source.startswith('data:image'):
                return source
            else:
                image = Image.open(source)
                if image.mode not in ('RGB', 'L'):
                    image = image.convert('RGB')
                
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"

        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")

    def solve_doubt(
        self,
        image_source: str,
        prompt: str = "Explain how to solve this problem",
        custom_instructions: Optional[str] = None,
        detail_level: Literal["low", "medium", "high"] = "medium",
        focus_areas: Optional[List[str]] = None,
        **kwargs
    ) -> SolvedDoubt:
        """
        Analyze an image and provide detailed explanation with solution steps.
        
        Args:
            image_source: Path or URL to the image
            prompt: Custom prompt for analysis
            custom_instructions: Additional instructions for analysis
            detail_level: Level of detail in explanation
            focus_areas: Specific aspects to focus on
            **kwargs: Additional parameters for the model
        
        Returns:
            SolvedDoubt: Object containing explanation, steps, and additional notes
        """
        if not image_source:
            raise ValueError("Image source (path or URL) is required")

        try:
            image_content = self._load_image(image_source)
            
            # Create parser for structured output
            parser = PydanticOutputParser(pydantic_object=SolvedDoubt)
            format_instructions = parser.get_format_instructions()

            # Construct the prompt with all parameters
            base_prompt = f"Analyze the image and {prompt}\n"
            if focus_areas:
                base_prompt += f"\nFocus on these aspects: {', '.join(focus_areas)}"
            base_prompt += f"\nProvide a {detail_level}-detail explanation"
            
            system_message = SystemMessage(
                content="You are a helpful assistant that responds in Markdown. Help with math homework."
            )

            human_message_content = f"""
            {base_prompt}
            
            Provide:
            1. A detailed explanation
            2. Step-by-step solution (if applicable)
            3. Any additional notes or tips
            
            {custom_instructions or ''}
            
            {format_instructions}
            """

            human_message = HumanMessage(content=[
                {"type": "text", "text": human_message_content},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_content,
                        "detail": "high" if detail_level == "high" else "low"
                    }
                }
            ])

            response = self.llm.invoke(
                [system_message, human_message],
                **kwargs
            )

            try:
                return parser.parse(response.content)
            except Exception as e:
                # Fallback if parsing fails
                return SolvedDoubt(
                    explanation=response.content,
                    steps=[],
                    additional_notes="Note: Response format was not structured as requested."
                )

        except Exception as e:
            error_msg = f"Error in solve_doubt: {type(e).__name__}: {str(e)}"
            print(error_msg)
            return SolvedDoubt(
                explanation=error_msg,
                steps=[],
                additional_notes="An error occurred during processing."
            )

   
