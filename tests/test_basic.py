import sys
import os
import asyncio
import pytest # type: ignore [import-untyped]
from typing import Dict, Any

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.task_manager import TaskManagerAgent
from src.agents.research_agent import ResearchAgent
from src.agents.planning_agent import PlanningAgent
from src.utils.helpers import validate_task_result, calculate_task_metrics

@pytest.fixture
async def task_manager():
    """Fixture to create a configured TaskManagerAgent"""
    manager = TaskManagerAgent()
    
    # Create and register test agents
    research_agent = ResearchAgent(name="TestResearchAgent")
    planning_agent = PlanningAgent(name="TestPlanningAgent")
    
    manager.register_agent(research_agent)
    manager.register_agent(planning_agent)
    
    return manager

@pytest.mark.asyncio
async def test_task_manager_initialization(task_manager):
    """Test that TaskManager initializes correctly"""
    assert isinstance(task_manager, TaskManagerAgent)
    assert len(task_manager.agent_pool) == 2 # type: ignore [reportUnknownMemberType]
    assert "TestResearchAgent" in task_manager.agent_pool # type: ignore [reportUnknownMemberType]
    assert "TestPlanningAgent" in task_manager.agent_pool # type: ignore [reportUnknownMemberType]

@pytest.mark.asyncio
async def test_basic_task_processing(task_manager):
    """Test processing a basic task"""
    task = {
        "description": "Test task for basic processing",
        "priority": "medium",
        "deadline": "2024-12-31"
    }
    
    result = await task_manager.process(task)
    
    assert isinstance(result, dict)
    assert "status" in result
    assert validate_task_result(result)
    
    # Calculate and verify metrics
    metrics = calculate_task_metrics(result)
    assert isinstance(metrics, dict)
    assert "success_rate" in metrics
    assert "complexity_score" in metrics

@pytest.mark.asyncio
async def test_error_handling(task_manager):
    """Test error handling for invalid tasks"""
    invalid_task = {}  # Empty task should cause an error
    
    with pytest.raises(Exception):
        await task_manager.process(invalid_task)

@pytest.mark.asyncio
async def test_agent_state_management(task_manager):
    """Test agent state management during task processing"""
    task = {
        "description": "Test task for state management",
        "priority": "high"
    }
    
    # Get initial states
    initial_states = {
        name: agent.get_status()
        for name, agent in task_manager.agent_pool.items()
    }
    
    # Process task
    result = await task_manager.process(task)
    
    # Get final states
    final_states = {
        name: agent.get_status()
        for name, agent in task_manager.agent_pool.items()
    }
    
    # Verify state transitions
    for name in task_manager.agent_pool:
        assert initial_states[name] == "idle"  # Should start idle
        assert final_states[name] == "idle"    # Should end idle

@pytest.mark.asyncio
async def test_task_breakdown(task_manager):
    """Test that tasks are properly broken down into subtasks"""
    task = {
        "description": "Complex task requiring multiple agents",
        "requirements": ["req1", "req2"],
        "priority": "high"
    }
    
    result = await task_manager.process(task)
    
    # Verify subtasks were created
    assert "subtask_results" in result
    assert len(result["subtask_results"]) > 0
    
    # Verify each subtask has required fields
    for subtask in result["subtask_results"]:
        assert "status" in subtask
        assert "description" in subtask

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 