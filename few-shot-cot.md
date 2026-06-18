# CoT 推理 prompt 模板

## system
你是一个擅长数学和逻辑推理的助手。请按步骤推理，最后给出答案。

## cot_few_shot
Q: 一只鸡有 2 只脚。3 只鸡跟 1 个人共有几只脚？
A: 3 只鸡 × 2 只脚 = 6 只脚。1 个人有 2 只脚。总共 6 + 2 = 8 只脚。答案是 8。

Q: 商店里有 15 个面包。上午卖了 7 个，下午又进货 10 个，然后卖了 5 个。傍晚还剩几个？
A: 上午卖了 7 个后剩 15 - 7 = 8 个。下午进货 10 个后有 8 + 10 = 18 个。又卖了 5 个后剩 18 - 5 = 13 个。答案是 13。

## template_direct
Q: {question}
A:

## template_step_by_step
Q: {question}
A: Let's think step by step.

## template_cot_few_shot
{cot_examples}

Q: {question}
A:
