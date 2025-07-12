from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field # type: ignore

class AgentState(BaseModel):
    """State model for agents"""
    name: str
    status: str = "idle"
    current_task: Optional[Dict[str, Any]] = None

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str):
        self.state = AgentState(name=name)
    
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    def update_state(self, **kwargs) -> None:
        """Update agent state"""
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value) 