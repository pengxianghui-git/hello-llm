import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}
USER_MSG = "请帮我解释什么是租赁合约。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
     msg = client.messages.create(
         model="deepseek-v4-flash",
         max_tokens=1000,
         system=system,
         messages=[{"role": "user", "content": USER_MSG}],
     )
     for block in msg.content:
         if block.type == "text":
             outputs[label] = block.text
             break
     print(f"\n--- [{label}] ---")
     print(outputs[label])

# 同样的 JSON assert（schema 跨 backend 通用）
json_output = outputs["JSON 机器"]
assert "{" in json_output and "}" in json_output
print(f"\n✅ 练习 1 通过（Anthropic）")
