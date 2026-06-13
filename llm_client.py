"""Unified LLM Client for model-specific generation and translation."""

import os
import openai
import httpx
from typing import Optional, Dict, Any, List
import logging
from dataclasses import dataclass
from enum import Enum

from env_config import load_project_env

load_project_env()

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    ANTHROPIC = "anthropic"


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    provider: LLMProvider
    model_id: str
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.95
    frequency_penalty: float = 0.3
    presence_penalty: float = 0.3


# Model configurations
MODEL_CONFIGS = {
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        provider=LLMProvider.OPENAI,
        model_id="gpt-4o",
        temperature=0.7,
        max_tokens=2000
    ),
    "claude-3.5-sonnet": ModelConfig(
        name="claude-3.5-sonnet",
        provider=LLMProvider.ANTHROPIC,
        model_id=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        temperature=0.7,
        max_tokens=2000
    ),
    "deepseek-chat": ModelConfig(
        name="deepseek-chat",
        provider=LLMProvider.OPENROUTER,
        model_id="deepseek/deepseek-chat",
        temperature=0.7,
        max_tokens=2000
    )
}


class UnifiedLLMClient:
    """
    Unified client for accessing different LLM providers.
    Supports OpenAI direct API and OpenRouter.
    """
    
    def __init__(self, model_name: str):
        """
        Initialize client for a specific model.
        
        Args:
            model_name: Name of the model (gpt-4o, claude-3.5-sonnet, deepseek-chat)
        """
        if model_name not in MODEL_CONFIGS:
            raise ValueError(f"Unknown model: {model_name}. Available models: {list(MODEL_CONFIGS.keys())}")
        
        self.config = MODEL_CONFIGS[model_name]
        self.client = self._initialize_client()
        
        logger.info(f"Initialized {self.config.provider.value} client for model {model_name}")
    
    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.config.provider == LLMProvider.OPENAI:
            # Direct OpenAI API
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            return openai.OpenAI(api_key=api_key)
        
        elif self.config.provider == LLMProvider.OPENROUTER:
            # OpenRouter API
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable not set")
            
            return openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

        elif self.config.provider == LLMProvider.ANTHROPIC:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")

            return httpx.Client(
                base_url="https://api.anthropic.com/v1",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=120.0,
            )
        
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    async def generate_completion(self, 
                                prompt: str,
                                temperature: Optional[float] = None,
                                max_tokens: Optional[int] = None) -> str:
        """
        Generate a completion using the configured model.
        
        Args:
            prompt: The prompt to send to the model
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            The model's response text
        """
        try:
            # Use provided values or defaults from config
            temp = temperature if temperature is not None else self.config.temperature
            max_tok = max_tokens if max_tokens is not None else self.config.max_tokens
            
            if self.config.provider == LLMProvider.ANTHROPIC:
                response = self.client.post(
                    "/messages",
                    json={
                        "model": self.config.model_id,
                        "max_tokens": max_tok,
                        "temperature": temp,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                )
                response.raise_for_status()
                payload = response.json()
                result = "".join(
                    block.get("text", "") for block in payload.get("content", []) if block.get("type") == "text"
                )
            else:
                # Prepare messages (stateless, no system prompt)
                messages = [{"role": "user", "content": prompt}]
                
                # Make the API call
                response = self.client.chat.completions.create(
                    model=self.config.model_id,
                    messages=messages,
                    temperature=temp,
                    max_tokens=max_tok,
                    top_p=self.config.top_p,
                    frequency_penalty=self.config.frequency_penalty,
                    presence_penalty=self.config.presence_penalty
                )
                
                result = response.choices[0].message.content
            
            logger.info(f"Generated response using {self.config.name} "
                       f"(provider: {self.config.provider.value}, temp: {temp})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating completion with {self.config.name}: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration."""
        return {
            "name": self.config.name,
            "provider": self.config.provider.value,
            "model_id": self.config.model_id,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "frequency_penalty": self.config.frequency_penalty,
            "presence_penalty": self.config.presence_penalty
        }


def get_available_models() -> List[str]:
    """Get list of available model names."""
    return list(MODEL_CONFIGS.keys())


def validate_environment():
    """Validate that required environment variables are set."""
    errors = []
    
    # Check for OpenAI API key if using gpt-4o
    if "gpt-4o" in MODEL_CONFIGS and not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY environment variable not set (required for gpt-4o)")
    
    # Check for Anthropic API key if using Anthropic direct
    anthropic_models = [m for m, c in MODEL_CONFIGS.items() if c.provider == LLMProvider.ANTHROPIC]
    if anthropic_models and not os.getenv("ANTHROPIC_API_KEY"):
        errors.append("ANTHROPIC_API_KEY environment variable not set "
                     f"(required for {', '.join(anthropic_models)})")

    # Check for OpenRouter API key if using other models
    openrouter_models = [m for m, c in MODEL_CONFIGS.items() 
                        if c.provider == LLMProvider.OPENROUTER]
    if openrouter_models and not os.getenv("OPENROUTER_API_KEY"):
        errors.append("OPENROUTER_API_KEY environment variable not set "
                     f"(required for {', '.join(openrouter_models)})")
    
    if errors:
        raise EnvironmentError("\n".join(errors))
    
    logger.info("Environment validation passed")


if __name__ == "__main__":
    # Test the client
    import asyncio
    
    async def test_client():
        # Validate environment first
        validate_environment()
        
        # Test with each model
        for model_name in get_available_models():
            print(f"\nTesting {model_name}...")
            try:
                client = UnifiedLLMClient(model_name)
                response = await client.generate_completion(
                    "What is 2+2? Answer in one word."
                )
                print(f"Response: {response}")
                print(f"Model info: {client.get_model_info()}")
            except Exception as e:
                print(f"Error with {model_name}: {e}")
    
    asyncio.run(test_client())
