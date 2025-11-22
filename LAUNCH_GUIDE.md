# 🎉 TeamAlpha Interactive Client - Launch Summary

## ✅ System Status

**All systems operational and tested:**

| Component | Status | Port | Details |
|-----------|--------|------|---------|
| Ollama LLM | ✅ Running | 11435 | llama3 loaded & ready |
| Agent API | ✅ Running | 18080 | Health check: OK |
| Interactive Client | ✅ Ready | N/A | Tested & working |
| 5-Agent Team | ✅ Ready | N/A | All roles configured |

---

## 🚀 Quick Start

### Launch Interactive Client
```bash
# Option 1: Using bash script (simplest)
./run-client.sh

# Option 2: Direct Python
.venv/bin/python3 interactive_client.py

# Option 3: With setup checker
.venv/bin/python3 setup_and_run.py
```

### First Commands
```
teamalpha> team create          # Initialize 5-agent team
teamalpha> status               # Verify everything running
teamalpha> assign Alice "Design a REST API"    # Get Alice's perspective
teamalpha> assign Bob "Review the design"      # Get Bob's review
teamalpha> exit
```

---

## 📚 Available Clients

### 1. Interactive CLI (`interactive_client.py`)
**Best for**: Real-time exploration, learning, ad-hoc queries

```bash
.venv/bin/python3 interactive_client.py
```

**Features:**
- ✅ Real-time command execution
- ✅ Agent assignment
- ✅ Task management
- ✅ Team creation
- ✅ LLM queries

**Usage:**
```
teamalpha> team create
teamalpha> generate "Your prompt here"
teamalpha> assign Alice "Your task"
```

### 2. Workflow Demonstrations (`demo_workflows.py`)
**Best for**: Understanding agent patterns, batch processing

```bash
# Show full workflow (PM → Architect → Engineer → Reviewer → QA)
.venv/bin/python3 demo_workflows.py --workflow

# Show parallel task execution
.venv/bin/python3 demo_workflows.py --parallel

# Show everything
.venv/bin/python3 demo_workflows.py --all
```

### 3. HTTP Client Library (`src/teamalpha/client.py`)
**Best for**: Integration with other Python apps

```python
from src.teamalpha.client import TeamAlphaClient

client = TeamAlphaClient("http://localhost:18080")
response = client.generate("Your prompt")
print(response)
```

### 4. Direct API (FastAPI)
**Best for**: Integration with non-Python tools

```bash
# Health check
curl http://localhost:18080/health

# Generate response
curl -X POST http://localhost:18080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is AI?"}'
```

---

## 👥 Agent Roles

Each agent brings a different perspective to problems:

| Agent | Role | Specialization | Perspective |
|-------|------|-----------------|-------------|
| **Alice** | Engineer | Backend, implementation | "How do I build this?" |
| **Bob** | Code Reviewer | Quality, standards | "Is this production-ready?" |
| **Eve** | Architect | System design, patterns | "What's the big picture?" |
| **Charlie** | QA Engineer | Testing, validation | "What could break this?" |
| **Diana** | Product Manager | Requirements, strategy | "Does this solve the problem?" |

### Getting Different Perspectives
```bash
# Get technical perspective
teamalpha> assign Alice "Design user authentication"

# Get architectural perspective
teamalpha> assign Eve "Design user authentication"

# Get quality perspective
teamalpha> assign Bob "Design user authentication"

# Get testing perspective
teamalpha> assign Charlie "Design user authentication"

# Get business perspective
teamalpha> assign Diana "Design user authentication"
```

---

## 📊 Example Interactions

### Single Task with All Perspectives
```
teamalpha> team create
teamalpha> assign Alice "Build a shopping cart system"
# [Get engineer's implementation approach]

teamalpha> assign Eve "Build a shopping cart system"
# [Get architect's system design]

teamalpha> assign Bob "Review the shopping cart design"
# [Get reviewer's quality concerns]
```

### Workflow: PM → Design → Build → Review → Test
```
teamalpha> assign Diana "Define requirements for API rate limiting"
teamalpha> assign Eve "Design rate limiting architecture"
teamalpha> assign Alice "Implement rate limiting middleware"
teamalpha> assign Bob "Review rate limiting implementation"
teamalpha> assign Charlie "Create test cases for rate limiting"
```

### Direct LLM Queries
```
teamalpha> generate "Explain the difference between SQL and NoSQL"
teamalpha> generate "What are SOLID principles?"
teamalpha> generate "Design a microservices architecture"
```

---

## 🔧 Stack Management

### Start Stack
```bash
docker compose -f infrastructure/docker-compose.dev.yml up -d
```

### Stop Stack
```bash
docker compose -f infrastructure/docker-compose.dev.yml down
```

### View Logs
```bash
# All services
docker compose -f infrastructure/docker-compose.dev.yml logs -f

# Specific service
docker logs -f dev_teamalpha_agent    # Agent API
docker logs -f dev_ollama             # LLM service
```

### Check Services
```bash
# List containers
docker ps | grep dev_

# Check Ollama models
docker exec dev_ollama ollama list

# Test agent health
curl http://localhost:18080/health
```

