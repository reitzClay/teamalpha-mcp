#!/usr/bin/env python3
"""
Direct MCP Tool Execution Demo
Shows actual tool execution without LLM mediation.
"""
import json
import os
from langchain_ollama import OllamaLLM


class GitHubMCPClient:
    """Real GitHub API client."""
    
    def search_repositories(self, query: str, limit: int = 3) -> dict:
        """Search for repositories on GitHub."""
        try:
            import requests
            
            params = {"q": query, "per_page": limit, "sort": "stars", "order": "desc"}
            response = requests.get(
                "https://api.github.com/search/repositories",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for repo in data.get("items", [])[:limit]:
                    results.append({
                        "name": repo["full_name"],
                        "description": repo["description"],
                        "url": repo["html_url"],
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                    })
                return {"success": True, "repos": results}
            else:
                return {"success": False, "error": f"GitHub API returned {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_repository_readme(self, owner: str, repo: str) -> dict:
        """Fetch README from a GitHub repository."""
        try:
            import requests
            
            url = f"https://api.github.com/repos/{owner}/{repo}/readme"
            headers = {"Accept": "application/vnd.github.v3.raw"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text[:1500]
                return {"success": True, "content": content}
            else:
                return {"success": False, "error": f"GitHub returned {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class FilesystemMCPClient:
    """Real filesystem access client."""
    
    def list_directory(self, path: str = ".") -> dict:
        """List directory contents."""
        try:
            if not os.path.isdir(path):
                return {"success": False, "error": f"Not a directory: {path}"}
            
            items = os.listdir(path)
            dirs = [d for d in items if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
            files = [f for f in items if os.path.isfile(os.path.join(path, f)) and not f.startswith('.')]
            
            return {
                "success": True,
                "path": path,
                "directories": sorted(dirs),
                "files": sorted(files),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_file(self, path: str) -> dict:
        """Read a file."""
        try:
            if not os.path.exists(path):
                return {"success": False, "error": f"File not found: {path}"}
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 1500:
                content = content[:1500] + f"\n\n... (truncated, {len(content)} total chars)"
            
            return {"success": True, "path": path, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Initialize clients
github = GitHubMCPClient()
filesystem = FilesystemMCPClient()


class ToolDemo:
    """Demonstrate MCP tools in action."""
    
    def __init__(self):
        self.llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
    
    def demo_filesystem_tools(self):
        """Demo: List directory and read file."""
        print("\n" + "="*80)
        print("📂 MCP Filesystem Tools Demo")
        print("="*80 + "\n")
        
        # List /app directory
        print("🔧 Executing: fs_list_directory('/app')\n")
        result = filesystem.list_directory("/app")
        
        if result["success"]:
            print(f"Directory: {result['path']}")
            print(f"\n📁 Subdirectories: {', '.join(result['directories']) or 'None'}")
            print(f"📄 Files: {', '.join(result['files'][:10])}")
        else:
            print(f"Error: {result['error']}")
        
        # Read pyproject.toml
        print("\n" + "-"*80)
        print("\n🔧 Executing: fs_read_file('pyproject.toml')\n")
        result = filesystem.read_file("/app/pyproject.toml")
        
        if result["success"]:
            print("Content:")
            print(result["content"])
        else:
            print(f"Error: {result['error']}")
        
        print("\n" + "="*80)
    
    def demo_github_tools(self):
        """Demo: Search GitHub and get README."""
        print("\n" + "="*80)
        print("🐙 MCP GitHub Tools Demo")
        print("="*80 + "\n")
        
        # Search for crewai
        print("🔧 Executing: github_search_repositories('crewai')\n")
        result = github.search_repositories("crewai", limit=3)
        
        if result["success"]:
            print("Search Results:")
            for i, repo in enumerate(result["repos"], 1):
                print(f"\n  {i}. {repo['name']} ⭐ {repo['stars']}")
                print(f"     {repo['description']}")
                print(f"     🔗 {repo['url']}")
        else:
            print(f"Error: {result['error']}")
        
        # Get the top crewai repo's README
        print("\n" + "-"*80)
        print("\n🔧 Executing: github_get_repository_readme('joaomdmoura', 'crewAI')\n")
        result = github.get_repository_readme("joaomdmoura", "crewAI")
        
        if result["success"]:
            print("README Content (first 1500 chars):")
            print(result["content"])
        else:
            print(f"Error: {result['error']}")
        
        print("\n" + "="*80)
    
    def analyze_with_llm(self, tool_output: str, prompt: str) -> str:
        """Use LLM to analyze tool output."""
        analysis_prompt = f"""I ran an MCP tool and got the following output:

{tool_output}

Question: {prompt}

Please analyze the output and answer the question."""
        
        return self.llm.invoke(analysis_prompt)
    
    def run_all_demos(self):
        """Run all tool demonstrations."""
        print("\n" + "="*80)
        print("🚀 MCP Tools Integration Demo")
        print("="*80)
        print("\nThis demo shows how MCP (Model Context Protocol) tools")
        print("integrate with an AI agent to perform real tasks.")
        print("\nAvailable MCP Tools:")
        print("  📂 fs_list_directory() - List directory contents")
        print("  📄 fs_read_file()       - Read file contents")
        print("  🔍 github_search_repos()- Search GitHub repositories")
        print("  📖 github_get_readme()  - Fetch repository README")
        
        self.demo_filesystem_tools()
        self.demo_github_tools()
        
        # Bonus: LLM analysis
        print("\n" + "="*80)
        print("🧠 LLM Analysis of Tool Results")
        print("="*80 + "\n")
        
        print("Using LLM to analyze pyproject.toml...")
        with open("/app/pyproject.toml", 'r') as f:
            content = f.read()
        
        analysis = self.analyze_with_llm(
            content,
            "What are the main dependencies of this project?"
        )
        
        print("\nAnalysis:\n")
        print(analysis)
        
        print("\n" + "="*80)


def main():
    """Run the demo."""
    demo = ToolDemo()
    demo.run_all_demos()


if __name__ == "__main__":
    main()
