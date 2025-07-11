from typing import Dict, Any, List
from .base_agent import BaseAgent
import asyncio

class TaskManagerAgent(BaseAgent):
    """Agent responsible for coordinating other agents"""
    
    def __init__(self, name: str = "TaskManager"):
        super().__init__(name)
        self.agents: List[BaseAgent] = []
        
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the task manager"""
        self.agents.append(agent)
        
    async def process(self, task: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
        """Process a task by coordinating multiple agents"""
        self.update_state(status="working", current_task=task)
        
        try:
            # Create tasks for all agents
            tasks = []
            for i, agent in enumerate(self.agents):
                print(f"  🔄 Starting {agent.__class__.__name__}...")
                tasks.append(asyncio.create_task(agent.process(task)))
            
            # Wait for all tasks with timeout
            print("  ⏳ Waiting for agent responses (timeout:", timeout, "seconds)...")
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout)
            print("  ✓ All agents completed successfully")
            
            # Combine results with better error handling
            combined_results = {
                "status": "completed",
                "research_results": {},
                "plan": {}
            }
            
            for result in results:
                if isinstance(result, dict):
                    if "research_query" in result:
                        combined_results["research_results"] = result
                    elif "plan" in result:
                        combined_results["plan"] = result.get("plan", {})
            
            # Validate results
            if not combined_results["research_results"]:
                print("  ⚠️ Warning: No research results available")
            if not combined_results["plan"]:
                print("  ⚠️ Warning: No planning results available")
            
            self.update_state(status="idle", current_task=None)
            return combined_results
            
        except asyncio.TimeoutError:
            print(f"\n  ⚠️ Task timed out after {timeout} seconds")
            print("  💡 Tip: Try increasing the timeout or simplifying the task")
            self.update_state(status="error", current_task=None)
            return {
                "status": "error",
                "message": f"Task timed out after {timeout} seconds"
            }
        except Exception as e:
            print(f"\n  ❌ Error: {str(e)}")
            self.update_state(status="error", current_task=None)
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _break_down_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Break down a complex task into subtasks"""
        # This is a simplified version - in practice, you'd want more sophisticated
        # task decomposition logic based on task type, complexity, etc.
        return [
            {
                "type": "research",
                "description": f"Research information for {task.get('description', '')}"
            },
            {
                "type": "planning",
                "description": f"Create execution plan for {task.get('description', '')}"
            },
            {
                "type": "implementation",
                "description": f"Implement solution for {task.get('description', '')}"
            },
            {
                "type": "qa",
                "description": f"Validate results for {task.get('description', '')}"
            }
        ]
        
    def _select_agent_for_task(self, task: Dict[str, Any]) -> str:
        """Select the most appropriate agent for a task"""
        # Simple mapping of task types to agent names
        task_to_agent = {
            "research": "ResearchAgent",
            "planning": "PlanningAgent",
            "implementation": "ImplementationAgent",
            "qa": "QAAgent"
        }
        
        task_type = task.get("type")
        if task_type not in task_to_agent:
            raise ValueError(f"No agent available for task type: {task_type}")
            
        agent_name = task_to_agent[task_type]
        if agent_name not in self.agent_pool: # type: ignore [reportUnknownMemberType]
            raise ValueError(f"Required agent {agent_name} not found in pool")
            
        return agent_name
        
    def _combine_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine results from multiple subtasks"""
        # This is a simplified version - in practice, you'd want more sophisticated
        # result combination logic based on task type, dependencies, etc.
        return {
            "status": "completed",
            "subtask_results": results,
            "summary": "Combined results from all subtasks"
        } 