#!/usr/bin/env python3
"""
LM Studio Connection Test & Setup for TeamAlpha

Tests connection to LM Studio and verifies the gpt-oss-20b model is available.
"""

import sys
import requests
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.teamalpha.lmstudio import LMStudioClient
from src.teamalpha.agent import Agent, AgentRole


def test_lmstudio_connection(host: str = "http://10.5.0.2:1234") -> bool:
    """Test if LM Studio is running and accessible."""
    print(f"🔍 Testing LM Studio connection at {host}...")
    
    try:
        response = requests.get(f"{host}/health", timeout=5)
        if response.ok:
            print(f"✅ LM Studio is running")
            return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to LM Studio at {host}")
        print(f"   Make sure LM Studio is running on {host}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def list_models(host: str = "http://10.5.0.2:1234") -> list:
    """List available models in LM Studio."""
    print(f"\n📦 Available models in LM Studio:")
    
    try:
        client = LMStudioClient(base_url=host)
        models = client.list_models()
        
        if models:
            for model in models:
                model_id = model.get("id", "unknown")
                print(f"   • {model_id}")
            return models
        else:
            print("   No models found (load one in LM Studio first)")
            return []
    except Exception as e:
        print(f"   Error: {e}")
        return []


def test_generation(host: str = "http://10.5.0.2:1234") -> bool:
    """Test generating text with LM Studio."""
    print(f"\n🧪 Testing text generation...")
    
    try:
        client = LMStudioClient(base_url=host)
        response = client.generate(
            "What is machine learning? Answer in one sentence.",
            max_tokens=100
        )
        
        if response:
            print(f"✅ Generation successful")
            print(f"\n📝 Sample output:\n{response[:200]}...\n")
            return True
        else:
            print(f"❌ Generation returned empty response")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_with_agent(host: str = "http://10.5.0.2:1234") -> bool:
    """Test agent connection to LM Studio."""
    print(f"\n🤖 Testing agent with LM Studio...")
    
    try:
        # Create an agent with LM Studio
        agent = Agent(
            name="TestAgent",
            role=AgentRole.ENGINEER,
            lmstudio_host=host,
            provider="lmstudio"
        )
        
        print(f"✅ Agent created: {agent.name} ({agent.role.value})")
        
        # Test thinking
        print(f"💭 Agent thinking...")
        response = agent.think("What is a REST API?")
        
        if response:
            print(f"✅ Agent response received")
            print(f"\n📝 Agent output:\n{response[:300]}...\n")
            return True
        else:
            print(f"❌ Agent returned empty response")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def setup_team(host: str = "http://10.5.0.2:1234") -> bool:
    """Create a team with LM Studio backend."""
    print(f"\n👥 Creating team with LM Studio backend...\n")
    
    try:
        agents_config = [
            ("Alice", AgentRole.ENGINEER),
            ("Bob", AgentRole.REVIEWER),
            ("Eve", AgentRole.ARCHITECT),
        ]
        
        agents = []
        for name, role in agents_config:
            agent = Agent(
                name=name,
                role=role,
                lmstudio_host=host,
                provider="lmstudio"
            )
            agents.append(agent)
            print(f"✅ Created: {agent.name} ({agent.role.value})")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main test routine."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LM Studio connection")
    parser.add_argument(
        "--host",
        default="http://10.5.0.2:1234",
        help="LM Studio host (default: http://10.5.0.2:1234)"
    )
    parser.add_argument(
        "--test-generation",
        action="store_true",
        help="Test text generation"
    )
    parser.add_argument(
        "--test-agent",
        action="store_true",
        help="Test agent with LM Studio"
    )
    parser.add_argument(
        "--create-team",
        action="store_true",
        help="Create a team with LM Studio"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🚀 LM Studio Connection Test for TeamAlpha")
    print("=" * 70)
    print()
    
    # Test connection
    if not test_lmstudio_connection(args.host):
        print("\n❌ Cannot connect to LM Studio. Exiting.")
        sys.exit(1)
    
    # List models
    list_models(args.host)
    
    # Run tests
    if args.test_generation or args.all:
        test_generation(args.host)
    
    if args.test_agent or args.all:
        test_with_agent(args.host)
    
    if args.create_team or args.all:
        setup_team(args.host)
    
    print("\n" + "=" * 70)
    print("✅ LM Studio is ready for use with TeamAlpha!")
    print("=" * 70)


if __name__ == "__main__":
    main()
