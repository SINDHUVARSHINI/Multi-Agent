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
            planning_prompt = f"""You are a technical project planning expert. Create a detailed implementation plan for the following task:

Task Description: {description}
Priority: {priority}
Deadline: {deadline}

Please provide a comprehensive implementation plan that includes:

1. Technical Requirements:
   - Required technologies and dependencies
   - API specifications
   - Development environment setup

2. Implementation Steps:
   - Step-by-step breakdown of development tasks
   - Integration points and considerations
   - Testing requirements for each step

3. Timeline and Milestones:
   - Estimated duration for each step
   - Critical path identification
   - Key milestones and deliverables

4. Quality Assurance:
   - Testing strategy
   - Performance benchmarks
   - Error handling considerations

5. Risk Assessment:
   - Potential technical challenges
   - Mitigation strategies
   - Fallback options

Format the response in a clear, structured way with markdown formatting. Use bullet points and numbered lists for clarity."""
            
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
        # Split the plan into sections and clean up
        sections = raw_plan.split("\n")
        cleaned_sections = [s.strip() for s in sections if s.strip()]
        
        return {
            "steps": cleaned_sections,
            "generated_at": "now",
            "confidence": 0.8,
            "format_version": "2.0"
        } 