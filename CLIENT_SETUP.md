# TeamAlpha Interactive Client - Complete Setup

## ✅ What's Ready

### 1. Running Services
```
dev_ollama           → localhost:11435 (LLM inference)
dev_teamalpha_agent  → localhost:18080 (Agent API)
```

### 2. Interactive Client Files
- **`interactive_client.py`** - Main CLI for agent interaction
- **`run-client.sh`** - Bash launcher script
- **`setup_and_run.py`** - Python setup with model waiting

### 3. Agent Team (5 Members)
- **Alice** (Engineer) - Technical implementation
- **Bob** (Code Reviewer) - Quality assurance & reviews
- **Eve** (Architect) - System design & patterns  
- **Charlie** (QA Engineer) - Testing & validation
- **Diana** (Product Manager) - Strategy & requirements

---

## 🚀 Launch Options

### **Option 1: Quick Start (Recommended)**
```bash
./run-client.sh
# or
.venv/bin/python3 interactive_client.py
```

### **Option 2: With Model Status Checker**
```bash
.venv/bin/python3 setup_and_run.py
```

---

## 📝 Commands Inside Client

```
status              → Check agent health ✅
team create         → Create 5-agent team 👥
agents              → List team members 📋
generate <prompt>   → Send to LLM 🤖
assign <name> <task>→ Assign to specific agent 🎯
help                → Show all commands 📚
exit                → Quit client 👋
```

---

## 💡 Usage Examples

### Create Team & Check Status
```bash
teamalpha> team create
teamalpha> agents
teamalpha> status
```

### Send Task to Specific Agent
```bash
teamalpha> assign Alice "Create a Python FastAPI endpoint for user login"
teamalpha> assign Eve "Design the database schema"
teamalpha> assign Bob "Review the implementation"
```

### Query LLM Directly
```bash
teamalpha> generate "Explain how REST APIs work"
teamalpha> generate "Write a Python decorator for authentication"
```

---

## ⏳ Model Status

**llama3 is downloading** (~4.7GB, ~2-5 minutes on typical connection)

### Monitor Download
```bash
# Check if model is ready
docker exec dev_ollama ollama list

# View download progress
docker logs dev_ollama | tail -20

# Restart if stuck
docker restart dev_ollama
```

### While Waiting
✅ You can still run these commands:
- `status` - Check agent health
- `team create` - Set up team
- `agents` - List agents
- `help` - Show help

❌ These will fail until model loads:
- `generate <prompt>` - Requires LLM
- `assign <name> <task>` - Requires LLM

---

## 🐳 Container Commands

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
docker logs -f dev_teamalpha_agent    # Agent server
docker logs -f dev_ollama             # LLM service
```

### Force Model Download
```bash
docker exec dev_ollama ollama pull llama3
```

---

## 🔍 Troubleshooting

### Client Won't Connect
```bash
# Verify containers running
docker ps | grep dev_

# Restart stack
docker compose -f infrastructure/docker-compose.dev.yml restart

# Check agent logs
docker logs dev_teamalpha_agent
```

### LLM Errors After Generate
```bash
# Model still downloading? Check:
docker exec dev_ollama ollama list

# Manual pull if needed:
docker exec dev_ollama ollama pull llama3

# Check model loaded:
curl http://localhost:11435/api/tags
```

### Import/Dependency Errors
```bash
# Reinstall Python dependencies
uv sync

# Verify venv
ls -la .venv/bin/python3
```

---

## 📚 File Structure

```
interactive_client.py    ← Main client (START HERE)
run-client.sh           ← Bash launcher
setup_and_run.py        ← Python launcher with model wait
INTERACTIVE_CLIENT.md   ← Full documentation
CLIENT_SETUP.md         ← This file

src/teamalpha/
  ├── agent.py          ← Agent class & LLM integration
  ├── team.py           ← Team orchestration
  └── client.py         ← HTTP client library

server.py               ← FastAPI wrapper (running)
```

---

## 🎯 Next Steps

1. **Start Client** → `./run-client.sh`
2. **Create Team** → `team create`
3. **Check Status** → `status`
4. **Try Assignment** → `assign Alice "Design an API"`
5. **Monitor Logs** → `docker logs -f dev_ollama`
6. **Query LLM** → `generate "Your prompt"`

---

## 📊 Current State

| Component | Status | Port | Notes |
|-----------|--------|------|-------|
| Ollama | ✅ Running | 11435 | Model downloading |
| Agent API | ✅ Running | 18080 | Health: OK |
| Client | ✅ Ready | N/A | Use ./run-client.sh |
| Team | ✅ Ready | N/A | 5 agents configured |

---

## 🔗 Related Files

- **Full Documentation**: `INTERACTIVE_CLIENT.md`
- **Framework Guide**: `docs/TEAM_GUIDE.md`
- **Stack Setup**: `docs/DEV_RUN.md`
- **Project Structure**: `STRUCTURE_GUIDE.md`

---

**Ready to go! Launch with:** `./run-client.sh`
