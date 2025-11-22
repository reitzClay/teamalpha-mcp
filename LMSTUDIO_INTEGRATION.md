# 🚀 Connect TeamAlpha Agents to LM Studio

Your agent fleet can now connect directly to LM Studio's local models. Here's how:

## ⚡ Quick Start (Windows)

### Step 1: Start LM Studio
```
• Launch LM Studio on Windows
• Load model: gpt-oss-20b-GGUF (from C:\Users\Clayt\.lmstudio\models\...)
• Verify it's running on http://localhost:1234
```

### Step 2: Connect Agents to LM Studio
```bash
python3 setup_lmstudio.py
```

This will:
1. ✅ Verify LM Studio is running
2. ✅ Check available models
3. ✅ Test agent connection
4. ✅ Start interactive client

### Step 3: Use Your Agent Fleet
```
> team create
> assign Alice "Design a REST API"
> assign Eve "Review the architecture"
> exit
```

---

## 🔌 Connection Methods

### Method 1: Environment Variables (Simplest)

```bash
# PowerShell
$env:LLM_PROVIDER = "lmstudio"
$env:LMSTUDIO_HOST = "http://localhost:1234"
python3 interactive_client.py

# CMD
set LLM_PROVIDER=lmstudio
set LMSTUDIO_HOST=http://localhost:1234
python3 interactive_client.py
```

### Method 2: Run Script (Recommended)

```bash
python3 setup_lmstudio.py
```

This handles everything automatically.

### Method 3: Direct Python

```python
from src.teamalpha.agent import Agent, AgentRole

# Create agent connected to LM Studio
agent = Agent(
    name="Alice",
    role=AgentRole.ENGINEER,
    lmstudio_host="http://localhost:1234",
    provider="lmstudio"
)

# Use agent
response = agent.think("Design a login system")
print(response)
```

---

## 📋 Files Created/Modified

### New Files
- ✅ `src/teamalpha/lmstudio.py` - LM Studio client (OpenAI-compatible API)
- ✅ `src/teamalpha/llm_config.py` - Configuration management
- ✅ `test_lmstudio.py` - Connection testing utility
- ✅ `setup_lmstudio.py` - Quick-start setup script
- ✅ `LMSTUDIO_SETUP.md` - Configuration guide

### Modified Files
- ✅ `src/teamalpha/agent.py` - Added LM Studio support
- ✅ `interactive_client.py` - Environment variable support

---

## 🧪 Test Your Connection

### Quick Test
```bash
python3 test_lmstudio.py
```

### Full Test
```bash
python3 test_lmstudio.py --all
```

### Test Generation
```bash
python3 test_lmstudio.py --test-generation
```

### Test Agent
```bash
python3 test_lmstudio.py --test-agent
```

---

## 🎯 Usage Examples

### Example 1: Get Multiple Perspectives
```bash
python3 setup_lmstudio.py

# In the interactive client:
> team create
> assign Alice "Design a REST API for e-commerce"
> assign Eve "Review the architecture"
> assign Bob "Check code quality"
> exit
```

### Example 2: Direct Agent Usage
```bash
# Create and use single agent
LLM_PROVIDER=lmstudio python3 -c "
from src.teamalpha.agent import Agent, AgentRole
agent = Agent('Alice', AgentRole.ENGINEER, provider='lmstudio')
print(agent.think('Explain REST APIs'))
"
```

### Example 3: Team Workflow
```bash
LLM_PROVIDER=lmstudio python3 demo_workflows.py --workflow
```

---

## ⚙️ Configuration

### LM Studio Default Settings
```python
base_url = "http://localhost:1234"
model = "gpt-oss-20b-GGUF"
temperature = 0.7
max_tokens = 500
timeout = 120
```

### Override Settings

#### Option 1: Environment Variables
```bash
export LMSTUDIO_HOST=http://localhost:1234
export LLM_PROVIDER=lmstudio
```

#### Option 2: Configuration File
Create `lmstudio_config.json`:
```json
{
  "provider": "lmstudio",
  "base_url": "http://localhost:1234",
  "model": "gpt-oss-20b-GGUF",
  "temperature": 0.7,
  "max_tokens": 500,
  "timeout": 120
}
```

#### Option 3: Direct Initialization
```python
agent = Agent(
    name="Alice",
    role=AgentRole.ENGINEER,
    lmstudio_host="http://localhost:1234",
    provider="lmstudio"
)
```

