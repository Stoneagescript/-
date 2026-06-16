"""小龙虾任务路由与工作流模板。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .tools import call_openai_compatible, read_text, save_output


TASK_GUIDES = {
    "content": "你现在处理内容生产任务。输出要适合公众号、小红书、短视频、海报或产品介绍。复杂内容按标题、正文、卖点、CTA拆分。",
    "sales": "你现在处理销售跟进任务。输出要像真人微信沟通，短、准、自然，避免过度营销。必要时给3个语气版本。",
    "customer": "你现在处理客户资料整理任务。请提取客户行业、需求、预算/数量、阶段、风险、下一步动作。",
    "image": "你现在处理图片生成任务。请输出中文画面说明、英文提示词、负面提示词、画幅建议和检查点。",
    "code": "你现在处理代码开发任务。请给可运行代码、配置说明、测试方法和常见错误排查。",
    "management": "你现在处理内部管理任务。请输出SOP、清单、表格结构、责任人和下一步动作。",
}


class WorkflowRouter:
    def __init__(self, config: dict[str, Any], root: Path) -> None:
        self.config = config
        self.root = root

    def build_messages(self, task: str, user_input: str) -> list[dict[str, str]]:
        prompt_path = self.root / self.config.get("paths", {}).get("system_prompt", "agent/system_prompt.md")
        system_prompt = read_text(prompt_path)
        guide = TASK_GUIDES.get(task, TASK_GUIDES["content"])

        return [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": guide},
            {"role": "user", "content": user_input},
        ]

    def run(self, task: str, user_input: str) -> str:
        messages = self.build_messages(task=task, user_input=user_input)
        content = call_openai_compatible(self.config, messages)

        if self.config.get("workflow", {}).get("save_outputs", True):
            saved_path = save_output(self.root, task, content)
            return f"{content}\n\n---\n已保存：{saved_path}"

        return content
