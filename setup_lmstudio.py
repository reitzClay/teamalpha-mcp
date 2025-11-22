#!/usr/bin/env python3
"""
LM Studio Quick Start for TeamAlpha

One-command setup to connect your fleet agents to LM Studio.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  TeamAlpha + LM Studio Integration                         ║
║                     Connect Your Agent Fleet to LM Studio                  ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)


def check_lmstudio():
    """Check if LM Studio is running."""
    print("🔍 Checking for LM Studio...")
    
    try:
        import requests
        response = requests.get("http://10.5.0.2:1234/health", timeout=2)
        if response.ok:
            print("✅ LM Studio is running on http://10.5.0.2:1234")
            return True
    except:
        pass
    
    print("❌ LM Studio not found")
    print("\n📋 To use LM Studio with TeamAlpha:")
    print("   1. Start LM Studio on Windows")
    print("   2. Load model: gpt-oss-20b-GGUF")
    print("   3. Run this script again")
    return False


def list_lmstudio_models():
    """List models available in LM Studio."""
    try:
        import requests
        response = requests.get("http://10.5.0.2:1234/v1/models", timeout=5)
        if response.ok:
            models = response.json().get("data", [])
            if models:
                print("\n📦 Loaded models:")
                for model in models:
                    print(f"   • {model.get('id', 'unknown')}")
                return models
    except:
        pass
    
    print("\n⚠️  No models loaded in LM Studio")
    print("   Load gpt-oss-20b-GGUF in LM Studio to continue")
    return []


def setup_environment():
    """Setup environment variables."""
    print("\n🔧 Setting environment for LM Studio...")
    
    os.environ["LLM_PROVIDER"] = "lmstudio"
    os.environ["LMSTUDIO_HOST"] = "http://10.5.0.2:1234"
    
    print("✅ Environment configured:")
    print(f"   LLM_PROVIDER={os.environ['LLM_PROVIDER']}")
    print(f"   LMSTUDIO_HOST={os.environ['LMSTUDIO_HOST']}")


def test_connection():
    """Test agent connection to LM Studio."""
    print("\n🧪 Testing agent connection...")
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from src.teamalpha.agent import Agent, AgentRole
        
        # Set environment
        os.environ["LLM_PROVIDER"] = "lmstudio"
        
        # Create test agent
        print("   Creating test agent...")
        agent = Agent(
            name="TestAlice",
            role=AgentRole.ENGINEER,
            provider="lmstudio"
        )
        print(f"   ✅ Agent created: {agent}")
        
        # Quick test
        print("   Sending test prompt...")
        response = agent.think("What is AI? Answer in one sentence.")
        
        if response and len(response) > 10:
            print("✅ Connection successful!")
            print(f"\n📝 Sample output:\n{response[:150]}...\n")
            return True
        else:
            print("❌ Empty response from agent")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def start_interactive_client():
    """Start the interactive client with LM Studio."""
    print("\n🚀 Starting interactive client with LM Studio...\n")
    
    # Set environment
    os.environ["LLM_PROVIDER"] = "lmstudio"
    os.environ["LMSTUDIO_HOST"] = "http://10.5.0.2:1234"
    
    # Run client
    script_path = Path(__file__).parent / "interactive_client.py"
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python3"
    
    if venv_python.exists():
        subprocess.run([str(venv_python), str(script_path)])
    else:
        subprocess.run([sys.executable, str(script_path)])


def main():
    """Main setup routine."""
    print_banner()
    
    # Check LM Studio
    if not check_lmstudio():
        print("\n💡 Next steps:")
        print("   1. Start LM Studio")
        print("   2. Load gpt-oss-20b-GGUF model")
        print("   3. Run: python3 setup_lmstudio.py")
        sys.exit(1)
    
    # List models
    models = list_lmstudio_models()
    if not models:
        print("\n💡 Next steps:")
        print("   1. Load a model in LM Studio (gpt-oss-20b-GGUF recommended)")
        print("   2. Run: python3 setup_lmstudio.py")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Test connection
    if not test_connection():
        print("❌ Connection test failed")
        sys.exit(1)
    
    # Start client
    print("\n" + "=" * 76)
    print("✅ LM Studio is ready! Starting interactive client...")
    print("=" * 76)
    
    response = input("\nStart interactive client? (y/n): ")
    if response.lower() == "y":
        start_interactive_client()
    else:
        print("\n💡 To start later, run:")
        print("   LMSTUDIO_HOST=http://10.5.0.2:1234 LLM_PROVIDER=lmstudio ./run-client.sh")


if __name__ == "__main__":
    main()