---

## 🔄 Switch Between Backends

### Use LM Studio
```bash
export LLM_PROVIDER=lmstudio
python3 interactive_client.py
```

### Use Ollama
```bash
export LLM_PROVIDER=ollama
python3 interactive_client.py
```

### Auto-Detect (Try LM Studio first, fallback to Ollama)
```bash
export LLM_PROVIDER=auto
python3 interactive_client.py
```

---

## 🔍 Troubleshooting

### LM Studio Not Responding

**Problem**: `Cannot connect to LM Studio at http://localhost:1234`

**Solution**:
```bash
# Check if LM Studio is running
curl http://localhost:1234/health

# Verify it's accessible
curl http://localhost:1234/v1/models
```

### Wrong Model Name

**Problem**: `Model not found in LM Studio`

**Solution**:
```bash
# List loaded models
python3 test_lmstudio.py

# Load model in LM Studio UI, then retry
```

### Timeout Errors

**Problem**: `LM Studio request timed out`

**Solution**:
```bash
# Increase timeout (in code):
agent = Agent(
    name="Alice",
    role=AgentRole.ENGINEER,
    lmstudio_host="http://localhost:1234",
    provider="lmstudio"
)
# Timeout handled internally
```

### Empty Responses

**Problem**: Agent returns empty response

**Solution**:
1. Check model is loaded in LM Studio
2. Verify LM Studio is responding: `curl http://localhost:1234/health`
3. Try: `python3 test_lmstudio.py --test-generation`

---

## 📊 Performance Tips

### For Faster Responses
```python
agent = Agent(
    "Alice",
    AgentRole.ENGINEER,
    provider="lmstudio"
)
# Reduce tokens for faster responses
response = agent.think("Your task")  # Uses default max_tokens=500
```

### For Better Quality
```python
# Use in client with longer timeout
# Quality improves with more tokens
```

### Optimize LM Studio
- Enable GPU acceleration in LM Studio settings
- Close other applications to free memory
- Use smaller models if performance is an issue

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│   Interactive Client (interactive_client.py)
│   - Command parsing
│   - Team management
│   - Detects LM Studio via environment
└────────────────┬────────────────────────────┘
                 │ LLM_PROVIDER=lmstudio
                 ▼
┌─────────────────────────────────────────────┐
│   Agent Framework (src/teamalpha/agent.py)
│   - 5 specialized roles
│   - Provider auto-detection
│   - Tool integration
└────────────────┬────────────────────────────┘
                 │ provider="lmstudio"
                 ▼
┌─────────────────────────────────────────────┐
│   LM Studio Client (src/teamalpha/lmstudio.py)
│   - HTTP requests to LM Studio API
│   - OpenAI-compatible endpoints
│   - Error handling
└────────────────┬────────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────────┐
│   LM Studio (localhost:1234)
│   - gpt-oss-20b-GGUF model
│   - Token generation
│   - Local inference
└─────────────────────────────────────────────┘
```

---

## 🎓 Learning Path

### Beginner (5 minutes)
```bash
python3 setup_lmstudio.py
```

### Intermediate (15 minutes)
```bash
# Test different agents
python3 test_lmstudio.py --all
```

### Advanced (30+ minutes)
```bash
# Create custom workflows
python3 demo_workflows.py --all
```

---

## 📝 Next Steps

1. ✅ **Start LM Studio** on Windows
2. ✅ **Load model** gpt-oss-20b-GGUF
3. ✅ **Run setup**: `python3 setup_lmstudio.py`
4. ✅ **Use agents**: `LLM_PROVIDER=lmstudio ./run-client.sh`
5. ✅ **Create team**: `team create`
6. ✅ **Assign tasks**: `assign Alice "Your task"`

---

## 📚 Related Files

- `LMSTUDIO_SETUP.md` - Detailed configuration guide
- `test_lmstudio.py` - Testing utility
- `setup_lmstudio.py` - Quick-start script
- `src/teamalpha/lmstudio.py` - LM Studio client
- `src/teamalpha/llm_config.py` - Configuration module

---

## 🎉 Ready to Go!

Your agent fleet is now ready to connect to LM Studio.

**Start with:**
```bash
python3 setup_lmstudio.py
```

**Then:**
```bash
> team create
> assign Alice "Your first task"
```

Enjoy your local AI team! 🚀
