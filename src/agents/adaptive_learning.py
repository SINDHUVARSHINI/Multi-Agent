from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field # type: ignore
import time
import json
from pathlib import Path

class LearningExample(BaseModel):
    """Model for storing learning examples"""
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    performance_metrics: Dict[str, float]
    timestamp: float
    tags: List[str] = Field(default_factory=list)

class AdaptiveLearningMixin:
    """Mixin to add adaptive learning capabilities to agents"""
    
    def __init__(self, learning_path: str = "data/learning"):
        self.learning_path = Path(learning_path)
        self.learning_path.mkdir(parents=True, exist_ok=True)
        self.examples: List[LearningExample] = self._load_examples()
        self.performance_threshold = 0.7
        self.adaptation_rate = 0.1
    
    def _load_examples(self) -> List[LearningExample]:
        """Load learning examples from disk"""
        examples = []
        if (self.learning_path / "examples.json").exists():
            with open(self.learning_path / "examples.json", "r") as f:
                data = json.load(f)
                for item in data:
                    examples.append(LearningExample(**item))
        return examples
    
    def _save_examples(self) -> None:
        """Save learning examples to disk"""
        with open(self.learning_path / "examples.json", "w") as f:
            json.dump([example.dict() for example in self.examples], f, indent=2)
    
    def add_learning_example(self, input_data: Dict[str, Any], output_data: Dict[str, Any], 
                           performance_metrics: Dict[str, float], tags: List[str]) -> None:
        """Add a new learning example"""
        example = LearningExample(
            input_data=input_data,
            output_data=output_data,
            performance_metrics=performance_metrics,
            timestamp=time.time(),
            tags=tags
        )
        self.examples.append(example)
        self._save_examples()
        self._adapt_to_new_example(example)
    
    def _adapt_to_new_example(self, example: LearningExample) -> None:
        """Adapt agent behavior based on new example"""
        # Update performance threshold
        avg_performance = sum(example.performance_metrics.values()) / len(example.performance_metrics)
        if avg_performance > self.performance_threshold:
            self.performance_threshold = (1 - self.adaptation_rate) * self.performance_threshold + \
                                      self.adaptation_rate * avg_performance
    
    def find_similar_examples(self, query: Dict[str, Any], top_k: int = 3) -> List[Tuple[LearningExample, float]]:
        """Find similar examples to the query"""
        if not self.examples:
            return []
        
        similarities = []
        for example in self.examples:
            similarity = self._calculate_similarity(query, example.input_data)
            similarities.append((example, similarity))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _calculate_similarity(self, query: Dict[str, Any], example_input: Dict[str, Any]) -> float:
        """Calculate similarity between query and example"""
        # Simple similarity based on shared keys and values
        shared_keys = set(query.keys()) & set(example_input.keys())
        if not shared_keys:
            return 0.0
        
        similarity_score = 0.0
        for key in shared_keys:
            if query[key] == example_input[key]:
                similarity_score += 1.0
        
        return similarity_score / len(shared_keys)
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        if not self.examples:
            return {"average_performance": 0.0, "improvement_rate": 0.0}
        
        # Calculate average performance over time
        performances = []
        for example in self.examples:
            avg_perf = sum(example.performance_metrics.values()) / len(example.performance_metrics)
            performances.append(avg_perf)
        
        # Calculate improvement rate
        if len(performances) > 1:
            improvement_rate = (performances[-1] - performances[0]) / len(performances)
        else:
            improvement_rate = 0.0
        
        return {
            "average_performance": sum(performances) / len(performances),
            "improvement_rate": improvement_rate
        }
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights about learning progress"""
        if not self.examples:
            return {"status": "No learning examples available"}
        
        # Analyze performance trends
        performance_stats = self.get_performance_stats()
        
        # Analyze common patterns in successful examples
        successful_examples = [ex for ex in self.examples 
                             if sum(ex.performance_metrics.values()) / len(ex.performance_metrics) 
                             > self.performance_threshold]
        
        # Extract common tags
        all_tags = {}
        for example in successful_examples:
            for tag in example.tags:
                all_tags[tag] = all_tags.get(tag, 0) + 1
        
        return {
            "performance_stats": performance_stats,
            "successful_patterns": {
                "count": len(successful_examples),
                "common_tags": dict(sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:5])
            },
            "adaptation_metrics": {
                "performance_threshold": self.performance_threshold,
                "adaptation_rate": self.adaptation_rate
            }
        } 