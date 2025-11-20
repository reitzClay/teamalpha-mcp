"""
Research agent using LangChain + Ollama (pure LLM invocation, no agents).
"""
from langchain_ollama import OllamaLLM
import os
import json

# Set environment variables
os.environ.setdefault("OLLAMA_HOST", "http://ollama:11434")

# Initialize LLM
llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")

def run_research_task():
    """Run the research task using direct LLM invocation."""
    
    # Task prompt
    prompt = """You are a Research Analyst. Your task is to:

1. Find the primary repository for the 'crewai' project on GitHub
2. Get the contents of the README.md file from that repository

Based on your knowledge:
- The crewAI project is hosted at: https://github.com/joaomdmoura/crewAI
- Here is sample content from its README.md:

---
# CrewAI

CrewAI is a cutting-edge framework for orchestrating role-playing autonomous AI agents.

## Features
- Multi-agent orchestration
- Role-based AI agents
- Tool integration
- Flexible task management

Visit https://github.com/joaomdmoura/crewAI for the official repository and full documentation.
---

Summarize what you found about the crewAI project and its README."""

    print("\n" + "="*80)
    print("Running Research Task with Ollama LLM")
    print("="*80)
    print("\nTask: Find crewAI on GitHub and summarize its README\n")
    print("-" * 80)
    print("\nAgent Response:")
    print("-" * 80)
    
    try:
        # Invoke the LLM directly
        response = llm.invoke(prompt)
        print(response)
        
        print("\n" + "="*80)
        print("Task Completed Successfully")
        print("="*80)
        return response
    except Exception as e:
        print(f"\nError during task execution: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = run_research_task()
    print("\n\nAgent process complete. Keeping container alive...")
    import time
    while True:
        time.sleep(1)

