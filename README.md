# AssembleAI

A powerful multi-agent AI system where specialized agents work together to solve complex problems efficiently. Leveraging Groq's ultra-fast inference capabilities for lightning-quick responses.

## Overview

AssembleAI combines specialized AI agents, each with a specific role in the problem-solving process. Like a well-coordinated team of experts, they work together to achieve what would be impossible alone.

- **Task Manager**: The orchestrator who coordinates the entire workflow
- **Research Agent**: The analyst who gathers and processes information
- **Planning Agent**: The strategist who creates detailed execution plans
- **Adaptive Learning Agent**: The learner who improves from experience
- **Reflection Agent**: The evaluator who ensures continuous improvement

## Key Features

- **Ultra-Fast Processing**: Powered by Groq's `llama-3.3-70b-versatile` model
- **Efficient Collaboration**: Seamless coordination between specialized agents
- **Smart Task Distribution**: Automatic task delegation based on agent expertise
- **Adaptive Learning**: System improves from past experiences
- **Reflection Capabilities**: Built-in self-evaluation and improvement
- **Cost-Efficient**: Optimized for Groq's competitive pricing ($0.0007/1K tokens)
- **Rate-Limited Design**: Respects Groq's limits (30 RPM, 1000 RPD)

## Quick Start

1. Set up your environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
# Create a .env file with:
GROQ_API_KEY=your_api_key_here
```

4. Basic usage:
```python
from src.main import setup_agents, process_task

# Initialize the system
agents = setup_agents()

# Example task
task = {
    "description": "Research and plan implementation for a weather API integration"
}

# Process the task
result = await process_task(task, agents)
```

## Project Structure

```
AssembleAI/
├── src/
│   ├── agents/          # Specialized agent implementations
│   │   ├── adaptive_learning.py   # Learning capabilities
│   │   ├── reflection_mixin.py    # Self-improvement features
│   │   └── ...
│   ├── tools/          # Shared tools and utilities
│   ├── memory/         # Shared memory system
│   └── utils/          # Helper functions
├── config/             # Configuration files
├── tests/             # Test cases
└── examples/          # Usage examples
```

## Technologies Used

- **LangChain**: For agent orchestration and chaining
- **Groq**: Ultra-fast LLM inference with `llama-3.3-70b-versatile`
- **Async Operations**: For optimal performance
- **Adaptive Learning**: Custom implementation for continuous improvement
- **Cost Monitoring**: Built-in usage tracking and optimization

## Advanced Features

### Adaptive Learning
- Learns from past interactions
- Improves response quality over time
- Maintains a performance metrics database

### Reflection System
- Self-evaluates performance
- Identifies improvement areas
- Suggests optimization strategies

### Cost Management
- Tracks token usage
- Monitors API costs
- Optimizes for efficiency

## Performance

- **Processing Speed**: Leverages Groq's ultra-fast inference
- **Cost Efficiency**: Optimized token usage
- **Quality Assurance**: Built-in validation at every step
- **Scalability**: Designed for high-throughput operations

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.

---
*"Assembling AI Agents at the Speed of Groq!"*