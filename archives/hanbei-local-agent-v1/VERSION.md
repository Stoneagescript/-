# VERSION

## v1.0.0-first-archive

- 版本名称：第一版归档
- 日期：2026-06-16
- 状态：可继续开发的本地智能体骨架
- 主要目标：把 Codex 阶段形成的“小龙虾”本地智能体思路固化成可维护的 Python 项目结构。

### 已固定内容

1. 智能体入口：`app.py`
2. 配置入口：`config.example.yaml`
3. Codex 开发说明生成器：`setup_codex.py`
4. 小龙虾系统提示词：`agent/system_prompt.md`
5. 任务工作流：`agent/workflow.py`
6. 工具函数：`agent/tools.py`
7. 本地网页入口：`webui.py`

### 下一版建议

- 增加公司知识库读取能力。
- 增加派立德产品资料库。
- 增加客户库 Excel / CSV 解析。
- 增加图片生成平台真实 API 适配。
- 增加小程序线索推送能力。
- 增加费用台账和 API 调用日志。
