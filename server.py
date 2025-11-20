#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_ollama import OllamaLLM
import os

app = FastAPI(title="TeamAlpha LLM Proxy")

# Read OLLAMA_HOST from environment or use default
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
llm = OllamaLLM(model="llama3", base_url=OLLAMA_HOST)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512

class GenerateResponse(BaseModel):
    text: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")
    try:
        # Use the OllamaLLM invoke method
        result = llm.invoke(req.prompt)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_ollama import OllamaLLM
import os

app = FastAPI(title="TeamAlpha LLM Proxy")

# Read OLLAMA_HOST from environment or use default
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
llm = OllamaLLM(model="llama3", base_url=OLLAMA_HOST)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 512

class GenerateResponse(BaseModel):
    text: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="prompt is required")
    try:
        # Use the OllamaLLM invoke method
        result = llm.invoke(req.prompt)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
