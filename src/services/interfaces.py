from abc import ABC, abstractmethod
from typing import Dict, Any

class IAgentService(ABC):
    """
    Abstract blueprint ensuring scalable structural bridging across versions.
    """
    @abstractmethod
    def process_query(self, raw_query: str, structured_intent: Dict[str, Any] = None) -> Dict[str, Any]:
        pass
