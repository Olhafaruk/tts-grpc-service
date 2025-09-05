import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(dotenv_path=".env")


print("API KEY:", os.getenv("OPENAI_API_KEY"))
print("DEBUG:", os.getenv("DEBUG_ENV"))
print("FOUND ENV:", find_dotenv())
