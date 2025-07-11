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
            insights = result.get("research_results", {}).get("analysis", {}).get("key_insights", [])
            for finding in insights:
                if finding and finding.strip():
                    print(f"  {finding.strip()}")
            
            # Implementation plan
            print("\n📋 Implementation Plan:")
            plan_steps = result.get("plan", {}).get("steps", [])
            if isinstance(plan_steps, list):
                for step in plan_steps:
                    if step and step.strip():
                        print(f"  • {step.strip()}")
            elif isinstance(plan_steps, str):
                for line in plan_steps.split('\n'):
                    if line and line.strip():
                        print(f"  • {line.strip()}")
    
    except Exception as e:
        print(f"\nError processing task: {str(e)}")
    
    print("\n✨ Example complete")

if __name__ == "__main__":
    asyncio.run(main()) 