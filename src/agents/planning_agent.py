from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel # type: ignore [reportUnknownParameterType]

class PlanningAgent:
    """Agent responsible for creating implementation plans"""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a planning task"""
        try:
            print("\n📝 Planning Agent:")
            print("- Reviewing research findings")
            
            # Extract task info and research results
            description = task.get("description", "")
            research_results = task.get("research_results", {})
            if not description or not research_results:
                raise ValueError("Task description and research results are required")
            
            print("- Creating implementation plan")
            # Prepare the planning prompt
            planning_prompt = f"""
            Task: {description}
            
            Research Summary: {research_results.get('summary', '')}
            Detailed Analysis: {research_results.get('detailed_analysis', '')}
            Recommendations: {research_results.get('recommendations', '')}
            Implementation Considerations: {research_results.get('considerations', '')}
            
            Based on the research findings above, create a detailed implementation plan.
            Format your response using these exact section headers:

            ## IMPLEMENTATION_PLAN:
            [Provide a detailed, step-by-step implementation guide]

            ## TECHNICAL_SPECIFICATIONS:
            [List API endpoints, data structures, and technical requirements]

            ## TIMELINE:
            [Provide time estimates and milestones]

            ## RESOURCES:
            [List required tools and dependencies]

            ## RISKS_AND_MITIGATIONS:
            [List potential risks and mitigation strategies]

            Make each section comprehensive and immediately actionable.
            """
            
            print("- Generating technical specifications")
            # Get plan from LLM
            response = await self.llm.ainvoke(planning_prompt)
            
            print("- Estimating timeline")
            # Parse sections from the response
            sections = self._parse_sections(str(response.content))
            
            # Structure the results
            implementation_plan = {
                "plan": sections.get("IMPLEMENTATION_PLAN", "No implementation plan available"),
                "technical_specifications": {
                    "specifications": sections.get("TECHNICAL_SPECIFICATIONS", "No specifications available")
                },
                "timeline": {
                    "timeline": sections.get("TIMELINE", "No timeline available")
                },
                "resources": sections.get("RESOURCES", "No resources specified"),
                "risks_and_mitigations": sections.get("RISKS_AND_MITIGATIONS", "No risks specified")
            }
            
            print("✨ Planning complete")
            return {
                "status": "completed",
                "implementation_plan": implementation_plan,
                "confidence_scores": {
                    "plan": 0.9  # Example confidence score
                }
            }
            
        except Exception as e:
            print(f"❌ Planning failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse sections from the LLM response"""
        sections = {}
        current_section = None
        current_content = []

        # Initialize sections with default values
        for section in [
            "IMPLEMENTATION_PLAN",
            "TECHNICAL_SPECIFICATIONS",
            "TIMELINE",
            "RESOURCES",
            "RISKS_AND_MITIGATIONS"
        ]:
            sections[section] = "No content available"

        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('## ') and ':' in line:
                section_name = line[3:].split(':')[0].strip()
                if section_name in sections:
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = section_name
                    current_content = []
            elif current_section and line:
                current_content.append(line)

        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections 