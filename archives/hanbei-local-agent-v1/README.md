# 汉北本地“小龙虾”智能体归档｜第一版

> 归档版本：v1.0.0-first-archive  
> 归档日期：2026-06-16  
> 用途：沉淀 Codex 开发阶段形成的本地智能体最小可用代码骨架，便于后续继续交给 Codex、DeepSeek 或其他模型迭代。

## 1. 项目定位

这个目录是“汉北本地小龙虾智能体”的第一版代码存档。

第一版不追求完整商业化交付，而是先把已经确定的架构固定下来：

- `app.py`：命令行一键入口。
- `config.example.yaml`：模型、图片平台、路径等配置模板。
- `setup_codex.py`：为 Codex 或其他代码智能体生成项目开发说明。
- `agent/system_prompt.md`：小龙虾角色设定、公司业务边界、输出规则。
- `agent/workflow.py`：内容、销售、客户、图片、代码、管理六类工作流。
- `agent/tools.py`：模型调用、文件保存、日志记录等基础工具。
- `webui.py`：本地网页入口示例。
- `logs/`：运行日志目录，默认不提交日志内容。
- `outputs/`：生成结果目录，默认不提交生成内容。

## 2. 第一版能力范围

当前版本将“小龙虾”拆成六类能力：

| 模块 | 作用 |
|---|---|
| 内容小龙虾 | 公众号、小红书、产品文案、短视频脚本、海报提示词 |
| 销售小龙虾 | 客户跟进话术、电话前准备、微信短句、销售复盘 |
| 客户小龙虾 | 客户资料整理、J 表/C 表线索总结、展会名单归纳 |
| 图片小龙虾 | 生成图片提示词，后续可接即梦 AI、豆包、火山等平台 |
| 代码小龙虾 | 辅助修改 Python、小程序、接口脚本、自动化工具 |
| 管理小龙虾 | 记录制度、账号、API、费用台账、内部流程提醒 |

## 3. 快速开始

复制配置模板：

```bash
cp config.example.yaml config.yaml
```

设置环境变量，避免把 Key 写死在仓库：

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="你的API Key"

# macOS / Linux
export DEEPSEEK_API_KEY="你的API Key"
```

安装依赖：

```bash
pip install -r requirements.txt
```

命令行运行：

```bash
python app.py --task sales --input "客户做电热炉，想咨询电力调整器选型，帮我写一段微信跟进话术"
```

本地网页运行：

```bash
streamlit run webui.py
```

## 4. 版本记录

### v1.0.0-first-archive

- 建立第一版归档目录。
- 固定本地智能体基础架构。
- 支持 OpenAI-Compatible / DeepSeek 类接口调用。
- 预留图片生成平台配置。
- 预留长期知识库、客户库、账号台账、输出记录目录。

## 5. 注意事项

- 不要把真实 API Key 写入 `config.yaml` 或代码文件。
- `config.yaml`、`logs/`、`outputs/` 默认应加入 `.gitignore`。
- 当前版本是“工程骨架 + 最小可运行链路”，不是最终产品。
- 后续应继续补充公司资料、派立德产品资料、销售话术库、历史公众号/小红书内容和客户分层规则。
