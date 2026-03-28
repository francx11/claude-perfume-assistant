# prueba.py
import os
from dotenv import load_dotenv
from src.api.claude_client import ClaudeClient

load_dotenv()

client = ClaudeClient(api_key=os.getenv("ANTHROPIC_API_KEY"))

messages = [{"role": "user", "content": "Hola, dime un perfume famoso"}]
response = client.send_message(messages)

print(response["content"][0]["text"])
