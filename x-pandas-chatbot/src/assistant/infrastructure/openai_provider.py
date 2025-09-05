# src/assistant/infrastructure/openai_provider.py

import logging
import os

import openai

logger = logging.getLogger(__name__)


class OpenAIProvider:
    def __init__(self, api_key: str = None):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
        self.top_p = float(os.getenv("OPENAI_TOP_P", 1.0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 256))

    def complete(self, prompt: str, model: str = None) -> str:
        logger.info(
            f"Calling OpenAI model '{model or self.model}'"
            f" with prompt: {prompt[:100]}..."
        )

        try:
            response = openai.ChatCompletion.create(
                model=model or self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                stop=None,
            )
            return response.choices[0].message["content"]
        except openai.OpenAIError as e:
            logger.error(f"OpenAI call failed: {e}")
            raise RuntimeError(f"OpenAI call failed: {e}")
