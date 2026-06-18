import sys, os
from anthropic import Anthropic
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()
client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# 5 个 iteration、每一轮 prompt 都比前一轮更具体
PROMPTS = {
    "v1 模糊": "写一段介紹 ReAct 的文字。",
    "v2 加目标读者": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。",
    "v3 加格式": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落。",
    "v4 加 example 要求": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落、结尾举一个具体例子（譬如查天气）。",
    "v5 加禁忌": "写一段介紹 ReAct 的文字、给写过 Python 的软体工程师看。100 字以內、用一个段落、结尾举一个具体例子（譬如查天气）。不要用「賦能」「驅动」「智能」这類空泛词彙。",
}

outputs = {}
for label, prompt in PROMPTS.items():
     msg = client.messages.create(
         model="deepseek-v4-flash",
         max_tokens=1000,
         messages=[{"role": "user", "content": prompt}],
     )
     for block in msg.content:
         if block.type == "text":
             outputs[label] = block.text
             break
     print(f"\n--- [{label}] ({len(outputs[label])} chars) ---")
     print(outputs[label])

# === 自我验证 ===
v1_len, v5_len = len(outputs["v1 模糊"]), len(outputs["v5 加禁忌"])
banned_words = ("賦能", "驅动", "智能")
v5_has_banned = any(w in outputs["v5 加禁忌"] for w in banned_words)
assert v5_len > 0, "v5 必須有输出"
assert not v5_has_banned, f"v5 应该避免禁忌词、实际含: {[w for w in banned_words if w in outputs['v5 加禁忌']]}"
print(f"\n✅ 练习 4 通过 — v5 长度 {v5_len}、无禁忌词（本机 $0）")
print(f"💡 观察：v1 ({v1_len} chars) 通常比 v5 ({v5_len} chars) 「鬆」、加约束会逼 prompt 收斂")
print("💡 用 gemma4:e4b 跑这题特别有感——小 model 对 prompt 质量极敏感、5 轮 refine 的差距会比 Claude 更明显")