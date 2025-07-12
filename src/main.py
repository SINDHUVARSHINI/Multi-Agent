import asyncio
from typing import Dict, Any
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GROQ_CONFIG
from langchain_groq import ChatGroq # type: ignore [reportMissingImports]
from dotenv import load_dotenv # type: ignore [reportMissingImports]
from .agents.research_agent import ResearchAgent
from .agents.planning_agent import PlanningAgent
from .agents.task_manager import TaskManager

def setup_agents() -> Dict[str, Any]:
    """Set up and return all required agents"""
    load_dotenv()
    
    # Initialize Groq LLM with configuration
    llm = ChatGroq(
        model=GROQ_CONFIG["model"],
        groq_api_key=GROQ_CONFIG["api_key"],
        temperature=GROQ_CONFIG["temperature"],
        max_tokens=GROQ_CONFIG["max_tokens"],
        top_p=GROQ_CONFIG["top_p"],
        request_timeout=GROQ_CONFIG["request_timeout"]
    )
    
    # Create agents
    research_agent = ResearchAgent(llm=llm)
    planning_agent = PlanningAgent(llm=llm)
    
    # Create task manager
    task_manager = TaskManager(
        research_agent=research_agent,
        planning_agent=planning_agent
    )
    
    return {
        "research_agent": research_agent,
        "planning_agent": planning_agent,
        "task_manager": task_manager
    }

async def process_task(task: Dict[str, Any], agents: Dict[str, Any]) -> Dict[str, Any]:
    """Process a task using the provided agents"""
    task_manager = agents["task_manager"]
    return await task_manager.process_task(task)

async def main():
    """Main entry point"""
    print("Setting up multi-agent system...")
    agents = setup_agents()
    
    # Example task
    example_task = {
        "description": "Research and create a plan for implementing a new machine learning model",
        "priority": "high",
        "deadline": "2024-12-31"
    }
    
    print("\nProcessing task:", example_task["description"])
    result = await process_task(example_task, agents)
    
    print("\nTask processing complete!")
    print("Status:", result.get("status"))
    if result.get("status") == "completed":
        print("\nResults:")
        if "research_phase" in result:
            print("\nResearch Findings:")
            print(result["research_phase"]["analysis"]["summary"])
        if "planning_phase" in result:
            print("\nImplementation Plan:")
            print(result["planning_phase"]["implementation_plan"]["plan"])

if __name__ == "__main__":
    asyncio.run(main()) 