#!/usr/bin/env python3
"""
Complete MCP Workflow Example
Demonstrates a realistic multi-step task using MCP tools.
"""
from langchain_ollama import OllamaLLM
import json
import requests
import os


class RepoAnalyzer:
    """Analyzes GitHub repositories using MCP tools."""
    
    def __init__(self):
        self.llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
        self.github_api = "https://api.github.com"
    
    def search_repositories(self, query: str, limit: int = 3) -> list:
        """MCP Tool: Search GitHub repositories."""
        print(f"\n🔍 Searching GitHub for '{query}'...")
        
        try:
            params = {"q": query, "per_page": limit, "sort": "stars", "order": "desc"}
            response = requests.get(
                f"{self.github_api}/search/repositories",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                repos = []
                for item in response.json().get("items", [])[:limit]:
                    repos.append({
                        "name": item["full_name"],
                        "url": item["html_url"],
                        "description": item.get("description", "No description"),
                        "stars": item["stargazers_count"],
                        "language": item.get("language", "Unknown"),
                    })
                print(f"✓ Found {len(repos)} repositories")
                return repos
            else:
                print(f"✗ GitHub API error: {response.status_code}")
                return []
        except Exception as e:
            print(f"✗ Error: {e}")
            return []
    
    def fetch_readme(self, owner: str, repo: str) -> str:
        """MCP Tool: Fetch repository README."""
        print(f"\n📖 Fetching README from {owner}/{repo}...")
        
        try:
            url = f"{self.github_api}/repos/{owner}/{repo}/readme"
            headers = {"Accept": "application/vnd.github.v3.raw"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text[:2000]  # First 2000 chars
                print(f"✓ README fetched ({len(response.text)} total chars)")
                return content
            else:
                print(f"✗ No README found or API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def get_repo_stats(self, owner: str, repo: str) -> dict:
        """MCP Tool: Get repository statistics."""
        print(f"\n📊 Fetching stats for {owner}/{repo}...")
        
        try:
            url = f"{self.github_api}/repos/{owner}/{repo}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = {
                    "stars": data["stargazers_count"],
                    "forks": data["forks_count"],
                    "open_issues": data["open_issues_count"],
                    "language": data.get("language", "Unknown"),
                    "created_at": data["created_at"],
                    "updated_at": data["updated_at"],
                }
                print(f"✓ Stats fetched")
                return stats
            else:
                print(f"✗ API error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"✗ Error: {e}")
            return {}
    
    def analyze_repo(self, repo_name: str) -> str:
        """Use LLM to analyze repository information."""
        print(f"\n🧠 Analyzing {repo_name}...")
        
        # Parse owner/repo
        if "/" in repo_name:
            owner, repo = repo_name.split("/", 1)
        else:
            owner = repo_name
            repo = repo_name
        
        # Fetch data using MCP tools
        readme = self.fetch_readme(owner, repo)
        stats = self.get_repo_stats(owner, repo)
        
        if not readme and not stats:
            return "Could not fetch repository information"
        
        # Prepare data for LLM analysis
        analysis_prompt = f"""Based on the following repository information, provide a concise analysis:

Repository: {owner}/{repo}

Statistics:
{json.dumps(stats, indent=2)}

README (first part):
{readme or '[No README found]'}

Please provide:
1. What is this project about?
2. Main technologies used
3. Project maturity (early/stable/mature)
4. Who would benefit from using this?
5. Key features or strengths"""
        
        response = self.llm.invoke(analysis_prompt)
        return response
    
    def compare_projects(self, queries: list) -> str:
        """Compare multiple projects using MCP tools."""
        print("\n" + "="*80)
        print(f"🔬 Comparing Projects: {', '.join(queries)}")
        print("="*80)
        
        all_repos = []
        
        # Search for each query
        for query in queries:
            repos = self.search_repositories(query, limit=2)
            all_repos.extend(repos)
        
        # Prepare comparison data
        repos_summary = json.dumps(all_repos, indent=2)
        
        comparison_prompt = f"""I found these repositories matching multiple searches:

{repos_summary}

Please compare these projects:
1. What are the main differences?
2. Which would be best for what use cases?
3. How do they compare in terms of popularity and maturity?
4. Are they complementary or competitive?"""
        
        response = self.llm.invoke(comparison_prompt)
        return response


def main():
    """Run the complete workflow."""
    analyzer = RepoAnalyzer()
    
    print("\n" + "="*80)
    print("🚀 MCP Workflow: GitHub Repository Analysis")
    print("="*80)
    
    # Workflow 1: Analyze a single project
    print("\n" + "─"*80)
    print("Workflow 1: Deep dive into CrewAI")
    print("─"*80)
    
    analysis = analyzer.analyze_repo("crewAIInc/crewAI")
    print("\n📋 Analysis Result:\n")
    print(analysis)
    
    # Workflow 2: Compare multiple projects
    print("\n" + "─"*80)
    print("Workflow 2: Compare AI frameworks")
    print("─"*80)
    
    comparison = analyzer.compare_projects(["crewai", "langchain", "autogen"])
    print("\n📊 Comparison Result:\n")
    print(comparison)
    
    print("\n" + "="*80)
    print("✅ Workflow Complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
