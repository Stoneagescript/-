"""汉北本地“小龙虾”智能体命令行入口。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from agent.workflow import WorkflowRouter


ROOT = Path(__file__).resolve().parent


def load_config(path: str | Path = "config.yaml") -> dict[str, Any]:
    """Load YAML config. Fall back to config.example.yaml when config.yaml is absent."""
    config_path = ROOT / path
    if not config_path.exists():
        config_path = ROOT / "config.example.yaml"

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="汉北本地小龙虾智能体 v1")
    parser.add_argument(
        "--task",
        default="content",
        choices=["content", "sales", "customer", "image", "code", "management"],
        help="任务类型：content/sales/customer/image/code/management",
    )
    parser.add_argument("--input", required=True, help="本次任务需求")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    router = WorkflowRouter(config=config, root=ROOT)
    result = router.run(task=args.task, user_input=args.input)
    print(result)


if __name__ == "__main__":
    main()
