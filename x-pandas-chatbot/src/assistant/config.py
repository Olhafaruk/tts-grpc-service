#config.py

import os
from loguru import logger

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8085")
SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "python:3.10-slim")

logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="INFO")
