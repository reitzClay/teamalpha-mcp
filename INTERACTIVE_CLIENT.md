# 🚀 Interactive TeamAlpha Client

Your multi-agent agentic system is now ready for interactive use!

## Quick Start

### Option 1: Simple Client (Recommended)
```bash
.venv/bin/python3 interactive_client.py
```

### Option 2: With Setup & Model Waiting
```bash
.venv/bin/python3 setup_and_run.py
```

## System Status

✅ **Running Services:**
- **Ollama** (LLM): localhost:11435
- **TeamAlpha Agent API**: localhost:18080

✅ **Agent Team:**
- Alice (Engineer) - Backend & architecture
- Bob (Code Reviewer) - Code quality & reviews
- Eve (Architect) - System design & patterns
- Charlie (QA Engineer) - Testing & validation
- Diana (Product Manager) - Requirements & strategy

✅ **Available Commands:**

| Command | Description |
|---------|-------------|
| `status` | Check agent health |
| `team create` | Create team with all 5 agents |
| `agents` | List available agents |
| `generate <prompt>` | Send prompt to LLM |
| `assign <name> <task>` | Assign task to specific agent |
| `help` | Show all commands |
| `exit` | Exit client |

## Examples

### Start Interactive Session
```bash
.venv/bin/python3 interactive_client.py
```

### Check Agent Status
```
teamalpha> status
✅ Agent Status: {'status': 'ok'}
```

### Create Team
```
teamalpha> team create
👥 Team 'Diana' created with 5 agents:
   • Alice (engineer)
   • Bob (code_reviewer)
   • Eve (architect)
   • Charlie (qa_engineer)
   • Diana (product_manager)
```

### Send Task to LLM
```
teamalpha> generate "Design a REST API for a user authentication system"
💭 Sending prompt to agent...
🤖 Agent Response:
[LLM generates response...]
```

### Assign Task to Specific Agent
```
teamalpha> assign Alice "Implement a user login endpoint in FastAPI"
🎯 Assigning to Alice (engineer):
   Task: Implement a user login endpoint in FastAPI

💭 Sending prompt to agent...
🤖 Agent Response:
[Agent responds based on their role...]
```

### Assign to Different Agents
```
teamalpha> assign Eve "Review the API design for security"
teamalpha> assign Charlie "Write test cases for the login endpoint"
teamalpha> assign Bob "Review the implementation code"
```

## Architecture

```
┌─────────────────────────────────────────┐
│   Interactive Client (interactive_client.py)
│   - Command parsing
│   - Team management
│   - Task assignment
└────────────────┬────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────┐
│   FastAPI Server (server.py:18080)
│   - /health endpoint
│   - /generate endpoint
│   - Request/response handling
└────────────────┬────────────────────────┘
                 │ LangChain
                 ▼
┌─────────────────────────────────────────┐
│   LLM Client
│   - Model routing
│   - Prompt engineering
│   - Response parsing
└────────────────┬────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────┐
│   Ollama (localhost:11435)
│   - llama3 model
│   - Token generation
│   - Inference engine
└─────────────────────────────────────────┘
```

## Model Status

The `llama3` model is downloading (~4.7GB).

**While you wait**, you can:
1. Run `generate` commands and they will work once the model loads
2. Run other commands like `status`, `team create`, `agents`, `help`
3. Start writing tasks to assign once ready

**Current Status:**
```bash
# Check model status
docker exec dev_ollama ollama list

# Monitor download
docker logs dev_ollama | tail -20

# Manual pull (if needed)
docker exec dev_ollama ollama pull llama3
```

## Features

### 1. **Interactive CLI**
- Real-time command execution
- Context-aware responses
- Multi-turn conversations

### 2. **Agent Specialization**
Each agent has a specific role that influences their responses:
- **Engineer**: Implementation-focused, technical depth
- **Reviewer**: Quality-focused, identifying issues
- **Architect**: Design-focused, big-picture thinking
- **QA Engineer**: Testing-focused, edge cases
- **PM**: Strategy-focused, requirements

### 3. **HTTP Communication**
- RESTful API between client and server
- Stateless design
- Easy integration with other tools

### 4. **Task Management**
- Assign tasks to specific agents
- Track task assignments
- View agent capabilities

## Extending the Client

### Add Custom Commands
Edit `interactive_client.py` and add to the `interactive_loop()` method:

```python
if user_input.lower().startswith("custom "):
    custom_prompt = user_input[7:].strip()
    # Your custom logic here
    continue
```

### Add New Agent Roles
Edit `src/teamalpha/agent.py` and add to the `AgentRole` enum:

```python
class AgentRole(Enum):
    ENGINEER = "engineer"
    # ... existing roles ...
    SECURITY = "security"  # New role
```

Then update `interactive_client.py` to include the new role in `create_team()`.

## Troubleshooting

### Agent Server Not Responding
```bash
# Check if containers are running
docker ps

# Restart if needed
docker compose -f infrastructure/docker-compose.dev.yml restart

# View logs
docker logs dev_teamalpha_agent
```

### Ollama Model Not Loading
```bash
# Check model list
docker exec dev_ollama ollama list

# Pull model manually
docker exec dev_ollama ollama pull llama3

# Check Ollama logs
docker logs dev_ollama
```

### Import Errors
```bash
# Reinstall dependencies
uv sync

# Use venv for execution
.venv/bin/python3 interactive_client.py
```

## Next Steps

1. **Try the client now**: `python3 interactive_client.py`
2. **Create your team**: `team create`
3. **Assign tasks**: `assign Alice "Your task here"`
4. **Monitor performance**: Use `status` to check health
5. **Extend functionality**: Add custom agents and commands

## Stack Management

### Start the Stack
```bash
docker compose -f infrastructure/docker-compose.dev.yml up -d
```

### Stop the Stack
```bash
docker compose -f infrastructure/docker-compose.dev.yml down
```

### View Logs
```bash
# All services
docker compose -f infrastructure/docker-compose.dev.yml logs -f

# Specific service
docker logs dev_teamalpha_agent -f
docker logs dev_ollama -f
```

## Resources

- **Framework**: `src/teamalpha/` - Core agent system
- **Client Library**: `src/teamalpha/client.py` - HTTP client
- **Server**: `server.py` - FastAPI wrapper
- **Examples**: `examples/` - Usage patterns
- **Documentation**: `docs/` - Detailed guides

---

**Status**: ✅ Ready for interactive use

**Model Download**: ⏳ In progress (monitor with `docker logs dev_ollama`)

**Next Command**: `.venv/bin/python3 interactive_client.py`
