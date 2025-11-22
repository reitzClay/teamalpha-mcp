#!/usr/bin/env python3
"""
Interactive TeamAlpha Agent Client

Connect to the running TeamAlpha agent and send tasks interactively.
Supports both Ollama and LM Studio backends.
"""

import sys
import json
import os
import requests
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.teamalpha.client import TeamAlphaClient
from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole


class InteractiveClient:
    """Interactive client for TeamAlpha agents."""

    def __init__(self, server_url: str = "http://localhost:18080"):
        self.server_url = server_url
        self.client = TeamAlphaClient(server_url)
        self.team = None
        self.agents = {}
        
        print(f"🚀 TeamAlpha Interactive Client")
        print(f"📡 Connected to: {server_url}")
        print()
        
    def check_health(self) -> bool:
        """Check if agent server is healthy."""
        try:
            response = self.client.health()
            print(f"✅ Agent Status: {response}")
            return True
        except Exception as e:
            print(f"❌ Agent Error: {e}")
            return False

    def create_team(self, name: str = "Interactive Team") -> Team:
        """Create a team locally."""
        team = Team(name)
        
        # Get provider from environment
        provider = os.getenv("LLM_PROVIDER", "auto")
        lmstudio_host = os.getenv("LMSTUDIO_HOST", "http://localhost:1234")
        
        # Add standard agents
        agents_config = [
            ("Alice", AgentRole.ENGINEER, "Backend engineer"),
            ("Bob", AgentRole.REVIEWER, "Code reviewer"),
            ("Eve", AgentRole.ARCHITECT, "System architect"),
            ("Charlie", AgentRole.TESTER, "QA engineer"),
            ("Diana", AgentRole.PM, "Product manager"),
        ]
        
        for name, role, desc in agents_config:
            agent = Agent(
                name, 
                role,
                lmstudio_host=lmstudio_host,
                provider=provider
            )
            team.add_agent(agent)
            self.agents[name] = agent
        
        self.team = team
        print(f"\n👥 Team '{name}' created with {len(team.agents)} agents:")
        print(f"   Provider: {provider}")
        if provider == "lmstudio":
            print(f"   LM Studio: {lmstudio_host}")
        for agent in team.agents.values():
            print(f"   • {agent.name} ({agent.role.value})")
        return team

    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Send a prompt to the agent and get response."""
        print(f"\n💭 Sending prompt to agent...")
        try:
            response = self.client.generate(prompt, max_tokens)
            return response
        except Exception as e:
            return f"Error: {e}"

    def show_agents(self):
        """Show available agents."""
        if not self.team:
            print("❌ No team created. Run 'team create' first.")
            return
        
        print("\n👥 Available Agents:")
        for agent in self.team.agents.values():
            print(f"   • {agent.name:<10} ({agent.role.value})")

    def assign_to_agent(self, agent_name: str, task: str) -> str:
        """Assign a task to a specific agent."""
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found"
        
        agent = self.agents[agent_name]
        print(f"\n🎯 Assigning to {agent.name} ({agent.role.value}):")
        print(f"   Task: {task}\n")
        
        # Send to LLM
        response = self.generate(task)
        return response

    def list_commands(self):
        """Show available commands."""
        print("""
📚 Available Commands:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  status          - Check agent health
  team create     - Create a team with 5 agents
  agents          - List available agents
  
  generate <text> - Send prompt to LLM
                    Example: generate "Design a REST API"
  
  assign <name> <task> - Assign task to specific agent
                    Example: assign Alice "Implement login endpoint"
  
  help            - Show this help message
  exit            - Exit the client

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Examples:

  > team create
  > assign Eve "Design database schema"
  > generate "Create a user authentication system"
  > assign Bob "Review the proposed design"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)

    def interactive_loop(self):
        """Run interactive command loop."""
        print("\n📖 Type 'help' for commands or 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("teamalpha> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == "help":
                    self.list_commands()
                    continue
                
                if user_input.lower() == "status":
                    self.check_health()
                    continue
                
                if user_input.lower() == "team create":
                    self.create_team()
                    continue
                
                if user_input.lower() == "agents":
                    self.show_agents()
                    continue
                
                if user_input.lower().startswith("generate "):
                    prompt = user_input[9:].strip()
                    if not prompt:
                        print("❌ Please provide a prompt")
                        continue
                    response = self.generate(prompt)
                    print(f"\n🤖 Agent Response:\n{response}\n")
                    continue
                
                if user_input.lower().startswith("assign "):
                    parts = user_input[7:].strip().split(" ", 1)
                    if len(parts) < 2:
                        print("❌ Usage: assign <agent_name> <task>")
                        continue
                    agent_name = parts[0]
                    task = parts[1]
                    response = self.assign_to_agent(agent_name, task)
                    print(f"\n🤖 Agent Response:\n{response}\n")
                    continue
                
                print(f"❓ Unknown command: {user_input}")
                print("   Type 'help' for available commands")
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    client = InteractiveClient()
    
    # Check health first
    if not client.check_health():
        print("\n❌ Cannot connect to agent. Is the stack running?")
        print("   Start with: docker compose -f infrastructure/docker-compose.dev.yml up -d")
        sys.exit(1)
    
    # Create team by default
    client.create_team()
    
    # Show help
    client.list_commands()
    
    # Start interactive loop
    client.interactive_loop()


if __name__ == "__main__":
    main()
