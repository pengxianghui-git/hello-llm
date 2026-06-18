from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

msg = client.messages.create(
    model="deepseek-v4-flash",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "用一句话自我介绍。"}],
        }
    ],
)

for block in msg.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "thinking":
        print("Thinking:", block.thinking[:200], "...")
