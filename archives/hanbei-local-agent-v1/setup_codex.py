"""Generate a short handoff file for Codex or another coding agent."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent

CODEX_GUIDE = """# Codex 开发说明

你正在维护汉北本地小龙虾智能体第一版。

## 当前目标

1. 保持项目可本地运行。
2. 不要把真实 API Key 写入仓库。
3. 优先补充业务知识库、客户数据读取、图片生成接口和输出记录。
4. 每次改动都要更新 VERSION.md。

## 建议开发顺序

1. 增加 knowledge/ 目录读取。
2. 增加客户 Excel/CSV 解析。
3. 增加更多任务模板。
4. 增加图片平台 API 适配层。
5. 增加日志和费用统计。
6. 增加一键打包脚本。
"""


def main() -> None:
    path = ROOT / "CODEX_HANDOFF.md"
    path.write_text(CODEX_GUIDE, encoding="utf-8")
    print(f"已生成：{path}")


if __name__ == "__main__":
    main()
