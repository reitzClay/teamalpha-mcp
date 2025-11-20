#!/usr/bin/env python3
"""
Simple script to request a poem from the Ollama agent.
"""
from langchain_ollama import OllamaLLM

# Initialize LLM
llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")

def request_poem():
    """Request a poem from the LLM."""
    
    prompt = "Write a short, creative poem about the beauty of autumn. Make it at least 8 lines."
    
    print("\n" + "="*80)
    print("POEM REQUEST")
    print("="*80)
    print(f"\nPrompt: {prompt}\n")
    print("-" * 80)
    print("Agent Response:")
    print("-" * 80 + "\n")
    
    try:
        response = llm.invoke(prompt)
        print(response)
        print("\n" + "-" * 80)
        print("✓ Poem generated successfully!")
        print("="*80 + "\n")
        return response
    except Exception as e:
        print(f"✗ Error: {e}")
        print("="*80 + "\n")
        return None

if __name__ == "__main__":
    request_poem()
