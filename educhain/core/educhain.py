from typing import Optional, Any, Dict, List
from educhain.core.config import LLMConfig
from educhain.engines.qna_engine import QnAEngine
from educhain.engines.content_engine import ContentEngine

class Educhain:
    def __init__(self, config: Optional[LLMConfig] = None):
        if config is None:
            config = LLMConfig()
        self.llm_config = config
        self.qna_engine = QnAEngine(config)
        self.content_engine = ContentEngine(config)
        self.components: Dict[str, Any] = {
            "qna_engine": self.qna_engine,
            "content_engine": self.content_engine
        }

    def get_qna_engine(self) -> QnAEngine:
        return self.qna_engine

    def get_content_engine(self) -> ContentEngine:
        return self.content_engine

    def get_config(self) -> LLMConfig:
        return self.llm_config

    def update_config(self, new_config: LLMConfig) -> None:
        self.llm_config = new_config
        self.qna_engine = QnAEngine(new_config)
        self.content_engine = ContentEngine(new_config)
        self.components["qna_engine"] = self.qna_engine
        self.components["content_engine"] = self.content_engine

    def add_component(self, component_name: str, component: Any) -> None:
        self.components[component_name] = component
        setattr(self, component_name, component)

    def get_component(self, component_name: str) -> Any:
        return self.components.get(component_name)

    def remove_component(self, component_name: str) -> None:
        if component_name in self.components:
            del self.components[component_name]
            delattr(self, component_name)

    def get_available_components(self) -> List[str]:
        return list(self.components.keys())

    def __str__(self) -> str:
        return f"Educhain(config={self.llm_config}, components={self.get_available_components()})"

    def __repr__(self) -> str:
        return self.__str__()