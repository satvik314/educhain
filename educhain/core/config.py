import os
from typing import Optional, Any

class LLMConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o-mini",
        max_tokens: int = 1500,
        temperature: float = 0.7,
        custom_model: Optional[Any] = None,
        base_url: Optional[str] = None,
        default_headers: Optional[dict] = None
    ):
        # If no API key is provided, try to get it from environment variables
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.custom_model = custom_model
        self.base_url = base_url
        self.default_headers = default_headers