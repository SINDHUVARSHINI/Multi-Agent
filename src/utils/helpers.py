import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

def format_task_description(task: Dict[str, Any]) -> str:
    """Format a task dictionary into a readable string"""
    parts = []
    
    # Add description
    if "description" in task:
        parts.append(f"Description: {task['description']}")
    
    # Add priority if present
    if "priority" in task:
        parts.append(f"Priority: {task['priority'].upper()}")
    
    # Add deadline if present
    if "deadline" in task:
        parts.append(f"Deadline: {task['deadline']}")
    
    # Add requirements if present
    if "requirements" in task:
        parts.append("Requirements:")
        for req in task["requirements"]:
            parts.append(f"- {req}")
    
    return "\n".join(parts)

def calculate_task_metrics(task_result: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate metrics from a task result"""
    metrics = {
        "completion_time": None,
        "success_rate": 0.0,
        "complexity_score": 0
    }
    
    # Calculate completion time if start/end times are present
    if "start_time" in task_result and "end_time" in task_result:
        start = datetime.fromisoformat(task_result["start_time"])
        end = datetime.fromisoformat(task_result["end_time"])
        metrics["completion_time"] = str(end - start)
    
    # Calculate success rate based on subtask results
    subtasks = task_result.get("subtask_results", [])
    if subtasks:
        successful = sum(1 for task in subtasks if task.get("status") == "completed")
        metrics["success_rate"] = (successful / len(subtasks)) * 100
    
    # Calculate complexity score based on various factors
    metrics["complexity_score"] = _calculate_complexity(task_result)
    
    return metrics

def _calculate_complexity(task_result: Dict[str, Any]) -> int:
    """Calculate a complexity score for a task result"""
    score = 0
    
    # Add points for each subtask
    score += len(task_result.get("subtask_results", []))
    
    # Add points for requirements
    score += len(task_result.get("requirements", []))
    
    # Add points for dependencies
    for subtask in task_result.get("subtask_results", []):
        score += len(subtask.get("dependencies", []))
    
    return score

def validate_task_result(result: Dict[str, Any]) -> bool:
    """Validate that a task result contains all required fields"""
    required_fields = {"status", "subtask_results"}
    return all(field in result for field in required_fields)

def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string"""
    duration = timedelta(seconds=seconds)
    
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def save_task_result(result: Dict[str, Any], filepath: str) -> None:
    """Save a task result to a JSON file"""
    with open(filepath, 'w') as f:
        json.dump(result, f, indent=2)

def load_task_result(filepath: str) -> Optional[Dict[str, Any]]:
    """Load a task result from a JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None 