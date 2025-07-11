import asyncio
from typing import Dict, Any
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GOOGLE_CONFIG, SYSTEM_CONFIG
from src.agents.task_manager import TaskManagerAgent
from src.agents.research_agent import ResearchAgent
from src.agents.planning_agent import PlanningAgent

async def setup_agents() -> TaskManagerAgent: # type: ignore [reportUnknownReturnType]
    """Set up and configure all agents"""
    # Create task manager
    task_manager = TaskManagerAgent()
    
    # Create specialized agents
    research_agent = ResearchAgent(google_api_key=GOOGLE_CONFIG["api_key"])
    planning_agent = PlanningAgent(google_api_key=GOOGLE_CONFIG["api_key"])
    
    # Register agents with task manager
    task_manager.register_agent(research_agent)
    task_manager.register_agent(planning_agent)
    
    return task_manager

async def process_task(task_manager: TaskManagerAgent, task: Dict[str, Any]) -> Dict[str, Any]:
    """Process a task through the multi-agent system"""
    try:
        return await task_manager.process(task)
    except Exception as e:
        print(f"Error processing task: {str(e)}")
        return {"status": "error", "message": str(e)}

async def main():
    """Main entry point"""
    print("Setting up multi-agent system...")
    task_manager = await setup_agents()
    
    # Example task
    example_task = {
        "description": "Research and create a plan for implementing a new machine learning model",
        "priority": "high",
        "deadline": "2024-12-31"
    }
    
    print("\nProcessing task:", example_task["description"])
    result = await process_task(task_manager, example_task)
    
    print("\nTask processing complete!")
    print("Status:", result.get("status"))
    if result.get("status") == "completed":
        print("\nSubtask Results:")
        for subtask in result.get("subtask_results", []):
            print(f"- {subtask.get('status', 'unknown')}: {subtask.get('description', 'no description')}")

if __name__ == "__main__":
    # Set up asyncio event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        loop.close() 