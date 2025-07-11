import os
from typing import Dict, Any
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Google AI Configuration
GOOGLE_CONFIG = {
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "model_name": "models/gemini-2.5-pro",
    "temperature": 0.7
}

# Agent Configuration
AGENT_CONFIG = {
    "task_manager": {
        "name": "TaskManager",
        "description": "Coordinates tasks between agents"
    },
    "research": {
        "name": "ResearchAgent",
        "description": "Gathers and analyzes information"
    },
    "planning": {
        "name": "PlanningAgent",
        "description": "Creates execution plans"
    },
    "implementation": {
        "name": "ImplementationAgent",
        "description": "Executes planned tasks"
    },
    "qa": {
        "name": "QAAgent",
        "description": "Validates results"
    }
}

# System Configuration
SYSTEM_CONFIG = {
    "max_retries": 3,
    "timeout": 30,  # seconds
    "debug_mode": True
}

def get_agent_config(agent_type: str) -> Dict[str, Any]:
    """Get configuration for a specific agent type"""
    return AGENT_CONFIG.get(agent_type, {}) 