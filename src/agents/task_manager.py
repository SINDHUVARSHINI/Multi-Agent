from typing import Dict, Any
from .research_agent import ResearchAgent
from .planning_agent import PlanningAgent

class TaskManager:
    """Manages task distribution and coordination between agents"""
    
    def __init__(self, research_agent: ResearchAgent, planning_agent: PlanningAgent):
        self.research_agent = research_agent
        self.planning_agent = planning_agent
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task through the multi-agent system"""
        try:
            # Step 1: Research phase
            print("\n🔍 Starting research phase...")
            print("- Analyzing requirements")
            print("- Gathering information")
            print("- Evaluating options")
            research_results = await self.research_agent.process(task)
            
            if research_results["status"] != "completed":
                print("❌ Research phase failed")
                return {
                    "status": "error",
                    "message": "Research phase failed",
                    "details": research_results
                }
            
            print("✅ Research phase completed successfully")
            
            # Step 2: Planning phase
            print("\n📋 Starting planning phase...")
            print("- Creating implementation plan")
            print("- Defining technical specifications")
            print("- Estimating timeline")
            
            # Prepare planning task with complete research results
            planning_task = {
                **task,
                "research_results": {
                    "summary": research_results["analysis"]["summary"],
                    "detailed_analysis": research_results["analysis"]["detailed_analysis"],
                    "recommendations": research_results["analysis"]["recommendations"],
                    "considerations": research_results["analysis"]["considerations"]
                }
            }
            
            planning_results = await self.planning_agent.process(planning_task)
            
            if planning_results["status"] != "completed":
                print("❌ Planning phase failed")
                return {
                    "status": "error",
                    "message": "Planning phase failed",
                    "details": planning_results
                }
            
            print("✅ Planning phase completed successfully")
            
            # Step 3: Combine results
            print("\n🎯 Finalizing results...")
            return {
                "status": "completed",
                "research_phase": research_results,
                "planning_phase": planning_results,
                "confidence_scores": {
                    "research": research_results["analysis"]["confidence"],
                    "planning": planning_results["confidence_scores"]["plan"]
                }
            }
            
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "details": None
            } 