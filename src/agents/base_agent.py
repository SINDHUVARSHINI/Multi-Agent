from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field # type: ignore
from abc import ABC, abstractmethod

class AgentState(BaseModel):
    """State model for agents"""
    name: str
    status: str = "idle"
    current_task: Optional[Dict[str, Any]] = None
    memory: Dict[str, Any] = Field(default_factory=dict)

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, tools: List[Any] = None): # type: ignore
        self.state = AgentState(name=name)
        self.tools = tools or []
        
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    def update_state(self, **kwargs) -> None:
        """Update agent state"""
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
                
    def add_to_memory(self, key: str, value: Any) -> None:
        """Add information to agent's memory"""
        self.state.memory[key] = value
        
    def get_from_memory(self, key: str) -> Optional[Any]:
        """Retrieve information from agent's memory"""
        return self.state.memory.get(key)
        
    def clear_memory(self) -> None:
        """Clear agent's memory"""
        self.state.memory.clear()
        
    def get_status(self) -> str:
        """Get agent's current status"""
        return self.state.status
        
    def get_current_task(self) -> Optional[Dict[str, Any]]:
        """Get agent's current task"""
        return self.state.current_task 