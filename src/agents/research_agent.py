from typing import Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel # type: ignore [reportUnknownParameterType]

class ResearchAgent:
    """Agent responsible for researching and analyzing tasks"""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a research task"""
        try:
            print("\n📚 Research Agent:")
            print("- Reading task description")
            
            # Extract task description
            description = task.get("description", "")
            if not description:
                raise ValueError("Task description is required")
            
            print("- Formulating research strategy")
            # Prepare the research prompt
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
            
            print("- Conducting analysis")
            # Get analysis from LLM
            response = await self.llm.ainvoke(research_prompt)
            
            print("- Organizing findings")
            # Parse sections from the response
            sections = self._parse_sections(str(response.content))
            
            # Structure the results
            analysis = {
                "summary": sections.get("SUMMARY", "No summary available"),
                "detailed_analysis": sections.get("ANALYSIS", "No analysis available"),
                "recommendations": sections.get("RECOMMENDATIONS", "No recommendations available"),
                "considerations": sections.get("CONSIDERATIONS", "No considerations available"),
                "confidence": 0.85,  # Example confidence score
                "timestamp": "2024-03-20T10:30:00Z"  # Example timestamp
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

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse sections from the LLM response"""
        sections = {}
        current_section = None
        current_content = []

        # Initialize sections with default values
        for section in ["SUMMARY", "ANALYSIS", "RECOMMENDATIONS", "CONSIDERATIONS"]:
            sections[section] = "No content available"

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

        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections 