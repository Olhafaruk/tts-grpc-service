#src/assistant/infrastructure/openai_provider.py

import os
import openai


from dotenv import load_dotenv
load_dotenv()

# Основные env-переменные
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL")
OPENAI_MODEL        = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE  = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS   = int(os.getenv("OPENAI_MAX_TOKENS", 1024))

# Конфигурируем SDK
openai.api_key = OPENAI_API_KEY
if OPENAI_API_BASE_URL:
    openai.api_base = OPENAI_API_BASE_URL

class OpenAIProvider:
    def __init__(self):
        self.model       = OPENAI_MODEL
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens  = OPENAI_MAX_TOKENS

    def generate(self, prompt: str) -> str:

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message.content

    def complete(self, prompt: str, model: str = None) -> str:

        chosen_model = model or self.model
        resp = openai.ChatCompletion.create(
            model=chosen_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message.content
