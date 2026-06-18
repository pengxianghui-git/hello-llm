from anthropic import Anthropic
from dotenv import load_dotenv
import sys, statistics

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os

load_dotenv()

client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

PROMPTS = {
    "中文": "用一句话描述一只猫在做什么。",
    "English": "Describe in one sentence what a cat is doing.",
}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(
            model="deepseek-v4-flash",
            max_tokens=1000,
            temperature=1.0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(msg.usage.output_tokens)
    print(
        f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}"
    )

# === 自我验证 ===
assert max(output_tokens) > min(
    output_tokens
), "temperature=1.0 下、output 长度应该有 variance"
print("\n✅ 练习 2 通过 — 本机跑 $0")
print(
    "💡 中文 prompt 通常 input tokens 比 English 多（中文 token 化通常一字 ≈ 2 tokens）"
)
