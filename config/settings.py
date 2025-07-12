"""Configuration settings for the multi-agent system"""
import os
from dotenv import load_dotenv # type: ignore [reportMissingImports]

# Load environment variables from .env file
load_dotenv()

GROQ_CONFIG = {
    "api_key": os.getenv("GROQ_API_KEY"),  # Get API key from environment variable
    "model": "llama-3.3-70b-versatile",  # High-performance model with fast inference
    "temperature": 0.7,
    "max_tokens": 4000,
    "top_p": 0.95,
    "request_timeout": 45,  # Timeout in seconds
}

SYSTEM_CONFIG = {
    "research": {
        "max_retries": 2,  # Reduced for faster error recovery
        "timeout": 45,  # Adjusted timeout
        "confidence_threshold": 0.7
    },
    "planning": {
        "max_retries": 2,  # Reduced for faster error recovery
        "timeout": 45,  # Adjusted timeout
        "confidence_threshold": 0.7
    }
} 