---

## 📁 File Structure

```
teamAlpha/
├── interactive_client.py      ← Main CLI (START HERE)
├── demo_workflows.py          ← Workflow demos
├── run-client.sh              ← Bash launcher
├── setup_and_run.py           ← Python launcher
├── CLIENT_SETUP.md            ← Setup guide (THIS FILE)
├── INTERACTIVE_CLIENT.md      ← Full documentation
│
├── src/teamalpha/
│   ├── agent.py               ← Agent implementation
│   ├── team.py                ← Team orchestration
│   └── client.py              ← HTTP client library
│
├── server.py                  ← FastAPI wrapper
│
├── infrastructure/
│   ├── docker-compose.dev.yml         ← Dev stack config
│   ├── docker-compose.staging.yml     ← Staging template
│   └── Dockerfile                     ← Container definition
│
└── docs/
    ├── TEAM_GUIDE.md          ← Framework documentation
    └── DEV_RUN.md             ← Detailed stack setup
```

---

## 🎯 Common Tasks

### Task: Get an AI Team's Perspective on Your Problem

```bash
# 1. Start client
./run-client.sh

# 2. Create team
> team create

# 3. Get multiple perspectives
> assign Alice "Implement OAuth2 authentication"
> assign Eve "Design OAuth2 architecture"
> assign Bob "Review OAuth2 implementation"
> assign Charlie "Test OAuth2 flows"
> assign Diana "Define OAuth2 requirements"

# 4. Exit
> exit
```

### Task: Batch Process Multiple Questions

```bash
.venv/bin/python3 interactive_client.py << 'EOF'
team create
generate "What is machine learning?"
generate "Explain deep learning"
generate "What are neural networks?"
exit
EOF
```

### Task: Run Team Workflow

```bash
# Shows full workflow from PM requirements → Final QA tests
.venv/bin/python3 demo_workflows.py --workflow
```

---

## ⚡ Performance Notes

**Response Times (typical):**
- Health check: < 100ms
- LLM generation: 15-30 seconds (first prompt), 10-15s (subsequent)
- Agent assignment: Same as LLM generation
- Team creation: < 10ms

**Tips for faster responses:**
- Shorter prompts generate faster
- Model loads faster after first request
- Keep prompts focused and specific

---

## 🔗 Integration Examples

### Python Integration
```python
from src.teamalpha.client import TeamAlphaClient

client = TeamAlphaClient()

# Get response
response = client.generate("Your prompt", max_tokens=500)
print(response)

# Create team (local)
from src.teamalpha.team import Team
from src.teamalpha.agent import Agent, AgentRole

team = Team("My Team")
alice = Agent("Alice", AgentRole.ENGINEER)
team.add_agent(alice)
```

### Shell Integration
```bash
# Get LLM response
curl -X POST http://localhost:18080/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain REST APIs","max_tokens":200}'

# Use in shell script
RESPONSE=$(curl -s -X POST http://localhost:18080/generate \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"$PROMPT\"}")

echo $RESPONSE | jq '.response'
```

---

## 🐛 Troubleshooting

### Client won't start
```bash
# Check Python environment
which python3
.venv/bin/python3 --version

# Reinstall dependencies
uv sync

# Check containers
docker ps | grep dev_
```

### LLM not responding
```bash
# Check Ollama
docker exec dev_ollama ollama list
docker logs dev_ollama | tail -20

# Model loaded?
curl http://localhost:11435/api/tags

# Restart if needed
docker restart dev_ollama
docker exec dev_ollama ollama pull llama3
```

### Agent API errors
```bash
# Check status
curl http://localhost:18080/health

# View logs
docker logs -f dev_teamalpha_agent

# Restart
docker compose -f infrastructure/docker-compose.dev.yml restart dev_teamalpha_agent
```

---

## 📖 Next Steps

1. **Launch**: `./run-client.sh`
2. **Create Team**: `team create`
3. **Explore Agents**: `assign Alice "Your task"`
4. **Learn Patterns**: Read `INTERACTIVE_CLIENT.md`
5. **Automate**: Create Python scripts using `TeamAlphaClient`
6. **Extend**: Add new agent roles in `src/teamalpha/agent.py`

---

## 🎓 Learning Path

**Beginner**: Start with interactive client
1. `./run-client.sh`
2. `team create`
3. `assign Alice "Simple task"`
4. Explore different agents

**Intermediate**: Use client library
1. Read `src/teamalpha/client.py`
2. Create Python script
3. Experiment with batch tasks

**Advanced**: Extend framework
1. Add new agent roles
2. Implement custom workflows
3. Build integrations

---

## 📞 Support

- **Framework Issues**: Check `docs/TEAM_GUIDE.md`
- **Stack Setup**: Check `docs/DEV_RUN.md`
- **Client Usage**: Check `INTERACTIVE_CLIENT.md`
- **Errors**: Check `docker logs` for details

---

**Ready?** Start with: `./run-client.sh` 🚀

---

*Generated for TeamAlpha - Your AI Software Team*
