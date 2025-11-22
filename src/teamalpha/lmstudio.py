"""
LM Studio LLM Integration for TeamAlpha Agents

Connects to LM Studio local models instead of Ollama.
LM Studio typically runs on http://localhost:1234
"""

from typing import Optional
import requests
from langchain_core.language_models import LLM
from pydantic import Field


class LMStudioLLM(LLM):
    """
    LangChain LLM wrapper for LM Studio.
    
    LM Studio exposes an OpenAI-compatible API.
    Default: http://localhost:1234/v1
    """
    
    base_url: str = Field(default="http://10.5.0.2:1234/v1")
    model_name: str = Field(default="openai/gpt-oss-20b")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=500)
    timeout: int = Field(default=120)
    
    @property
    def _llm_type(self) -> str:
        return "lmstudio"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager=None,
        **kwargs
    ) -> str:
        """Generate response from LM Studio."""
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": stop or [],
            "stream": False,
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("text", "")
            
            return ""
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to LM Studio at {self.base_url}\n"
                "Make sure LM Studio is running on http://localhost:1234"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"LM Studio request timed out after {self.timeout}s\n"
                "Try increasing timeout or reducing max_tokens"
            )
        except Exception as e:
            raise RuntimeError(f"LM Studio error: {str(e)}")


class LMStudioClient:
    """Simple client for LM Studio HTTP API."""
    
    def __init__(self, base_url: str = "http://10.5.0.2:1234"):
        self.base_url = base_url
        self.api_url = f"{base_url}/v1"
    
    def health(self) -> dict:
        """Check if LM Studio is running."""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.json() if response.ok else {"status": "offline"}
        except:
            return {"status": "offline"}
    
    def list_models(self) -> list[dict]:
        """List available models in LM Studio."""
        try:
            response = requests.get(
                f"{self.api_url}/models",
                timeout=5
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            raise ConnectionError(f"Cannot connect to LM Studio: {e}")
    
    def generate(
        self,
        prompt: str,
        model: str = "openai/gpt-oss-20b",
        max_tokens: int = 500,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> str:
        """Generate text from prompt."""
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/completions",
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("text", "")
            return ""
        
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to LM Studio at {self.base_url}\n"
                f"Ensure LM Studio is running: {self.base_url}"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(f"LM Studio request timed out after {timeout}s")
        except Exception as e:
            raise RuntimeError(f"LM Studio error: {str(e)}")


# Usage example:
if __name__ == "__main__":
    # Test connection
    client = LMStudioClient()
    
    try:
        # Check health
        health = client.health()
        print(f"LM Studio Status: {health}")
        
        # List models
        models = client.list_models()
        print(f"Available Models: {models}")
        
        # Generate response
        response = client.generate("What is AI?", max_tokens=100)
        print(f"Response: {response}")
    
    except Exception as e:
        print(f"Error: {e}")
