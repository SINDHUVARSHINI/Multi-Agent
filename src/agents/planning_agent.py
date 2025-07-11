from typing import Dict, Any, List
from .base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore [import-untyped]
from langchain.schema import HumanMessage, SystemMessage # type: ignore [import-untyped]

class PlanningAgent(BaseAgent):
    """Agent responsible for creating execution plans"""
    
    def __init__(self, name: str = "PlanningAgent", google_api_key: str = None): # type: ignore
        super().__init__(name)
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            google_api_key=google_api_key,
            temperature=0.7
        )
        
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a planning task"""
        self.update_state(status="working", current_task=task)
        
        try:
            # Extract task details
            description = task.get("description", "")
            priority = task.get("priority", "medium")
            deadline = task.get("deadline", "not specified")
            
            # Create planning prompt
            planning_prompt = f"""You are a project planning expert. Please create a detailed implementation plan for the following task:

Task Description: {description}
Priority: {priority}
Deadline: {deadline}

Please provide:
1. A breakdown of implementation steps
2. Resource requirements
3. Timeline estimates
4. Risk considerations

Format the response in a clear, structured way."""
            
            # Generate plan
            messages = [HumanMessage(content=planning_prompt)]
            response = await self.llm.agenerate([messages])
            
            # Process and structure the response
            plan = self._structure_plan(response.generations[0][0].text)
            
            result = {
                "status": "completed",
                "plan": plan
            }
            
            self.update_state(status="idle", current_task=None)
            return result
            
        except Exception as e:
            self.update_state(status="error", current_task=None)
            raise
            
    def _structure_plan(self, raw_plan: str) -> Dict[str, Any]:
        """Structure the raw plan into a formatted response"""
        return {
            "steps": raw_plan.split("\n"),
            "generated_at": "now",
            "confidence": 0.8
        } 