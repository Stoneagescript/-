"""基础工具函数：模型调用、提示词加载、输出保存。"""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Any

import requests


class AgentToolError(RuntimeError):
    """Raised when a local agent tool fails."""


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_output(root: Path, task: str, content: str) -> Path:
    output_dir = root / "outputs" / task
    ensure_dir(output_dir)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"{timestamp}.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def call_openai_compatible(config: dict[str, Any], messages: list[dict[str, str]]) -> str:
    """Call OpenAI-compatible chat completion API.

    The API key is read from environment variable declared in config, not from repo files.
    """
    model_config = config.get("model", {})
    base_url = model_config.get("base_url", "https://api.deepseek.com").rstrip("/")
    api_key_env = model_config.get("api_key_env", "DEEPSEEK_API_KEY")
    api_key = os.getenv(api_key_env)

    if not api_key:
        raise AgentToolError(f"缺少环境变量：{api_key_env}")

    payload = {
        "model": model_config.get("model_name", "deepseek-chat"),
        "messages": messages,
        "temperature": model_config.get("temperature", 0.7),
        "max_tokens": model_config.get("max_tokens", 2000),
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
