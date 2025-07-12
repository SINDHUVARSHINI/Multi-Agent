import asyncio
from src.main import setup_agents, process_task
import time

async def main():
    """Run the example"""
    print("🤖 Multi-Agent Research and Planning Example")
    print("=" * 50 + "\n")

    print("1. Setting up agent system...")
    agents = setup_agents()
    print("✓ Agents initialized\n")

    print("2. Submitting task to agent system...")
    # Very simple task for testing
    task = {
        "description": """
        Recommend a weather API for a basic weather app that shows:
        - Current temperature
        - Today's forecast
        - Basic weather conditions (sunny, rainy, etc.)
        """
    }
    print("\nTask description:", task["description"])
    print("\nProcessing (this may take a minute)...")
    
    try:
        start_time = time.time()
        result = await process_task(task, agents)
        duration = time.time() - start_time
        
        print(f"\n3. Results (took {duration:.1f} seconds):")
        print("=" * 50)
        
        if result.get("status") == "error":
            print(f"❌ Task failed: {result.get('message')}")
            if result.get("details"):
                print("Details:", result["details"])
        else:
            # Research findings
            print("\n📚 Research Findings")
            print("-" * 30)
            research_phase = result.get("research_phase", {})
            analysis = research_phase.get("analysis", {})
            
            print("\n🎯 Executive Summary:")
            print(analysis.get("summary", "No summary available"))
            
            print("\n📊 Detailed Analysis:")
            print(analysis.get("detailed_analysis", "No analysis available"))
            
            print("\n💡 Recommendations:")
            print(analysis.get("recommendations", "No recommendations available"))
            
            print("\n⚠️ Implementation Considerations:")
            print(analysis.get("considerations", "No considerations available"))
            
            # Implementation plan
            print("\n📋 Implementation Plan")
            print("-" * 30)
            planning_phase = result.get("planning_phase", {})
            implementation_plan = planning_phase.get("implementation_plan", {})
            
            if implementation_plan:
                print("\n📝 Step-by-Step Plan:")
                print(implementation_plan.get("plan", "No plan available"))
                
                print("\n⚙️ Technical Specifications:")
                tech_specs = implementation_plan.get("technical_specifications", {})
                print(tech_specs.get("specifications", "No specifications available"))
                
                print("\n⏱️ Timeline:")
                timeline = implementation_plan.get("timeline", {})
                print(timeline.get("timeline", "No timeline available"))
                
                print("\n📦 Required Resources:")
                print(implementation_plan.get("resources", "No resources specified"))
                
                print("\n🛡️ Risks and Mitigations:")
                print(implementation_plan.get("risks_and_mitigations", "No risks specified"))
            else:
                print("  ⚠️ No implementation plan available")
            
            # Performance metrics
            print("\n📊 Performance Metrics")
            print("-" * 30)
            print(f"• Total processing time: {duration:.1f} seconds")
            confidence_scores = result.get("confidence_scores", {})
            print(f"• Research confidence: {confidence_scores.get('research', 'N/A')}")
            print(f"• Planning confidence: {confidence_scores.get('planning', 'N/A')}")
    
    except Exception as e:
        print(f"\nError processing task: {str(e)}")
    
    print("\n✨ Example complete")

if __name__ == "__main__":
    asyncio.run(main()) 