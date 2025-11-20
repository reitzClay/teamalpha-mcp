# MCP (Model Context Protocol) Integration Guide

## Overview

You now have a **fully functional MCP-enabled agent** that can:
- 📂 Access the local filesystem (list directories, read files)
- 🐙 Query GitHub API (search repos, fetch READMEs)
- 🧠 Use Ollama's llama3 model to analyze results
- 🔧 Execute tools and combine results

---

## What is MCP?

**MCP** (Model Context Protocol) is an open standard that allows AI applications to safely connect to external systems—like file systems, APIs, databases, and specialized tools.

Think of it like:
> **USB-C for AI** — Just as USB-C provides a standard way to connect different devices, MCP provides a standard way for AI models to safely access tools and data.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Docker Compose (Orchestration)               │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────┐          ┌──────────────────┐  │
│  │   Ollama       │          │   Python Agent   │  │
│  │  (llama3 LLM)  │◄────────►│   (LangChain)    │  │
│  │                │          │                  │  │
│  │ Port 11434     │          │  MCP Tool Layer: │  │
│  └────────────────┘          │  ├─ GitHub API   │  │
│          ▲                    │  ├─ Filesystem   │  │
│          │                    │  └─ Web Search   │  │
│          │                    │                  │  │
│          │                    └──────────────────┘  │
│  Internal Network (Docker)                          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## MCP Tools Available

### 1. **Filesystem Tools**
```python
fs_list_directory(path)      # List directory contents
fs_read_file(path)           # Read file contents
```

**Example:**
```python
result = filesystem.list_directory("/app")
# Returns: {"success": True, "directories": [...], "files": [...]}

result = filesystem.read_file("pyproject.toml")
# Returns: {"success": True, "content": "...file contents..."}
```

---

### 2. **GitHub Tools**
```python
github_search_repositories(query, limit)  # Search GitHub repos
github_get_repository_readme(owner, repo) # Fetch README
```

**Example:**
```python
result = github.search_repositories("crewai", limit=3)
# Returns:
# {
#   "success": True,
#   "repos": [
#     {
#       "name": "crewAIInc/crewAI",
#       "description": "...",
#       "url": "https://github.com/crewAIInc/crewAI",
#       "stars": 40621
#     },
#     ...
#   ]
# }

result = github.get_repository_readme("crewAIInc", "crewAI")
# Returns: {"success": True, "content": "...README content..."}
```

---

## Example Use Cases

### Case 1: Analyze Local Configuration
```python
# Tool execution
pyproject = filesystem.read_file("pyproject.toml")

# LLM analysis
llm_response = llm.invoke(f"""
Analyze this project file and tell me its dependencies:
{pyproject['content']}
""")

# Result: "The main dependencies are langchain, langchain-core, langchain-ollama, and requests..."
```

### Case 2: Research a GitHub Project
```python
# Tool execution
repos = github.search_repositories("crewai")
readme = github.get_repository_readme(repos[0]["owner"], repos[0]["repo"])

# LLM analysis
summary = llm.invoke(f"""
Based on this README, summarize the project:
{readme['content']}
""")

# Result: "CrewAI is a framework for orchestrating autonomous AI agents..."
```

### Case 3: Multi-Tool Workflow
```python
# 1. Check local project
local_config = filesystem.read_file("pyproject.toml")

# 2. Compare with related projects
github_results = github.search_repositories("langchain")

# 3. LLM synthesis
insights = llm.invoke(f"""
My project uses: {local_config}
Similar projects: {github_results}
How does my project compare?
""")
```

---

## How It Works

### Step 1: Tool Definition
```python
class GitHubMCPClient:
    def search_repositories(self, query: str):
        # Make actual API calls
        response = requests.get(f"https://api.github.com/search/repositories?q={query}")
        return response.json()
```

### Step 2: Tool Integration
```python
# Tools are available to the agent
agent.tools = {
    "github_search_repos": github_client.search_repositories,
    "fs_read_file": filesystem_client.read_file,
    # ...
}
```

