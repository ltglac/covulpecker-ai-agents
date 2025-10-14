#!/usr/bin/env python3
"""
Quick test script to verify LLM configuration.
Run this after activating .venv to test if the LLM setup works.
"""

import sys
sys.path.insert(0, '/Users/macbook/Documents/personal/covul/ai-agents')

from src.utils.config import config

print("=" * 60)
print("Testing LLM Configuration")
print("=" * 60)

try:
    print(f"\nLLM Provider: {config.llm_provider}")
    print(f"Model: {config.gemini_model}")
    print(f"API Key: {config.gemini_api_key[:10]}..." if config.gemini_api_key else "NOT SET")
    
    print("\nCreating LLM instance...")
    llm = config.get_llm()
    print(f"✅ LLM created successfully!")
    print(f"Model type: {type(llm)}")
    print(f"Model name in LLM: {llm.model}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
