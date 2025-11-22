"""
LLM Configuration Module

Switch between different LLM backends:
- Ollama (localhost:11435)
- LM Studio (localhost:1234)
- Custom endpoints
"""

from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Available LLM providers."""
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"
    CUSTOM = "custom"


class OllamaConfig(BaseModel):
    """Ollama configuration."""
    provider: str = "ollama"
    base_url: str = "http://localhost:11435"
    model: str = "llama3"
    temperature: float = 0.7
    max_tokens: int = 500
    timeout: int = 120


class LMStudioConfig(BaseModel):
    """LM Studio configuration."""
    provider: str = "lmstudio"
    base_url: str = "http://10.5.0.2:1234"
    model: str = "gpt-oss-20b"
    temperature: float = 0.7
    max_tokens: int = 500
    timeout: int = 120


class CustomConfig(BaseModel):
    """Custom LLM endpoint configuration."""
    provider: str = "custom"
    base_url: str = Field(..., description="Full API endpoint URL")
    model: str = Field(..., description="Model name")
    temperature: float = 0.7
    max_tokens: int = 500
    timeout: int = 120
    api_key: Optional[str] = None


class LLMConfig(BaseModel):
    """Main LLM configuration."""
    provider: LLMProvider = LLMProvider.OLLAMA
    ollama: OllamaConfig = OllamaConfig()
    lmstudio: LMStudioConfig = LMStudioConfig()
    custom: Optional[CustomConfig] = None
    
    def get_config(self) -> Union[OllamaConfig, LMStudioConfig, CustomConfig]:
        """Get active configuration based on provider."""
        if self.provider == LLMProvider.OLLAMA:
            return self.ollama
        elif self.provider == LLMProvider.LMSTUDIO:
            return self.lmstudio
        elif self.provider == LLMProvider.CUSTOM:
            if self.custom is None:
                raise ValueError("Custom provider selected but no custom config provided")
            return self.custom
        else:
            raise ValueError(f"Unknown provider: {self.provider}")


# Default configurations
DEFAULT_OLLAMA = OllamaConfig()
DEFAULT_LMSTUDIO = LMStudioConfig()

# Environment-aware defaults
import os

if os.getenv("LLM_PROVIDER") == "lmstudio":
    DEFAULT_CONFIG = LLMConfig(provider=LLMProvider.LMSTUDIO)
elif os.getenv("LLM_PROVIDER") == "ollama":
    DEFAULT_CONFIG = LLMConfig(provider=LLMProvider.OLLAMA)
else:
    # Auto-detect: Try LM Studio first, fallback to Ollama
    DEFAULT_CONFIG = LLMConfig(provider=LLMProvider.OLLAMA)


def get_default_config() -> LLMConfig:
    """Get default LLM configuration."""
    return DEFAULT_CONFIG
