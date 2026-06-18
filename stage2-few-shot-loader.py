"""
stage2-few-shot-loader.py

演示「prompt md 文件 + prompt_loader.py」的完整工作流。

关键区别：
  - prompt 内容来自 few-shot-prompt-for-codex.md（可编辑，不动代码）
  - prompt_loader.py 负责读取和渲染
  - 调用方只管传 text + 参数的开关
"""

import sys, os
from anthropic import Anthropic
from dotenv import load_dotenv
from prompt_loader import PromptTemplate

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

# 从 md 文件加载 prompt，不硬编码
prompt = PromptTemplate("few-shot-prompt-for-codex.md")

client = Anthropic(
    base_url="https://api.deepseek.com/anthropic",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

TEST_SET = [
    ("这部电影超赞、看完想再看一次！", "正面"),
    ("剧情无聊、演员演技尴尬。", "负面"),
    ("这是一部 2019 年的电影。", "中立"),
    ("我不确定喜不喜欢、可能再想想。", "中立"),
    ("第一集很不错但第二集就崩了。", "负面"),
    ("看完心情很好、推荐！", "正面"),
]


def classify(text: str, *, use_few_shot: bool) -> str:
    msg = client.messages.create(
        model="deepseek-v4-flash",
        max_tokens=200,
        system=prompt.system,
        messages=prompt.render_messages(text, use_few_shot=use_few_shot),
    )
    for block in msg.content:
        if block.type == "text":
            return block.text.strip().splitlines()[0]
    return ""


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正确 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正确 {c3}/{_} = {c3/_:.0%}")

assert c3 >= c0, f"预期 3-shot 不比 0-shot 差、实际 {c3} < {c0}"
print(f"\n✅ 通过 — 0-shot {c0}/{n}、3-shot {c3}/{n}")
print("💡 prompt 来源：few-shot-prompt-for-codex.md（不动代码，改 md 即可换 prompt）")
