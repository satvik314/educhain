import pytest
from educhain.core.config import LLMConfig
from educhain.engines.qna_engine import QnAEngine
from unittest.mock import patch, MagicMock
from educhain.models.qna_models import MCQList, MultipleChoiceQuestion

@pytest.fixture
def ollama_config():
    return LLMConfig(
        model_name="llama2",
        base_url="http://localhost:11434",
        temperature=0.7
    )

@pytest.fixture
def mock_ollama_response():
    return """
    {
        "questions": [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": "Paris",
                "explanation": "Paris is the capital city of France."
            }
        ]
    }
    """

def test_ollama_connection_check(ollama_config):
    """Test the Ollama server connection check"""
    with patch('requests.get') as mock_get:
        # Test successful connection
        mock_get.return_value.status_code = 200
        engine = QnAEngine(ollama_config)
        assert engine._check_ollama_connection(ollama_config.base_url) == True

        # Test failed connection
        mock_get.return_value.status_code = 500
        assert engine._check_ollama_connection(ollama_config.base_url) == False

def test_ollama_initialization(ollama_config):
    """Test QnAEngine initialization with Ollama config"""
    with patch('educhain.engines.qna_engine.QnAEngine._check_ollama_connection') as mock_check:
        mock_check.return_value = True
        engine = QnAEngine(ollama_config)
        assert engine.llm is not None
        assert isinstance(engine.llm.__class__.__name__, str)
        assert "Ollama" in engine.llm.__class__.__name__

@pytest.mark.asyncio
async def test_generate_multiple_choice_questions(ollama_config, mock_ollama_response):
    """Test generating multiple choice questions using Ollama"""
    with patch('educhain.engines.qna_engine.QnAEngine._check_ollama_connection') as mock_check, \
         patch('langchain_ollama.OllamaLLM.predict') as mock_predict:
        
        mock_check.return_value = True
        mock_predict.return_value = mock_ollama_response
        
        engine = QnAEngine(ollama_config)
        questions = engine.generate_questions(
            question_type="Multiple Choice",
            num=1,
            topic="Geography"
        )
        
        assert questions is not None
        assert len(questions.questions) == 1
        assert questions.questions[0].question == "What is the capital of France?"
        assert questions.questions[0].answer == "Paris"

def test_ollama_connection_error(ollama_config):
    """Test handling of Ollama connection errors"""
    with patch('educhain.engines.qna_engine.QnAEngine._check_ollama_connection') as mock_check:
        mock_check.return_value = False
        
        with pytest.raises(ConnectionError) as exc_info:
            QnAEngine(ollama_config)
        
        assert "Cannot connect to local model server" in str(exc_info.value)

def test_mcq_model_structure():
    """Test that the MCQ model accepts correctly structured data"""
    question = MultipleChoiceQuestion(
        question="What is the capital of France?",
        options=["London", "Paris", "Berlin", "Madrid"],
        answer="Paris",
        explanation="Paris is the capital city of France."
    )
    
    mcq_list = MCQList(questions=[question])
    assert len(mcq_list.questions) == 1
    assert mcq_list.questions[0].answer == "Paris" 