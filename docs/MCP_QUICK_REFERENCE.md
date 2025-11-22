# MCP Quick Reference

## Run the Demos

```bash
# Best for seeing actual tool execution
docker compose exec teamalpha-agent python mcp_tool_demo.py

# Best for realistic agent workflow
docker compose exec teamalpha-agent python mcp_workflow_example.py

# Best for understanding tool awareness
docker compose exec teamalpha-agent python mcp_langchain_agent.py

# Best for advanced execution patterns
docker compose exec teamalpha-agent python mcp_executor_agent.py
```

---

## Available MCP Tools

### Filesystem Tools
```python
filesystem.read_file(path)          # Read file contents
filesystem.list_directory(path)     # List directory contents
```

### GitHub Tools
```python
github.search_repositories(query)           # Search repos
github.get_repository_readme(owner, repo)   # Fetch README
github.get_repo_stats(owner, repo)          # Get repo stats
```

---

## Example: Use MCP Tools

### Step 1: Import Client
```python
from mcp_tool_demo import GitHubMCPClient, FilesystemMCPClient

github = GitHubMCPClient()
filesystem = FilesystemMCPClient()
```

### Step 2: Execute Tool
```python
result = github.search_repositories("crewai", limit=3)
# Result: {"success": True, "repos": [...]}
```

### Step 3: Analyze with LLM
```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3", base_url="http://ollama:11434")
analysis = llm.invoke(f"""
Analyze these repos: {result}
Which is most mature?
""")
```

---

## Docker Quick Commands

```bash
# View logs
docker compose logs -f teamalpha-agent

# Stop everything
docker compose down

# Rebuild and restart
docker compose up -d --build

# Run bash in container
docker compose exec teamalpha-agent bash

# Run Python directly
docker compose exec teamalpha-agent python -c "print('Hello')"
```

---

## Project Structure

```
/home/clay/Development/teamAlpha/
├── 📄 MCP_INTEGRATION_GUIDE.md      ← Detailed guide
├── 📄 MCP_SUMMARY.md                ← This overview
├── 📄 MCP_QUICK_REFERENCE.md        ← Quick ref (this file)
├── 📄 pyproject.toml                ← Dependencies
├── 📄 compose.yaml                  ← Docker setup
├── 📄 Dockerfile                    ← Container image
│
├── 🐍 mcp_tool_demo.py              ← ⭐ START HERE
├── 🐍 mcp_workflow_example.py       ← ⭐ REALISTIC EXAMPLE
├── 🐍 mcp_langchain_agent.py        ← Tool awareness
├── 🐍 mcp_executor_agent.py         ← Advanced patterns
├── 🐍 mcp_agent.py                  ← Server framework
│
├── 🐍 request_poem.py               ← Simple example
├── 🐍 crew.py                       ← Original agent
│
└── src/
    └── teamalpha/
        ├── __init__.py
        └── config/
            └── tasks.yaml
```

---

## Key Concepts Recap

### MCP = "USB-C for AI"
- Standard interface for tools
- LLM accesses external systems safely
- Supports any type of tool/API

### Tool Execution Flow
```
Agent → "I need data"
  ↓
Tool → "Fetching from GitHub API..."
  ↓
Data → "Here are 5 crewAI repos"
  ↓
LLM → "Based on this data, crewAI is mature because..."
```

### Three Types of Agents
1. **Chatbot** — No tools, just inference
2. **Tool-Aware Agent** — Knows about tools, doesn't use them
3. **Tool-Executing Agent** — Can actually call tools ← **You have this!**

---

## Common Tasks

### Search GitHub
```python
repos = github.search_repositories("your-query")
print(f"Found {len(repos['repos'])} repositories")
```

### Analyze a Repo
```python
readme = github.get_repository_readme("owner", "repo")
analysis = llm.invoke(f"Summarize this README: {readme}")
```

### Read Local File
```python
content = filesystem.read_file("path/to/file.py")
review = llm.invoke(f"Review this code: {content}")
```

### Compare Projects
```python
repos1 = github.search_repositories("langchain")
repos2 = github.search_repositories("crewai")
comparison = llm.invoke(f"Compare: {repos1} vs {repos2}")
```

---

## Files to Modify

### Add a New Tool
Edit `mcp_tool_demo.py`:
```python
class NewToolMCP:
    def my_tool(self, arg):
        # Implement your tool
        return {"success": True, "data": result}
```

### Change Model
Edit Docker `compose.yaml`:
```yaml
environment:
  - OLLAMA_MODEL=mistral  # or any other model
```

### Add Dependencies
Edit `pyproject.toml`:
```toml
dependencies = [
    "langchain>=0.1.0",
    "your-new-library"  # Add here
]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Make sure `docker compose up -d` is running |
| "Module not found" | Rebuild: `docker compose up -d --build` |
| "API rate limit" | Add delays between GitHub API calls |
| "File not found" | Use absolute path `/app/filename` |
| "Ollama not responding" | Check: `docker compose logs ollama` |

---

## Next Steps

1. **Run demos** → See tools in action
2. **Read guides** → Understand MCP concepts
3. **Modify scripts** → Adapt to your use case
4. **Add tools** → Extend with custom tools
5. **Deploy** → Push to production

---

## Resources

- **Full Guide**: `MCP_INTEGRATION_GUIDE.md`
- **Detailed Summary**: `MCP_SUMMARY.md`
- **Official MCP**: https://modelcontextprotocol.io
- **Tool Registry**: https://smithery.ai

---

## Performance Tips

- Cache tool results for frequently accessed data
- Use tool limits (e.g., `limit=5` in GitHub searches)
- Parallelize independent tool calls
- Reuse client connections

---

**You're all set! Run `mcp_tool_demo.py` to see everything in action.** 🚀
