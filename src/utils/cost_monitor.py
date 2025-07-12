"""Utility for monitoring Groq API costs"""
from typing import Dict, Optional
import json
import os
from datetime import datetime

class CostMonitor:
    def __init__(self, log_file: str = "api_costs.json"):
        self.log_file = log_file
        self.cost_per_1k_tokens = {
            "llama-3.3-70b-versatile": {
                "input": 0.0007,   # $0.0007 per 1K input tokens
                "output": 0.0007   # $0.0007 per 1K output tokens
            },
            "llama3-8b-8192": {
                "input": 0.0001,   # $0.0001 per 1K input tokens
                "output": 0.0001   # $0.0001 per 1K output tokens
            }
        }
        self._load_or_create_log()

    def _load_or_create_log(self) -> None:
        """Load existing cost log or create new one"""
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.cost_log = json.load(f)
        else:
            self.cost_log = {
                "total_cost": 0.0,
                "requests": []
            }

    def _save_log(self) -> None:
        """Save cost log to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.cost_log, f, indent=2)

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a single API request"""
        if model not in self.cost_per_1k_tokens:
            raise ValueError(f"Unknown model: {model}")
        
        rates = self.cost_per_1k_tokens[model]
        input_cost = (input_tokens / 1000) * rates["input"]
        output_cost = (output_tokens / 1000) * rates["output"]
        return input_cost + output_cost

    def log_request(self, model: str, input_tokens: int, output_tokens: int, 
                   success: bool, error: Optional[str] = None) -> None:
        """Log an API request with its cost and details"""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        request_log = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "success": success
        }
        
        if error:
            request_log["error"] = error

        self.cost_log["requests"].append(request_log)
        self.cost_log["total_cost"] += cost
        self._save_log()

    def get_total_cost(self) -> float:
        """Get total cost of all API requests"""
        return self.cost_log["total_cost"]

    def get_cost_summary(self) -> Dict:
        """Get summary of API usage and costs"""
        summary = {
            "total_cost": self.cost_log["total_cost"],
            "total_requests": len(self.cost_log["requests"]),
            "successful_requests": sum(1 for r in self.cost_log["requests"] if r["success"]),
            "failed_requests": sum(1 for r in self.cost_log["requests"] if not r["success"]),
            "costs_by_model": {}
        }

        # Calculate costs per model
        for model in self.cost_per_1k_tokens.keys():
            model_requests = [r for r in self.cost_log["requests"] if r["model"] == model]
            if model_requests:
                summary["costs_by_model"][model] = {
                    "total_cost": sum(r["cost"] for r in model_requests),
                    "request_count": len(model_requests),
                    "total_input_tokens": sum(r["input_tokens"] for r in model_requests),
                    "total_output_tokens": sum(r["output_tokens"] for r in model_requests)
                }

        return summary

    def print_summary(self) -> None:
        """Print a formatted summary of API usage and costs"""
        summary = self.get_cost_summary()
        
        print("\n=== Groq API Cost Summary ===")
        print(f"Total Cost: ${summary['total_cost']:.4f}")
        print(f"Total Requests: {summary['total_requests']}")
        print(f"Successful Requests: {summary['successful_requests']}")
        print(f"Failed Requests: {summary['failed_requests']}")
        
        print("\nCosts by Model:")
        for model, data in summary["costs_by_model"].items():
            print(f"\n{model}:")
            print(f"  Total Cost: ${data['total_cost']:.4f}")
            print(f"  Requests: {data['request_count']}")
            print(f"  Input Tokens: {data['total_input_tokens']}")
            print(f"  Output Tokens: {data['total_output_tokens']}") 