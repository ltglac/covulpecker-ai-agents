"""
Configuration loader for CoVulPecker.

Handles loading environment variables and model configuration.
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM


# Load environment variables
load_dotenv()


class Config:
    """Configuration manager for CoVulPecker."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # API Keys
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Model Configuration
        self.llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
        
        # Model Parameters
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        
        # Application Settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.output_format = os.getenv("OUTPUT_FORMAT", "json")
        
        # Paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"
        self.outputs_dir = self.base_dir / "outputs"
        self.tmp_dir = self.base_dir / "tmp"
        
        # Create directories if they don't exist
        for directory in [self.data_dir, self.logs_dir, self.outputs_dir, self.tmp_dir]:
            directory.mkdir(exist_ok=True)
    
    def get_llm(self, temperature: Optional[float] = None) -> Any:
        """
        Get the configured LLM instance based on the provider.
        
        Args:
            temperature: Override default temperature (optional)
            
        Returns:
            LLM instance for the configured provider
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        temp = temperature if temperature is not None else self.temperature
        
        if self.llm_provider == "gemini":
            if not self.gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            # For Google AI Studio (not Vertex AI), we need to explicitly set the provider
            # LiteLLM will use the correct endpoint with this configuration
            import os
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key
            return LLM(
                model=f"gemini/{self.gemini_model}",
                temperature=temp,
                max_tokens=self.max_tokens
            )
        
        elif self.llm_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            return LLM(
                model=self.openai_model,
                api_key=self.openai_api_key,
                temperature=temp,
                max_tokens=self.max_tokens
            )
        
        elif self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            return LLM(
                model=self.anthropic_model,
                api_key=self.anthropic_api_key,
                temperature=temp,
                max_tokens=self.max_tokens
            )
        
        else:
            raise ValueError(
                f"Unsupported LLM provider: {self.llm_provider}. "
                "Supported providers: gemini, openai, anthropic"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary (without sensitive data).
        
        Returns:
            Configuration dictionary
        """
        return {
            "llm_provider": self.llm_provider,
            "model": getattr(self, f"{self.llm_provider}_model"),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "log_level": self.log_level,
            "output_format": self.output_format
        }


# Global configuration instance
config = Config()
