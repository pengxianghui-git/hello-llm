# 中文文本分类 prompt 模板

## system
你是一位中文文本分析助手。收到 input 后，只输出分类标签、不要输出其他文字。

## user
对以下文本进行分类。分类规则参见示例。

## examples
input: 这家餐厅的牛排好吃到让我哭出来。
output: 正面 / 美食

input: 服务生态度很差、我再也不会来了。
output: 负面 / 客服

input: 这家店位于新北市三重区、营业时间每天 11:00–21:00。
output: 中立 / 资讯

## template
{examples}
input: {text}
output:

## template_zero_shot
input: {text}
output:
