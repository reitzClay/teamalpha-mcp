# TeamAlpha - Agentic AI Software Development Framework

A sophisticated multi-agent framework for collaborative software development, powered by LangChain + Ollama.

## 📦 Project Structure

```
teamAlpha/
├── README.md                          # This file
├── pyproject.toml                     # Python dependencies
├── Dockerfile                         # Container image
│
├── src/teamalpha/                     # Core framework
│   ├── __init__.py
│   ├── agent.py                       # Agent base class and roles
│   ├── team.py                        # Team orchestration
│   ├── client.py                      # HTTP client library
│   └── tools/                         # Built-in tools
│
├── server.py                          # FastAPI HTTP wrapper for LLM
├── client.py                          # CLI client
│
├── infrastructure/                    # Docker & deployment configs
│   ├── docker-compose.yml             # Dev orchestration
│   ├── docker-compose.dev.yml         # Development environment
│   └── docker-compose.staging.yml     # Staging environment
│
├── docs/                              # Documentation
│   ├── TEAM_GUIDE.md                  # Framework guide
│   ├── DEV_RUN.md                     # Development instructions
│   └── MCP_*.md                       # MCP integration guides
│
├── examples/                          # Example scripts
│   ├── example_team.py                # Team collaboration example
│   └── run_team_on_prod.py            # Running agents on production repo
│
├── tools/                             # Utility tools
│   ├── workflow_analyzer.py           # Analyze git workflows
│   └── mcp_tool_demo.py               # MCP tool demonstrations
│
├── projects/                          # Project workspaces
│   ├── theagame-analysis/             # TheAgame project analysis
│   │   ├── analyze_theagame.py
│   │   ├── analyze_theagame_prod.py
│   │   └── *.md                       # Reports and documentation
│   │
│   └── greenfield-starter/            # Template for new projects
│       ├── README.md                  # Getting started guide
│       ├── project.yaml               # Project metadata
│       ├── team.yaml                  # Team definition
│       ├── tools.yaml                 # Tool registry
│       ├── run.py                     # Main entry point
│       ├── workflows/                 # Workflow definitions
│       ├── tools/                     # Custom implementations
│       └── output/                    # Generated reports
│
└── config/                            # Configuration templates
    ├── agents.yaml
    └── tasks.yaml
```

## 🚀 Quick Start

### 1. Start Infrastructure

**Development (with isolated ports):**
```bash
cd infrastructure
docker compose -f docker-compose.dev.yml up --build
```

**Production (if running locally for testing):**
```bash
docker compose -f /path/to/prod/docker-compose.prod.yml up -d
```

### 2. Create a New Project

```bash
# Copy the greenfield template
cp -r projects/greenfield-starter projects/my-project
cd projects/my-project

# Configure your project
nano project.yaml    # Update metadata
nano team.yaml       # Define your team

# Run the project
python3 run.py
```

### 3. Use as a Library

```python
from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole

# Create team
team = Team("My Team")

# Add agents
engineer = Agent("Alice", AgentRole.ENGINEER)
reviewer = Agent("Bob", AgentRole.REVIEWER)

team.add_agent(engineer)
team.add_agent(reviewer)

# Create and execute tasks
task = team.create_task("task-1", "Implement login endpoint")
team.assign_task("task-1", "Alice")
team.execute_task("task-1")
```

### 4. Use HTTP API

**Start the server:**
```bash
python3 server.py
```

**Generate text:**
```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Design a REST API", "max_tokens": 500}'
```

**Check health:**
```bash
curl http://localhost:8080/health
```

## 🎯 Core Components

### Agent (`src/teamalpha/agent.py`)
- **Roles**: Engineer, Code Reviewer, Architect, QA Engineer, Product Manager
- **Capabilities**: LLM invocation, tool calling, memory management
- **Integration**: LangChain + Ollama

### Team (`src/teamalpha/team.py`)
- **Orchestration**: Manage multiple agents
- **Task Management**: Create, assign, execute tasks
- **Communication**: Message broadcasting to team members
- **Reporting**: Status reports and task results

### Tools & Utilities
- **workflow_analyzer.py**: Git workflow analysis and recommendations
- **mcp_tool_demo.py**: Model Context Protocol demonstrations
- **client.py**: Reusable HTTP client library

## 📊 Execution Model

```
┌─────────────────┐
│   Project       │
│   Configuration │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Load Team Config      │
│   Create Agents         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Define Workflows      │
│   Create Tasks          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Assign Tasks to       │
│   Agents by Role        │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│   Execute Tasks                      │
│   - Agent thinks about task          │
│   - Parses and invokes tools if req. │
│   - Returns results                  │
└────────┬─────────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Collect Results       │
│   Generate Reports      │
│   Save Outputs          │
└─────────────────────────┘
```

## 🔧 Configuration

### project.yaml
```yaml
name: my-project
version: 1.0.0
description: "Project description"
goals:
  - "Goal 1"
  - "Goal 2"
```

### team.yaml
```yaml
agents:
  - name: Alice
    role: engineer
    description: "Backend engineer"
  
  - name: Bob
    role: code_reviewer
    description: "Code quality expert"
```

### tools.yaml
```yaml
tools:
  - name: code_analyzer
    description: "Analyze code quality"
    module: tools.code_analyzer
    function: analyze_code
```

## 📚 Examples

### Analyze a Repository
```bash
cd projects/theagame-analysis
python3 analyze_theagame_prod.py
```

### Run TeamAlpha on a Production Build
```bash
python3 examples/run_team_on_prod.py
```

### Build a Collaboration Workflow
```bash
python3 examples/example_team.py
```

## 🌐 Integration Points

### LLM Provider
- **Local**: Ollama (llama3 by default)
- **External**: Configure LangChain to use OpenAI, Claude, etc.

### Container Orchestration
- **Development**: `docker-compose.dev.yml`
- **Staging**: `docker-compose.staging.yml`
- **Production**: Separate prod compose files

### HTTP API
- **FastAPI server** for remote LLM access
- **Reusable client** for integration with external tools

### Git Workflow
- **Git Flow**: feature → dev → staging → prod
- **Analysis tools** for branch health, commit patterns
- **Automation ready** for GitHub Actions CI/CD

## 🚦 Running Dev and Prod in Parallel

Without port conflicts:

```bash
# Terminal 1: Production (on prod server)
cd /home/clay/Projects/TheAgame
docker compose -f docker-compose.prod.yml up -d

# Terminal 2: Development (on your machine)
cd /home/clay/Development/teamAlpha
docker compose -f infrastructure/docker-compose.dev.yml up --build

# Test dev (won't affect prod)
curl http://localhost:18080/generate
```

## 📖 Documentation

- **TEAM_GUIDE.md**: Comprehensive framework documentation
- **DEV_RUN.md**: Development and deployment instructions
- **MCP_*.md**: Model Context Protocol integration guides
- **projects/greenfield-starter/README.md**: New project template

## 🔄 Workflow Examples

### Feature Development
```bash
git checkout -b feature/my-feature dev
# ... implement feature ...
python3 run_team_on_prod.py  # Test with agents
git push origin feature/my-feature
# Create PR → Review → Merge to dev
```

### Code Review
```python
from src.teamalpha.team import Team
from src.teamalpha.agent import AgentRole

team = Team("Review Team")
# ... add reviewer agents ...

task = team.create_task("review-1", "Review pull request #42")
reviewer = team.get_agent_by_role(AgentRole.REVIEWER)
team.assign_task("review-1", reviewer.name)
team.execute_task("review-1")
```

### Architecture Design
```python
team = Team("Architecture Team")
architect = team.get_agent_by_role(AgentRole.ARCHITECT)

task = team.create_task("arch-1", "Design database schema")
team.assign_task("arch-1", architect.name)
result = team.execute_task("arch-1")

# Generate report
print(result.result)  # Save to file
```

## 🔐 Security Considerations

- **Environment Variables**: Use `.env` files (git-ignored) for secrets
- **Volume Mounts**: Production paths mounted read-only in dev
- **Network**: Services isolated on custom Docker networks
- **Git Credentials**: Never commit `.env` or private keys

## 🐛 Troubleshooting

**LLM not responding**: Ensure Ollama is running
```bash
docker ps | grep ollama
```

**Port conflicts**: Use different compose files or check active services
```bash
docker ps
lsof -i :8080
```

**Import errors**: Add src to Python path
```bash
export PYTHONPATH="${PYTHONPATH}:/home/clay/Development/teamAlpha"
```

## 🎓 Next Steps

1. **Explore Examples**: Run `examples/example_team.py`
2. **Create a Project**: Copy `projects/greenfield-starter`
3. **Build Workflows**: Define tasks and agents
4. **Integrate Tools**: Add custom tool implementations
5. **Automate**: Set up CI/CD pipelines

## 📞 Support

For issues and questions:
1. Check `docs/` for existing documentation
2. Review `examples/` for reference implementations
3. Inspect agent/team logs for debugging
4. Run with `--verbose` for detailed output

---

**TeamAlpha v0.1.0** | Multi-agent agentic AI framework for collaborative software development
