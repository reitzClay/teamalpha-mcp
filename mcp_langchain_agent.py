#!/usr/bin/env python3
"""
Practical MCP Integration Demo
Shows how to connect MCP servers to LangChain as callable tools.
"""
import json
import subprocess
import os
from typing import Optional
from langchain_ollama import OllamaLLM


# ============================================================================
# MCP Tool Implementations (Simulated for Demo)
# ============================================================================

class GitHubMCPClient:
    """Wrapper around MCP GitHub server."""
    
    def __init__(self):
        self.api_base = "https://api.github.com"
        self.session = None
    
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
            # Prevent path traversal
            if ".." in path or path.startswith("/"):
                return "Error: Path traversal not allowed. Use relative paths."
            
            if not os.path.exists(path):
                return f"File not found: {path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Return first 1500 chars if file is large
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
            
            result = f"Directory: {path}\n\nFolders:\n"
            result += "\n".join(f"  - {d}/" for d in sorted(dirs)[:20])
            result += f"\n\nFiles:\n"
            result += "\n".join(f"  - {f}" for f in sorted(files)[:20])
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"


# Initialize MCP clients
github_client = GitHubMCPClient()
filesystem_client = FilesystemMCPClient()


# ============================================================================
# MCP Tool Registration (Functions as Tools)
# ============================================================================

def github_get_readme(owner: str, repo: str) -> str:
    """Fetch the README from a GitHub repository. Use this to get documentation."""
    return github_client.get_repository_readme(owner, repo)


def github_search_repos(query: str) -> str:
    """Search for repositories on GitHub by keyword or query."""
    return github_client.search_repositories(query)


def fs_read_file(path: str) -> str:
    """Read the contents of a file from the local filesystem."""
    return filesystem_client.read_file(path)


def fs_list_directory(path: str = ".") -> str:
    """List contents of a directory."""
    return filesystem_client.list_directory(path)


# ============================================================================
# MCP Agent with LangChain (Simple Tool-Based)
# ============================================================================

class MCPLangChainAgent:
    """AI Agent that uses MCP tools with LangChain."""
    
    def __init__(self):
        self.llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
        
        # Define available tools with their descriptions
        self.tools_registry = {
            "github_get_readme": {
                "func": github_get_readme,
                "description": "Fetch README file from a GitHub repository",
                "params": "owner (str), repo (str)"
            },
            "github_search_repos": {
                "func": github_search_repos,
                "description": "Search for repositories on GitHub",
                "params": "query (str)"
            },
            "fs_read_file": {
                "func": fs_read_file,
                "description": "Read contents of a local file",
                "params": "path (str)"
            },
            "fs_list_directory": {
                "func": fs_list_directory,
                "description": "List contents of a directory",
                "params": "path (str)"
            },
        }
    
    def format_tools_prompt(self) -> str:
        """Format available tools for the LLM."""
        tools_text = "Available MCP Tools:\n\n"
        for name, info in self.tools_registry.items():
            tools_text += f"- {name}({info['params']}): {info['description']}\n"
        return tools_text
    
    def ask(self, query: str) -> str:
        """Ask the agent a question using MCP tools."""
        print("\n" + "="*80)
        print("MCP-Powered Agent with LangChain")
        print("="*80)
        print(f"\nQuery: {query}\n")
        print("-" * 80)
        print("Agent Thinking...\n")
        
        tools_prompt = self.format_tools_prompt()
        
        full_prompt = f"""You are an AI assistant with access to the following MCP tools:

{tools_prompt}

When answering questions, you can use these tools. If a tool would help answer the question, mention which tool you would use and describe what it would return.

For example:
- To search for crewAI repos, use: github_search_repos("crewai")
- To get a repo's README, use: github_get_readme("owner", "repo_name")
- To list a directory, use: fs_list_directory("path")
- To read a file, use: fs_read_file("path/to/file")

Question: {query}

Please answer using relevant tools when appropriate."""
        
        try:
            response = self.llm.invoke(full_prompt)
            print("-" * 80)
            print("\nAgent Response:")
            print("-" * 80)
            print(response)
            print("\n" + "="*80 + "\n")
            return response
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("="*80 + "\n")
            return f"Error: {str(e)}"


# ============================================================================
# Demo
# ============================================================================

def main():
    """Run the MCP agent demo."""
    print("\n🤖 MCP-Enabled Agent with LangChain\n")
    print("This agent has access to:")
    print("  1. GitHub API (fetch repos, READMEs, search)")
    print("  2. Local Filesystem (read files, list directories)")
    print("\nInitializing...\n")
    
    agent = MCPLangChainAgent()
    
    # Demo queries
    queries = [
        "What's in the teamAlpha directory?",
        "Search GitHub for 'crewai' and tell me what you find",
        "Get the README from the crewai repository and summarize it",
        "Read the pyproject.toml file and tell me what dependencies are listed",
    ]
    
    # Run a few queries
    for i, query in enumerate(queries[:2], 1):
        print(f"\n▶️  Query {i}/{len(queries[:2])}")
        agent.ask(query)
        print("\n" + "─"*80)


if __name__ == "__main__":
    main()
