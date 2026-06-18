"""
prompt_loader.py — 从 markdown 模板加载 prompt 组件

用法:
    prompt = PromptTemplate("few-shot-prompt-for-codex.md")
    prompt.system       # → "你是一位中文文本分析助手..."
    prompt.user         # → "对以下文本进行分类。..."
    prompt.examples     # → "input: ...\\noutput: ...\\n..."
    prompt.render(text="你好", use_few_shot=True)
        # → "{examples}\\ninput: 你好\\noutput:"
    prompt.render(text="你好", use_few_shot=False)
        # → "input: 你好\\noutput:"
"""

import re
from pathlib import Path


class PromptTemplate:
    """从 markdown 文件加载 prompt 模板并渲染。"""

    def __init__(self, path: str | Path) -> None:
        text = Path(path).read_text(encoding="utf-8")
        self._raw = text
        self.system = self._extract("system")
        self.user = self._extract("user")
        self.examples = self._extract("examples")
        self._template = self._extract("template")
        self._template_zs = self._extract("template_zero_shot")

    def _extract(self, section: str) -> str:
        """提取 ## {section} 下面的内容，到下一个 ## 或文件结尾。"""
        m = re.search(
            rf"^##\s+{re.escape(section)}\s*\n(.+?)(?=\n##\s|\Z)",
            self._raw,
            re.DOTALL | re.MULTILINE,
        )
        if not m:
            raise KeyError(f"section '## {section}' not found in prompt file")
        return m.group(1).strip()

    def render(self, text: str, *, use_few_shot: bool = True) -> str:
        """渲染完整的 user message content。"""
        tmpl = self._template if use_few_shot else self._template_zs
        return tmpl.format(examples=self.examples, text=text)

    def render_messages(self, text: str, *, use_few_shot: bool = True) -> list[dict]:
        """返回 [{"role": "user", "content": ...}]，可直接丢给 client.messages.create。"""
        content = self.render(text, use_few_shot=use_few_shot)
        return [{"role": "user", "content": content}]

    def __repr__(self) -> str:
        return f"<PromptTemplate sections=[system, user, examples, template, template_zero_shot]>"


if __name__ == "__main__":
    # 快速验证
    pt = PromptTemplate("few-shot-prompt-for-codex.md")
    print(f"system:      {pt.system!r}")
    print(f"user:        {pt.user!r}")
    print(f"examples:    {pt.examples!r}")
    print("---")
    print(pt.render("看完心情很好、推荐！"))
    print("---")
    print(pt.render("看完心情很好、推荐！", use_few_shot=False))
