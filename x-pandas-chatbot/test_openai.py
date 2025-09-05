import os

from openai import OpenAI

print("API KEY:", os.getenv("OPENAI_API_KEY"))


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Привет!"}]
)
print(resp.choices[0].message.content)