### Step 3: Tool Execution
```python
# Agent calls tools based on the task
result = agent.tools["github_search_repos"]("crewai")
```

### Step 4: LLM Analysis
```python
# LLM reasons about tool results
llm_response = llm.invoke(f"""
Tool returned: {result}
What does this tell us?
""")
```

---

## The Scripts Included

### 1. `mcp_tool_demo.py` ⭐ **START HERE**
Demonstrates actual MCP tools in action with:
- Filesystem operations (list directories, read files)
- GitHub API calls (search repos, fetch READMEs)
- LLM analysis of results

**Run it:**
```bash
docker compose exec teamalpha-agent python mcp_tool_demo.py
```

---

### 2. `mcp_langchain_agent.py`
Shows how to expose tools to the LLM with descriptions:
- Tool registry with descriptions
- LLM-aware tool prompting
- Tool invocation patterns

---

### 3. `mcp_executor_agent.py`
Advanced agent that can parse LLM output and execute tools:
- Regex-based tool call extraction
- Tool result formatting
- Iterative tool use

---

### 4. `mcp_agent.py`
Framework for managing multiple MCP servers:
- Server startup/shutdown
- Tool aggregation from multiple servers
- Async tool execution

---

## Key Concepts

### **MCP Servers**
Separate services that expose tools. Examples:
- `mcp-server-filesystem` — File system access
- `mcp-server-github` — GitHub API
- `mcp-server-web` — Web search and scraping
- `mcp-server-git` — Git operations
- `mcp-server-slack` — Slack integration

**In this project:** We're implementing MCP clients directly (not using external servers), but the pattern is the same.

---

### **Tool Wrapping**
Converting real API calls into a standardized interface:

```python
# Raw API call
requests.get("https://api.github.com/search/repositories?q=crewai")

# Wrapped as MCP tool
def github_search_repos(query: str) -> dict:
    # Same API call, but with error handling, result formatting, etc.
    ...
```

---

### **LLM Tool Awareness**
The LLM needs to know what tools exist and when to use them:

```
System Prompt:
"You have access to these tools:
- github_search_repos(query): Search GitHub
- fs_read_file(path): Read a file
- ..."

User: "Find the crewAI repo and tell me about it"

Agent: "I'll search for crewai, then fetch its README"
       github_search_repos("crewai")
       github_get_readme("crewAIInc", "crewAI")
```

---

## Next Steps

### 1. **Extend with More Tools**
Add tools for:
- Web search (Brave, Tavily)
- Database queries (SQLite, PostgreSQL)
- API calls to any service

### 2. **Implement Tool Execution Loop**
Create an agent that:
1. Analyzes the task
2. Determines which tools to use
3. Executes them
4. Analyzes results
5. Repeats if needed

### 3. **Add Tool Caching**
Cache frequently requested data:
- GitHub repo info
- File contents
- API responses

### 4. **Connect Real MCP Servers**
Use official implementations:
```bash
pip install mcp mcp-server-filesystem mcp-server-github
```

---

## Resources

**Official MCP Documentation:**
- https://modelcontextprotocol.io

**MCP Server Registry:**
- https://smithery.ai — Curated server registry
- https://mcpservers.com — Community servers
- https://github.com/modelcontextprotocol/servers — Official servers

**Python SDK:**
```bash
pip install mcp
```

**Popular MCP Servers:**
- Filesystem, Git, GitHub, Slack, Notion, SQLite, Web Search, Brave, Playwright, Docker

---

## Summary

You now have:
✅ Working MCP tool integration
✅ GitHub API access
✅ Filesystem access
✅ LLM analysis of tool results
✅ Docker-based deployment
✅ Examples of tool execution

**The agent can now:**
1. Query external systems (GitHub, filesystem)
2. Get real data
3. Analyze with AI
4. Take intelligent actions

This is the foundation for building sophisticated AI agents! 🚀
