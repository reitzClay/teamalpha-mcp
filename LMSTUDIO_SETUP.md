# LM Studio Configuration for TeamAlpha

This directory contains configuration for using LM Studio as the LLM backend for TeamAlpha agents.

## Quick Start

### 1. Set Environment Variable

```bash
# Windows (PowerShell)
$env:LLM_PROVIDER = "lmstudio"
$env:LMSTUDIO_HOST = "http://localhost:1234"

# Windows (CMD)
set LLM_PROVIDER=lmstudio
set LMSTUDIO_HOST=http://localhost:1234

# Linux/Mac
export LLM_PROVIDER=lmstudio
export LMSTUDIO_HOST=http://localhost:1234
```

### 2. Test Connection

```bash
.venv/bin/python3 test_lmstudio.py --all
```

### 3. Use with Agents

```bash
# Interactive client with LM Studio
LLM_PROVIDER=lmstudio ./run-client.sh

# Or direct Python
LLM_PROVIDER=lmstudio .venv/bin/python3 interactive_client.py
```

## Configuration Methods

### Method 1: Environment Variables (Recommended)

```bash
export LLM_PROVIDER=lmstudio
export LMSTUDIO_HOST=http://localhost:1234
```

Supported variables:
- `LLM_PROVIDER` - "lmstudio", "ollama", or "auto"
- `LMSTUDIO_HOST` - LM Studio URL (default: http://localhost:1234)

### Method 2: Python Configuration File

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

### Method 3: Direct Agent Initialization

```python
from src.teamalpha.agent import Agent, AgentRole

agent = Agent(
    name="Alice",
    role=AgentRole.ENGINEER,
    lmstudio_host="http://localhost:1234",
    provider="lmstudio"
)
```

## MCP Configuration

Your `mcp.json` shows Docker MCP server configuration. To use with LM Studio locally:

```json
{
  "mcpServers": {
    "lmstudio": {
      "type": "stdio",
      "command": "python3",
      "args": ["src/teamalpha/lmstudio.py"]
    }
  }
}
```

## Troubleshooting

### LM Studio Not Responding

```bash
# Check if LM Studio is running
curl http://localhost:1234/health

# List loaded models
curl http://localhost:1234/v1/models

# Check LM Studio logs for errors
```

### Wrong Model Name

Ensure the model name matches exactly:

```bash
# Check available models
python3 test_lmstudio.py

# List models in LM Studio API
curl http://localhost:1234/v1/models | python3 -m json.tool
```

### Connection Timeout

Increase timeout in configuration:

```python
agent = Agent(
    name="Alice",
    role=AgentRole.ENGINEER,
    lmstudio_host="http://localhost:1234",
    provider="lmstudio",
)
# Timeout is handled internally, set in llm_config.py if needed
```

## Performance Tips

1. **Model Size**: GPT-OSS-20B works well. Larger models are slower.
2. **GPU Acceleration**: Configure in LM Studio settings
3. **Token Limits**: Reduce max_tokens for faster responses
4. **Temperature**: Lower values (0.3-0.5) for more deterministic responses

## Files

- `src/teamalpha/lmstudio.py` - LM Studio client and LangChain wrapper
- `src/teamalpha/llm_config.py` - Configuration management
- `test_lmstudio.py` - Connection testing utility

## Switching Providers

Switch between Ollama and LM Studio:

```bash
# Use LM Studio
export LLM_PROVIDER=lmstudio
./run-client.sh

# Use Ollama
export LLM_PROVIDER=ollama
./run-client.sh

# Auto-detect (tries LM Studio first)
export LLM_PROVIDER=auto
./run-client.sh
```

## Next Steps

1. Start LM Studio on Windows
2. Load gpt-oss-20b model in LM Studio
3. Run: `python3 test_lmstudio.py --all`
4. Use: `LLM_PROVIDER=lmstudio ./run-client.sh`

---

For more information, see the main README and documentation files.
