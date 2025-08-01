"""
Assemble AI - Main System Entry Point
-----------------------------------
This module serves as the entry point and orchestrator of the Assemble AI system,
demonstrating how our multi-agent system comes together and processes tasks efficiently.
"""

# 1. IMPORTS AND CONFIGURATION
# --------------------------
# Core system imports for async processing and type safety
import asyncio
from typing import Dict, Any
import sys
import os

# Add project root to Python path for proper imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration and LLM integration imports
from config.settings import GROQ_CONFIG
from langchain_groq import ChatGroq # type: ignore [reportMissingImports]
from dotenv import load_dotenv # type: ignore [reportMissingImports]

# Specialized agent imports
from .agents.research_agent import ResearchAgent
from .agents.planning_agent import PlanningAgent
from .agents.task_manager import TaskManager


# 2. AGENT SETUP AND INITIALIZATION
# -------------------------------
def setup_agents() -> Dict[str, Any]:
    """
    Initialize and configure the multi-agent system.
    
    Key Components:
    - Environment configuration loading
    - LLM initialization with Groq
    - Agent creation and configuration
    - Task manager orchestration setup
    
    Returns:
        Dict containing initialized agents and task manager
    """
    # Load environment variables for secure configuration
    load_dotenv()
    
    # Initialize Groq LLM with precise configuration
    # This ensures consistent and reliable AI responses
    llm = ChatGroq(
        model=GROQ_CONFIG["model"],          # Model selection
        groq_api_key=GROQ_CONFIG["api_key"], # Secure API key handling
        temperature=GROQ_CONFIG["temperature"],   # Response creativity control
        max_tokens=GROQ_CONFIG["max_tokens"],    # Response length control
        top_p=GROQ_CONFIG["top_p"],             # Response diversity
        request_timeout=GROQ_CONFIG["request_timeout"]  # Reliability timeout
    )
    
    # 3. SPECIALIZED AGENT CREATION
    # ---------------------------
    # Create specialized agents with dependency injection
    research_agent = ResearchAgent(llm=llm)  # Information gathering and analysis
    planning_agent = PlanningAgent(llm=llm)  # Implementation planning
    
    # Initialize task manager for agent orchestration
    task_manager = TaskManager(
        research_agent=research_agent,
        planning_agent=planning_agent
    )
    
    # Return initialized system components
    return {
        "research_agent": research_agent,
        "planning_agent": planning_agent,
        "task_manager": task_manager
    }


# 4. TASK PROCESSING PIPELINE
# -------------------------
async def process_task(task: Dict[str, Any], agents: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a task through the multi-agent system asynchronously.
    
    Features:
    - Asynchronous processing for efficiency
    - Structured task handling
    - Delegated processing through task manager
    
    Args:
        task: Task description and parameters
        agents: Dictionary of initialized agents
    
    Returns:
        Processed task results
    """
    task_manager = agents["task_manager"]
    return await task_manager.process_task(task)


# 5. MAIN EXECUTION FUNCTION
# ------------------------
async def main():
    """
    Main entry point demonstrating system capabilities.
    
    Demonstrates:
    - System initialization
    - Task structuring
    - Result handling
    - Error management
    """
    print("Setting up multi-agent system...")
    agents = setup_agents()
    
    # 6. EXAMPLE TASK STRUCTURE
    # -----------------------
    # Structured task with clear parameters
    example_task = {
        "description": "Research and create a plan for implementing a new machine learning model",
        "priority": "high",
        "deadline": "2025-07-12"
    }
    
    # 7. RESULT HANDLING AND PROCESSING
    # ------------------------------
    print("\nProcessing task:", example_task["description"])
    result = await process_task(example_task, agents)
    
    print("\nTask processing complete!")
    print("Status:", result.get("status"))
    
    # Structured result extraction and presentation
    if result.get("status") == "completed":
        print("\nResults:")
        # Research phase results
        if "research_phase" in result:
            print("\nResearch Findings:")
            print(result["research_phase"]["analysis"]["summary"])
        # Planning phase results
        if "planning_phase" in result:
            print("\nImplementation Plan:")
            print(result["planning_phase"]["implementation_plan"]["plan"])


# 8. SYSTEM ENTRY POINT
# -------------------
if __name__ == "__main__":
    # Initialize async event loop and run main function
    asyncio.run(main()) 