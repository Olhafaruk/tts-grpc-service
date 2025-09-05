# src/assistant/config.py

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 1024))

# GPT_LLM_API_TOKEN = os.getenv("GPT_LLM_API_TOKEN")
# GPT_LLM_NAME      = os.getenv("GPT_LLM_NAME", "gpt-3.5-turbo")
# GPT_LLM_BASE_URL  = os.getenv("GPT_LLM_BASE_URL", "https://api.openai.com/v1")

# GPT_LLM_TEMPERATURE = float(os.getenv("GPT_LLM_TEMPERATURE", 0.7))
# GPT_LLM_MAX_TOKENS  = int(os.getenv("GPT_LLM_MAX_TOKENS", 1024))


WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "python:3.10-slim")
SANDBOX_MEMORY = os.getenv("SANDBOX_MEMORY_LIMIT", "512m")
SANDBOX_CPU = os.getenv("SANDBOX_CPU_LIMIT", "0.5")


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
