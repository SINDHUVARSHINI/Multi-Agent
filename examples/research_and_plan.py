import asyncio
from src.main import setup_agents, process_task
import time

async def main():
    """Run the example"""
    print("🤖 Multi-Agent Research and Planning Example")
    print("=" * 50 + "\n")

    print("1. Setting up agent system...")
    task_manager = await setup_agents()
    print("✓ Agents initialized\n")

    print("2. Submitting task to agent system...")
    # Very simple task for testing
    task = {
        "description": """
        Recommend a weather API for a basic weather app that shows:
        - Current temperature
        - Today's forecast
        - Basic weather conditions (sunny, rainy, etc.)
        """,
        "priority": "medium",
        "deadline": "2024-12-31"
    }
    print("\nTask description:", task["description"])
    print("\nProcessing (this may take a minute)...")
    
    try:
        start_time = time.time()
        result = await process_task(task_manager, task)
        duration = time.time() - start_time
        
        print(f"\n3. Results (took {duration:.1f} seconds):")
        print("-" * 30)
        
        if result.get("status") == "error":
            print(f"❌ Task failed: {result.get('message')}")
        else:
            # Research findings
            print("\n📚 Research Findings:")
            research_results = result.get("research_results", {})
            if isinstance(research_results.get("analysis", {}).get("key_insights"), list):
                insights = research_results.get("analysis", {}).get("key_insights", [])
                for finding in insights:
                    if finding and finding.strip():
                        print(f"  {finding.strip()}")
            elif isinstance(research_results.get("analysis"), str):
                print(f"  {research_results.get('analysis')}")
            
            # Implementation plan
            print("\n📋 Implementation Plan:")
            plan = result.get("plan", {})
            if not plan:
                print("  ⚠️ No implementation plan available")
            else:
                steps = plan.get("steps", [])
                if not steps:
                    print("  ⚠️ No implementation steps available")
                else:
                    for step in steps:
                        if step and step.strip():
                            print(f"  • {step.strip()}")
            
            # Performance metrics
            print("\n📊 Performance Metrics:")
            print(f"  • Total processing time: {duration:.1f} seconds")
            print(f"  • Research confidence: {research_results.get('analysis', {}).get('confidence_score', 'N/A')}")
            if plan:
                print(f"  • Planning confidence: {plan.get('confidence', 'N/A')}")
                print(f"  • Plan format version: {plan.get('format_version', '1.0')}")
    
    except Exception as e:
        print(f"\nError processing task: {str(e)}")
    
    print("\n✨ Example complete")

if __name__ == "__main__":
    asyncio.run(main()) 