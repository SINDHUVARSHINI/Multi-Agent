from typing import Dict, Any, List
from .base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore [import-untyped]
from langchain.schema import HumanMessage, SystemMessage # type: ignore [import-untyped]

class ResearchAgent(BaseAgent):
    """Agent responsible for gathering and analyzing information"""
    
    def __init__(self, name: str = "ResearchAgent", google_api_key: str = None): # type: ignore
        super().__init__(name)
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            google_api_key=google_api_key,
            temperature=0.7
        )
        
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a research task"""
        self.update_state(status="working", current_task=task)
        
        try:
            # Extract relevant information from task
            description = task.get("description", "")
            
            # Prepare research query
            research_query = self._prepare_research_query(description)
            
            # Gather information using LLM
            research_results = await self._gather_information(research_query)
            
            # Analyze gathered information
            analysis = await self._analyze_information(research_results)
            
            # Prepare final results
            result = {
                "status": "completed",
                "research_query": research_query,
                "raw_results": research_results,
                "analysis": analysis
            }
            
            self.update_state(status="idle", current_task=None)
            return result
            
        except Exception as e:
            self.update_state(status="error", current_task=None)
            raise
            
    def _prepare_research_query(self, description: str) -> str:
        """Prepare a research query from task description"""
        return f"Research and analyze: {description}"
        
    async def _gather_information(self, query: str) -> List[Dict[str, Any]]:
        """Gather information using LLM"""
        # Combine system and human messages into a single human message
        combined_prompt = f"""You are a research assistant tasked with gathering comprehensive information.

Query: {query}

Please provide detailed, well-structured information addressing all aspects of the query."""

        messages = [HumanMessage(content=combined_prompt)]
        
        response = await self.llm.agenerate([messages])
        
        return [{
            "source": "LLM",
            "content": response.generations[0][0].text,
            "confidence": 0.8
        }]
        
    async def _analyze_information(self, research_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze gathered information"""
        combined_results = "\n".join(
            result["content"] for result in research_results
        )
        
        # Combine system and human messages into a single human message
        combined_prompt = f"""You are an analyst tasked with extracting key insights from research data.

Research Results:
{combined_results}

Please analyze these results and provide key insights in a clear, structured format."""

        messages = [HumanMessage(content=combined_prompt)]
        
        response = await self.llm.agenerate([messages])
        
        return {
            "key_insights": response.generations[0][0].text.split("\n"),
            "confidence_score": 0.8,
            "analysis_method": "LLM-based semantic analysis"
        } 