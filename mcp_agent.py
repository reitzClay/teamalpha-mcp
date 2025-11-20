#!/usr/bin/env python3
"""
Agent with MCP (Model Context Protocol) server integration.
Uses Python MCP SDK to connect to external tools like GitHub, filesystem, web search.
"""
import json
import asyncio
import subprocess
import sys
from typing import Any
from langchain_ollama import OllamaLLM

# We'll implement MCP client integration
# First, let's define a tool wrapper for MCP servers

class MCPToolWrapper:
    """Wrapper to connect MCP servers to the agent."""
    
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.tools = {}
    
    async def start_server(self):
        """Start the MCP server as a subprocess."""
        try:
            # Try to start the server using uvx (fast Python exec)
            self.process = await asyncio.create_subprocess_exec(
                "uvx", f"mcp-server-{self.server_name}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            print(f"✓ Started MCP server: {self.server_name}")
        except Exception as e:
            print(f"✗ Failed to start {self.server_name} server: {e}")
            raise
    
    async def stop_server(self):
        """Stop the MCP server."""
        if hasattr(self, 'process'):
            self.process.terminate()
            await self.process.wait()

class MCPAgent:
    """AI Agent with MCP tool integration."""
    
    def __init__(self):
        self.llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
        self.servers = {}
        self.available_tools = []
    
    async def register_mcp_server(self, server_name: str):
        """Register an MCP server for this agent."""
        wrapper = MCPToolWrapper(server_name)
        try:
            await wrapper.start_server()
            self.servers[server_name] = wrapper
            print(f"Registered MCP server: {server_name}")
        except Exception as e:
            print(f"Could not register {server_name}: {e}")
    
    def list_available_tools(self) -> str:
        """Return list of available tools from MCP servers."""
        tools_info = """
Available Tools:
================

1. Filesystem Tools (from mcp-server-filesystem):
   - read_file(path): Read file contents
   - write_file(path, contents): Write to a file
   - list_directory(path): List directory contents
   - search_files(pattern): Search for files

2. GitHub Tools (from mcp-server-github):
   - get_repository_readme(owner, repo): Fetch README from repo
   - search_repositories(query): Search GitHub repos
   - get_issues(owner, repo): Get issues from a repository
   - get_pull_requests(owner, repo): Get PRs from a repository

3. Git Tools (from mcp-server-git):
   - get_repository_status(): Get repo status
   - get_commits(branch): Get commit history
   - show_file_at_revision(path, revision): Get file at specific revision

4. Web Search Tools:
   - search_web(query): Search the web
   - fetch_webpage(url): Get webpage contents

Note: Tools become available after registering their MCP servers.
"""
        return tools_info
    
    def create_system_prompt(self) -> str:
        """Create a system prompt that tells the agent about available tools."""
        tools_list = self.list_available_tools()
        
        prompt = f"""You are an AI Agent with access to the following tools via MCP (Model Context Protocol):

{tools_list}

When responding to requests:
1. Use tools from MCP servers to gather real information
2. For GitHub queries, use the GitHub MCP server to fetch actual data
3. For file operations, use the Filesystem MCP server
4. Always cite your sources and explain what tools you used

Current available MCP servers: {list(self.servers.keys())}
"""
        return prompt
    
    async def ask_with_tools(self, query: str) -> str:
        """Ask the agent a question, giving it access to MCP tools."""
        
        system_prompt = self.create_system_prompt()
        
        # Combine system prompt with user query
        full_prompt = f"""{system_prompt}

User Query: {query}

Please answer the query using available tools if needed. If a tool can help, mention which tool you would use and what it would return."""
        
        print("\n" + "="*80)
        print("MCP-Enabled Agent Query")
        print("="*80)
        print(f"\nQuery: {query}\n")
        print("-" * 80)
        print("Agent Response:")
        print("-" * 80 + "\n")
        
        try:
            response = self.llm.invoke(full_prompt)
            print(response)
            print("\n" + "-" * 80)
            return response
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            return error_msg
    
    async def cleanup(self):
        """Stop all MCP servers."""
        for server_name, wrapper in self.servers.items():
            print(f"Stopping {server_name} server...")
            await wrapper.stop_server()


async def main():
    """Demonstrate MCP-integrated agent."""
    
    agent = MCPAgent()
    
    # Try to register MCP servers (these may not be installed yet)
    print("Initializing MCP-Enabled Agent...")
    print("="*80 + "\n")
    
    servers_to_try = ["filesystem", "git"]
    for server in servers_to_try:
        print(f"Attempting to register {server}...", end=" ")
        try:
            # We'll skip actual registration for now since servers may not be installed
            # Just simulate it
            agent.servers[server] = MCPToolWrapper(server)
            print("✓ (simulated)")
        except Exception as e:
            print(f"✗ ({e})")
    
    # Demo queries
    queries = [
        "What MCP servers would I need to fetch the crewAI README from GitHub?",
        "How would I use filesystem tools to read a local Python file and analyze it?",
    ]
    
    for query in queries:
        response = await agent.ask_with_tools(query)
        print()
    
    await agent.cleanup()
    print("\nAgent session ended.")


if __name__ == "__main__":
    asyncio.run(main())
