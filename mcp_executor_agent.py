#!/usr/bin/env python3
"""
MCP Agent with Tool Execution
This agent can actually execute tools when instructed by the LLM.
"""
import json
import os
import re
from langchain_ollama import OllamaLLM


class GitHubMCPClient:
    """Wrapper around MCP GitHub server."""
    
    def __init__(self):
        self.api_base = "https://api.github.com"
    
    def get_repository_readme(self, owner: str, repo: str) -> str:
        """Fetch README from a GitHub repository using requests."""
        try:
            import requests
            
            url = f"{self.api_base}/repos/{owner}/{repo}/readme"
            headers = {"Accept": "application/vnd.github.v3.raw"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.text[:2000]  # First 2000 chars
            else:
                return f"Error fetching README: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def search_repositories(self, query: str, limit: int = 5) -> str:
        """Search for repositories on GitHub."""
        try:
            import requests
            
            params = {"q": query, "per_page": limit}
            response = requests.get(f"{self.api_base}/search/repositories", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                repos = []
                for repo in data.get("items", [])[:limit]:
                    repos.append({
                        "name": repo["full_name"],
                        "description": repo["description"],
                        "url": repo["html_url"],
                        "stars": repo["stargazers_count"]
                    })
                return json.dumps(repos, indent=2)
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"


class FilesystemMCPClient:
    """Wrapper around MCP Filesystem server."""
    
    def read_file(self, path: str) -> str:
        """Read a file with safety checks."""
        try:
            if ".." in path or path.startswith("/"):
                return "Error: Path traversal not allowed. Use relative paths."
            
            if not os.path.exists(path):
                return f"File not found: {path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 1500:
                return content[:1500] + f"\n\n... (truncated, {len(content)} total chars)"
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def list_directory(self, path: str = ".") -> str:
        """List directory contents."""
        try:
            if not os.path.isdir(path):
                return f"Not a directory: {path}"
            
            items = os.listdir(path)
            dirs = [d for d in items if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
            files = [f for f in items if os.path.isfile(os.path.join(path, f)) and not f.startswith('.')]
            
            result = f"📁 Directory: {path}\n\n📂 Folders:\n"
            result += "\n".join(f"  - {d}/" for d in sorted(dirs)[:20])
            result += f"\n\n📄 Files:\n"
            result += "\n".join(f"  - {f}" for f in sorted(files)[:20])
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"


# Initialize clients
github_client = GitHubMCPClient()
filesystem_client = FilesystemMCPClient()


class ToolExecutor:
    """Executes MCP tools based on LLM instructions."""
    
    def __init__(self):
        self.tools = {
            "github_get_readme": github_client.get_repository_readme,
            "github_search_repos": github_client.search_repositories,
            "fs_read_file": filesystem_client.read_file,
            "fs_list_directory": filesystem_client.list_directory,
        }
    
    def extract_tool_calls(self, text: str) -> list:
        """Extract tool calls from LLM response text."""
        # Look for patterns like: tool_name("arg1", "arg2")
        pattern = r'(\w+)\(\s*"([^"]*)"\s*(?:,\s*"([^"]*)")?\s*\)'
        matches = re.findall(pattern, text)
        
        tool_calls = []
        for match in matches:
            tool_name = match[0]
            arg1 = match[1]
            arg2 = match[2] if match[2] else None
            
            if tool_name in self.tools:
                tool_calls.append({
                    "tool": tool_name,
                    "args": [arg1, arg2] if arg2 else [arg1]
                })
        
        return tool_calls
    
    def execute_tool(self, tool_name: str, args: list) -> str:
        """Execute a specific tool."""
        if tool_name not in self.tools:
            return f"Tool not found: {tool_name}"
        
        try:
            tool_func = self.tools[tool_name]
            if len(args) == 1:
                return tool_func(args[0])
            elif len(args) == 2:
                return tool_func(args[0], args[1])
            else:
                return f"Invalid number of arguments for {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def execute_all(self, text: str) -> dict:
        """Execute all tool calls found in text."""
        tool_calls = self.extract_tool_calls(text)
        results = {}
        
        for call in tool_calls:
            tool_name = call["tool"]
            result = self.execute_tool(tool_name, call["args"])
            results[tool_name] = result
        
        return results


class MCPExecutorAgent:
    """Agent that can execute MCP tools."""
    
    def __init__(self):
        self.llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
        self.executor = ToolExecutor()
        self.conversation_history = []
    
    def run_query(self, query: str, max_iterations: int = 2) -> str:
        """Run a query with tool execution."""
        print("\n" + "="*80)
        print("🤖 MCP Agent with Tool Execution")
        print("="*80)
        print(f"\n📋 Query: {query}\n")
        
        system_prompt = """You are an AI assistant with access to MCP tools:
        
Tools available:
- fs_list_directory("path"): List directory contents
- fs_read_file("path"): Read file contents
- github_search_repos("query"): Search GitHub repos
- github_get_readme("owner", "repo"): Get repo README

When you need to use tools, call them directly in your response like:
fs_list_directory(".")
github_search_repos("crewai")

I will execute these tools and show you the results."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        for iteration in range(max_iterations):
            print(f"🔄 Iteration {iteration + 1}/{max_iterations}\n")
            
            # Get LLM response
            prompt = f"{query}\n\nPlease respond and use tools if needed."
            response = self.llm.invoke(prompt)
            print(f"Agent: {response}\n")
            
            # Extract and execute tools
            tool_results = self.executor.execute_all(response)
            
            if tool_results:
                print("-" * 80)
                print("🔧 Tool Results:\n")
                for tool_name, result in tool_results.items():
                    print(f"{tool_name}:")
                    print(f"{result}\n")
                print("-" * 80 + "\n")
            else:
                # No more tools to execute
                break
        
        print("="*80 + "\n")
        return response


def main():
    """Run the agent with tool execution."""
    agent = MCPExecutorAgent()
    
    queries = [
        "What's in the /app directory? List it for me.",
        "Search GitHub for 'crewai' and show me the top results",
        "Read the pyproject.toml file and tell me what it contains",
    ]
    
    for query in queries[:2]:
        agent.run_query(query)
        print("\n" + "─"*80 + "\n")


if __name__ == "__main__":
    main()
