from setuptools import setup, find_packages

setup(
    name="assembleai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain==0.1.12",
        "langchain-community>=0.0.28",  # Added for HuggingFace support
        "langchain-groq>=0.0.3",  # Added for Groq support
        "groq>=0.3.2",
        "pydantic==2.6.4",
        "python-dotenv==1.0.1",
        "typing-extensions==4.10.0",
        "aiohttp==3.10.5",
        "nest-asyncio==1.5.8",
        "transformers>=4.37.0",
        "torch>=2.2.0",
        "accelerate>=0.27.0",
    ],
    python_requires=">=3.8",
) 