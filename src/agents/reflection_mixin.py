from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field # type: ignore
import time

class ReflectionLog(BaseModel):
    """Model for storing reflection data"""
    timestamp: float
    action: str
    outcome: str
    success: bool
    error: Optional[str] = Field(default=None)
    learning_points: List[str] = Field(default_factory=list)
    confidence: float
    improvement_suggestions: List[str] = Field(default_factory=list)

class ReflectionMixin:
    """Mixin to add self-reflection capabilities to agents"""
    
    def __init__(self):
        self.reflection_logs: List[ReflectionLog] = []
        self.performance_metrics: Dict[str, float] = {
            "success_rate": 1.0,
            "average_confidence": 0.0,
            "tasks_completed": 0
        }
    
    def reflect_on_action(self, action: str, outcome: Dict[str, Any], success: bool = True, error: Optional[str] = None) -> None:
        """Record and analyze an action's outcome"""
        reflection = self._analyze_outcome(action, outcome, success, error)
        self.reflection_logs.append(reflection)
        self._update_metrics(reflection)
        
        if not success or reflection.confidence < 0.7:
            self._trigger_improvement_analysis(reflection)
    
    def _analyze_outcome(self, action: str, outcome: Dict[str, Any], success: bool, error: Optional[str] = None) -> ReflectionLog:
        """Analyze the outcome of an action"""
        learning_points = []
        improvement_suggestions = []
        confidence = 0.8 if success else 0.4
        
        if success:
            learning_points.append(f"Successfully completed {action}")
            if isinstance(outcome.get("confidence_scores"), dict):
                confidence = sum(outcome["confidence_scores"].values()) / len(outcome["confidence_scores"])
        else:
            error_msg = error if error else "Unknown error"
            learning_points.append(f"Failed to complete {action}: {error_msg}")
            improvement_suggestions.append(self._generate_improvement_suggestion(action, error))
        
        return ReflectionLog(
            timestamp=time.time(),
            action=action,
            outcome=str(outcome),
            success=success,
            error=error,
            learning_points=learning_points,
            confidence=confidence,
            improvement_suggestions=improvement_suggestions
        )
    
    def _update_metrics(self, reflection: ReflectionLog) -> None:
        """Update performance metrics based on reflection"""
        self.performance_metrics["tasks_completed"] += 1
        
        # Update success rate
        total_tasks = self.performance_metrics["tasks_completed"]
        current_success_rate = self.performance_metrics["success_rate"]
        new_success_rate = ((current_success_rate * (total_tasks - 1)) + (1 if reflection.success else 0)) / total_tasks
        self.performance_metrics["success_rate"] = new_success_rate
        
        # Update average confidence
        current_avg_confidence = self.performance_metrics["average_confidence"]
        new_avg_confidence = ((current_avg_confidence * (total_tasks - 1)) + reflection.confidence) / total_tasks
        self.performance_metrics["average_confidence"] = new_avg_confidence
    
    def _trigger_improvement_analysis(self, reflection: ReflectionLog) -> None:
        """Analyze failures and low confidence outcomes"""
        if not reflection.success:
            self._analyze_failure(reflection)
        elif reflection.confidence < 0.7:
            self._analyze_low_confidence(reflection)
    
    def _analyze_failure(self, reflection: ReflectionLog) -> None:
        """Analyze failure cases"""
        error_type = self._categorize_error(reflection.error)
        reflection.improvement_suggestions.extend([
            f"Review error handling for {error_type}",
            "Add additional validation steps",
            "Consider implementing retry logic"
        ])
    
    def _analyze_low_confidence(self, reflection: ReflectionLog) -> None:
        """Analyze low confidence outcomes"""
        reflection.improvement_suggestions.extend([
            "Gather additional context before processing",
            "Implement confidence threshold checks",
            "Add verification steps for uncertain outcomes"
        ])
    
    def _categorize_error(self, error: Optional[str]) -> str:
        """Categorize error types"""
        if not error:
            return "unknown"
        
        error_categories = {
            "timeout": ["timeout", "timed out", "deadline exceeded"],
            "validation": ["invalid", "validation", "schema"],
            "permission": ["permission", "unauthorized", "forbidden"],
            "not_found": ["not found", "missing", "404"],
            "rate_limit": ["rate limit", "too many requests"]
        }
        
        error_lower = error.lower()
        for category, keywords in error_categories.items():
            if any(keyword in error_lower for keyword in keywords):
                return category
        
        return "other"
    
    def _generate_improvement_suggestion(self, action: str, error: Optional[str]) -> str:
        """Generate specific improvement suggestions"""
        error_type = self._categorize_error(error)
        
        suggestions = {
            "timeout": "Implement exponential backoff retry logic",
            "validation": "Add input validation and schema checks",
            "permission": "Implement proper authentication flow",
            "not_found": "Add existence checks before operations",
            "rate_limit": "Implement rate limiting and queuing",
            "other": "Review error handling and add logging",
            "unknown": "Add comprehensive error tracking"
        }
        
        return suggestions.get(error_type, "Review and improve error handling") 