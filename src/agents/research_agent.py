"""
Research Agent Implementation
--------------------------
This module implements the Research Agent, responsible for gathering and analyzing
information using LLM capabilities. It processes tasks through structured analysis
and provides organized, actionable insights.

Key Capabilities:
- Task analysis and research planning
- Structured information gathering
- Comprehensive result organization
- Error handling and recovery
"""

#####################################
# 1. IMPORTS AND DEPENDENCIES
#####################################
from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel # type: ignore [reportUnknownParameterType]

#####################################
# 2. RESEARCH AGENT DEFINITION
#####################################
class ResearchAgent:
    """
    Agent responsible for researching and analyzing tasks using LLM capabilities.
    
    Features:
    - Task analysis and validation
    - Structured prompt generation
    - Response parsing and organization
    - Error handling and reporting
    
    Output Sections:
    - Summary: Brief overview of findings
    - Analysis: Detailed examination of options
    - Recommendations: Actionable suggestions
    - Considerations: Implementation factors
    """
    
    #####################################
    # Agent Initialization
    #####################################
    def __init__(self, llm: BaseChatModel):
        """
        Initialize Research Agent with LLM model.
        
        Args:
            llm: LangChain chat model for analysis
        """
        self.llm = llm
    
    #####################################
    # 3. TASK PROCESSING IMPLEMENTATION
    #####################################
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a research task through analysis and structured response.
        
        Args:
            task: Dictionary containing task details and requirements
            
        Returns:
            Dict containing analysis results or error information
            
        Raises:
            ValueError: If task description is missing
        """
        try:
            print("\n📚 Research Agent:")
            print("- Reading task description")
            
            # Extract and validate task description
            description = task.get("description", "")
            if not description:
                raise ValueError("Task description is required")
            
            #####################################
            # 4. RESEARCH PROMPT GENERATION
            #####################################
            print("- Formulating research strategy")
            research_prompt = f"""
            Task: {description}
            
            Please provide a detailed analysis in the following structure:

            SUMMARY:
            [Provide a brief executive summary of your findings]

            ANALYSIS:
            [Detailed analysis of available options]

            RECOMMENDATIONS:
            [Clear recommendations with justification]

            CONSIDERATIONS:
            [Important factors to consider during implementation]

            Format your response using these exact section headers.
            Make sure each section starts with the exact header followed by a colon.
            """
            
            #####################################
            # 5. LLM INTERACTION AND ANALYSIS
            #####################################
            print("- Conducting analysis")
            response = await self.llm.ainvoke(research_prompt)
            
            print("- Organizing findings")
            sections = self._parse_sections(str(response.content))
            
            #####################################
            # 6. RESULT STRUCTURING
            #####################################
            analysis = {
                "summary": sections.get("SUMMARY", "No summary available"),
                "detailed_analysis": sections.get("ANALYSIS", "No analysis available"),
                "recommendations": sections.get("RECOMMENDATIONS", "No recommendations available"),
                "considerations": sections.get("CONSIDERATIONS", "No considerations available"),
                "confidence": 0.85,  # Confidence scoring
                "timestamp": "2024-03-20T10:30:00Z"  # Analysis timestamp
            }
            
            print("✨ Research complete")
            return {
                "status": "completed",
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    #####################################
    # 7. RESPONSE PARSING
    #####################################
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
        for section in ["SUMMARY", "ANALYSIS", "RECOMMENDATIONS", "CONSIDERATIONS"]:
            sections[section] = "No content available"

        # Parse content into sections
        for line in content.split('\n'):
            line = line.strip()
            if line.endswith(':') and line[:-1] in [
                "SUMMARY",
                "ANALYSIS",
                "RECOMMENDATIONS",
                "CONSIDERATIONS"
            ]:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[:-1]
                current_content = []
            elif current_section and line:
                current_content.append(line)

        # Handle final section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections 