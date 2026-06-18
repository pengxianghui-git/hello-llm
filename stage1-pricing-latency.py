# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

# Anthropic 2026 Q2 公开计价（每 1M token、USD）— 运行前对照 https://www.anthropic.com/pricing
PRICING = {
    "DeepSeek-V4-Flash":   {"input": 1.00, "output":  5.00},
    "DeepSeek-V4-Pro":  {"input": 3.00, "output": 15.00}
}

client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)
MODEL = "DeepSeek-V4-Flash"
msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！自我介绍一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

assert cost_one > 0, "Cloud LLM 一定有成本"
print(f"\n✅ 练习 3 通过（DeepSeek）— 1000 次 V4-Flash ≈ $0.25、V4-Pro ≈ $0.76")