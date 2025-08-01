"""
Base Agent Implementation
-----------------------
This module defines the foundation for all specialized agents in the system.
It provides core functionality and structure that all agents must follow.

Key Components:
- Type-safe state management
- Abstract process interface
- Asynchronous task handling
- Pydantic data validation
"""

# 1. IMPORTS AND TYPE DEFINITIONS
# ----------------------------
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field # type: ignore

# 2. AGENT STATE MANAGEMENT
# ----------------------
class AgentState(BaseModel):
    """
    State model for agents using Pydantic validation.
    
    Attributes:
        name (str): Unique identifier for the agent
        status (str): Current agent status (default: idle)
        current_task (Optional[Dict]): Information about the task being processed
    
    Features:
    - Automatic data validation
    - JSON serialization
    - Type safety
    - Clear error messages
    """
    name: str
    status: str = "idle"
    current_task: Optional[Dict[str, Any]] = None

# 3. BASE AGENT DEFINITION
# ----------------------
class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Features:
    - Abstract template for specialized agents
    - Consistent state management
    - Asynchronous task processing
    - Type-safe operations
    
    Implementation Requirements:
    - All child classes must implement process()
    - State management through update_state()
    - Asynchronous task handling
    - Structured input/output
    """
    
    def __init__(self, name: str):
        """
        Initialize agent with name and state.
        
        Args:
            name (str): Unique identifier for the agent
        """
        self.state = AgentState(name=name)
    
    # 4. ABSTRACT PROCESS METHOD
    # ------------------------
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task and return results. Must be implemented by child classes.
        
        Args:
            task (Dict[str, Any]): Task to be processed
            
        Returns:
            Dict[str, Any]: Processing results
            
        Features:
        - Asynchronous operation
        - Structured input/output
        - Type safety
        - Required implementation
        """
        pass
    
    # 5. STATE MANAGEMENT
    # -----------------
    def update_state(self, **kwargs) -> None:
        """
        Update agent state safely.
        
        Args:
            **kwargs: State attributes to update
            
        Features:
        - Flexible updates via kwargs
        - Attribute validation
        - Safe state management
        - Maintains consistency
        
        Example:
            update_state(status="processing", current_task=task_data)
        """
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value) 