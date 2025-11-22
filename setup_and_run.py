#!/usr/bin/env python3
"""
Setup script to prepare the environment and run interactive client.
Waits for Ollama model to be available before starting client.
"""

import sys
import time
import requests
from pathlib import Path

def wait_for_model(max_wait: int = 300) -> bool:
    """Wait for Ollama model to be available."""
    print("⏳ Waiting for Ollama model to be available...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get("http://localhost:11435/api/tags")
            models = response.json().get("models", [])
            if models:
                print(f"✅ Model ready: {models[0]['name']}")
                return True
        except:
            pass
        
        elapsed = int(time.time() - start_time)
        remaining = max_wait - elapsed
        print(f"   [{elapsed}s / {max_wait}s] Checking model status...", end='\r')
        time.sleep(5)
    
    print(f"\n❌ Timeout waiting for model (after {max_wait}s)")
    return False


def wait_for_agent(max_wait: int = 30) -> bool:
    """Wait for agent server to be responsive."""
    print("⏳ Waiting for agent server...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get("http://localhost:18080/health")
            if response.status_code == 200:
                print(f"✅ Agent server ready")
                return True
        except:
            pass
        
        time.sleep(1)
    
    print(f"❌ Agent server not responding")
    return False


def main():
    """Main setup and launch."""
    print("🚀 TeamAlpha Setup\n")
    
    # Check dependencies
    print("📦 Checking environment...")
    try:
        import requests
        print("   ✅ requests")
    except ImportError:
        print("   ❌ requests module not found")
        sys.exit(1)
    
    # Wait for agent
    if not wait_for_agent():
        print("\n❌ Cannot connect to agent server.")
        print("   Start with: docker compose -f infrastructure/docker-compose.dev.yml up -d")
        sys.exit(1)
    
    # Wait for Ollama model
    if not wait_for_model():
        print("\n⚠️  Model not ready yet, but agent is responsive.")
        print("   You can still run commands, but LLM generation will fail until model loads.")
        response = input("   Continue anyway? (y/n): ")
        if response.lower() != "y":
            sys.exit(1)
    
    print("\n✨ All systems ready!\n")
    
    # Import and run client
    sys.path.insert(0, str(Path(__file__).parent))
    from interactive_client import InteractiveClient
    
    client = InteractiveClient()
    client.interactive_loop()


if __name__ == "__main__":
    main()
