"""
Planning Agent Implementation
--------------------------
This module implements the Planning Agent, responsible for creating detailed
implementation plans based on research findings. It transforms analysis into
actionable steps with technical specifications and risk assessments.

Key Capabilities:
- Research interpretation
- Implementation planning
- Technical specification generation
- Timeline estimation
- Risk assessment and mitigation
"""

# 1. IMPORTS AND DEPENDENCIES
# ------------------------
from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel # type: ignore [reportUnknownParameterType]

# 2. PLANNING AGENT DEFINITION
# -------------------------
class PlanningAgent:
    """
    Agent responsible for creating comprehensive implementation plans.
    
    Features:
    - Research result interpretation
    - Detailed plan generation
    - Technical specification creation
    - Timeline estimation
    - Resource identification
    - Risk assessment
    
    Output Sections:
    - Implementation Plan: Step-by-step guide
    - Technical Specifications: System requirements
    - Timeline: Project milestones
    - Resources: Required tools and dependencies
    - Risks and Mitigations: Risk management strategy
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        Initialize Planning Agent with LLM model.
        
        Args:
            llm: LangChain chat model for plan generation
        """
        self.llm = llm
    
    # 3. TASK PROCESSING IMPLEMENTATION
    # ------------------------------
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a planning task and generate implementation details.
        
        Args:
            task: Dictionary containing task description and research results
            
        Returns:
            Dict containing implementation plan or error information
            
        Raises:
            ValueError: If required information is missing
        """
        try:
            print("\n📝 Planning Agent:")
            print("- Reviewing research findings")
            
            # 4. INPUT VALIDATION AND PREPARATION
            # --------------------------------
            description = task.get("description", "")
            research_results = task.get("research_results", {})
            if not description or not research_results:
                raise ValueError("Task description and research results are required")
            
            # 5. PLAN GENERATION
            # ---------------
            print("- Creating implementation plan")
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
            
            # 6. LLM INTERACTION AND PROCESSING
            # ------------------------------
            print("- Generating technical specifications")
            response = await self.llm.ainvoke(planning_prompt)
            
            print("- Estimating timeline")
            sections = self._parse_sections(str(response.content))
            
            # 7. RESULT STRUCTURING
            # ------------------
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
                    "plan": 0.9  # Confidence scoring
                }
            }
            
        except Exception as e:
            print(f"❌ Planning failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    # 8. RESPONSE PARSING
    # ----------------
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse and organize sections from LLM response.
        
        Args:
            content: Raw LLM response text
            
        Returns:
            Dictionary of parsed sections with standardized format
            
        Features:
        - Section identification
        - Content aggregation
        - Default value handling
        - Structured output
        """
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

        # Parse content into sections
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

        # Handle final section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections 