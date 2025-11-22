# Building an Agentic AI Software Team

This guide shows how to use the **TeamAlpha framework** to create and run collaborative AI agents that work together like a software team.

## Architecture Overview

The framework provides three core components:

### 1. **Agent** (`src/teamalpha/agent.py`)
Individual AI agents with:
- **Role**: Engineer, Reviewer, Architect, Tester, PM
- **Tools**: Callable functions (write code, run tests, review, etc.)
- **Memory**: Shared message history
- **LLM**: Powered by Ollama (llama3)

### 2. **Team** (`src/teamalpha/team.py`)
Orchestration layer that:
- Manages multiple agents
- Creates and assigns tasks
- Broadcasts messages to all agents
- Tracks task status and results
- Maintains conversation history

### 3. **Message & Task**
- **Message**: Team communication with sender, role, and timestamp
- **Task**: Work items with assignment, status, and results

## Quick Start

### Example 1: Simple Agent Usage

```python
from src.teamalpha.agent import Agent, AgentRole, Tool

# Create an engineer agent
engineer = Agent(name="Alice", role=AgentRole.ENGINEER)

# Add a tool
engineer.add_tool(Tool(
    name="write_code",
    description="Write Python code",
    func=lambda filename, content: f"Wrote {filename}",
    required_args=["filename", "content"]
))

# Have the agent think about a task
response = engineer.think("Design a login system")
print(response)

# Or execute (think + use tools)
result = engineer.execute("Build a user authentication module")
print(result)
```

### Example 2: Building a Team

```python
from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole

# Create team
team = Team("ProductTeam")

# Add agents
engineer = Agent(name="Alice", role=AgentRole.ENGINEER)
reviewer = Agent(name="Bob", role=AgentRole.REVIEWER)
tester = Agent(name="Charlie", role=AgentRole.TESTER)

team.add_agent(engineer)
team.add_agent(reviewer)
team.add_agent(tester)

# Create and execute a task
task = team.create_task("feature-1", "Build login feature")
team.assign_task("feature-1", "Alice")
result = team.execute_task("feature-1")

print(result.result)  # View the work output

# Check status
status = team.get_status_report()
print(status)
```

### Example 3: Multi-Step Workflow

```python
# Create a workflow: Design → Code → Review → Test

team = Team("SoftwareTeam")
# ... add agents ...

# Step 1: Architect designs
task1 = team.create_task("design", "Design microservices architecture")
team.assign_task("design", "architect_agent.name")
team.execute_task("design")

# Step 2: Engineer implements
task2 = team.create_task("code", "Implement according to design")
team.assign_task("code", "engineer_agent.name")
team.execute_task("code")

# Step 3: Reviewer checks
task3 = team.create_task("review", "Code review and approval")
team.assign_task("review", "reviewer_agent.name")
team.execute_task("review")

# Step 4: Tester validates
task4 = team.create_task("test", "Run full test suite")
team.assign_task("test", "tester_agent.name")
team.execute_task("test")
```

## Customization

### Creating Custom Tools

```python
def run_linter(files: str) -> str:
    """Run linter on files."""
    # Your implementation
    return f"Linted {files}: 3 issues found"

engineer.add_tool(Tool(
    name="lint",
    description="Check code quality with linter",
    func=run_linter,
    required_args=["files"]
))
```

### Custom Agent Roles

```python
from enum import Enum

class CustomAgentRole(Enum):
    DATA_SCIENTIST = "data_scientist"
    DEVOPS = "devops_engineer"

agent = Agent(name="Dave", role=CustomAgentRole.DEVOPS)
```

### Tool Call Parsing

Agents can parse LLM responses for tool invocations. Expected format:

```
[TOOL: write_code, ARGS: {"filename": "app.py", "content": "..."}]
[TOOL: run_git, ARGS: {"cmd": "commit -m 'feature'"}]
```

The agent will automatically detect and invoke these tools.

## Advanced: Integration with Your HTTP Server

You can wrap the team framework with your FastAPI server:

```python
from fastapi import FastAPI
from src.teamalpha.team import Team

app = FastAPI()

# Initialize team
team = Team("MyTeam")
# ... add agents ...

@app.post("/execute-workflow")
async def execute(workflow_name: str, description: str):
    """Execute a workflow via HTTP."""
    task = team.create_task(workflow_name, description)
    agent = team.get_agent_by_role(AgentRole.PM)
    team.assign_task(workflow_name, agent.name)
    result = team.execute_task(workflow_name)
    return {"result": result.result}
```

## Running the Example

```bash
# The full example is in example_team.py
# It shows agents building an authentication feature

python3 example_team.py
```

## Key Concepts

| Concept | Purpose |
|---------|---------|
| **Agent** | Single AI actor with a role and tools |
| **Team** | Multi-agent coordinator and orchestrator |
| **Task** | Unit of work assigned to an agent |
| **Tool** | Callable function available to agents |
| **Message** | Communication log entry |
| **Role** | Agent's specialization (engineer, reviewer, etc.) |

## Next Steps

1. **Extend tools**: Add real git, file I/O, testing, and deployment tools
2. **Agent-to-agent communication**: Build peer-to-peer messaging and debates
3. **Autonomous workflows**: Use agent memory and context to chain tasks
4. **Integration**: Connect to your codebase, CI/CD, and monitoring
5. **Evaluation**: Add metrics for agent performance and code quality

## Architecture Diagram

```
┌─────────────────────────────────┐
│         HTTP Endpoint            │  (server.py via FastAPI)
└────────────┬──────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│         Team                      │  Orchestration & Task Management
├─────────────────────────────────┤
│ Agent 1 (Engineer)               │
│ Agent 2 (Reviewer)               │
│ Agent 3 (Tester)                 │
│ Agent 4 (PM)                     │
└────────┬────────┬────────┬────────┘
         │        │        │
         ▼        ▼        ▼
    ┌────────┬────────┬────────┐
    │ Tools  │ Tools  │ Tools  │
    └────────┴────────┴────────┘
         │        │        │
         └────┬───┴────┬───┘
              │        │
              ▼        ▼
          ┌──────────────────┐
          │  Ollama LLM      │
          │  (llama3)        │
          └──────────────────┘
```

## Troubleshooting

**Q: Agents aren't using tools?**  
A: Check tool call format in agent response: `[TOOL: name, ARGS: {...}]`

**Q: Messages not reaching all agents?**  
A: Verify `broadcast_message()` is called; all agents should have identical memory.

**Q: Tasks hanging?**  
A: LLM calls can be slow. Consider timeouts or running in production with smaller models.

## For More Information

- See `example_team.py` for a complete workflow example
- Explore `src/teamalpha/agent.py` for agent internals
- Check `src/teamalpha/team.py` for team orchestration API
