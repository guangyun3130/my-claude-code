# my‑claude‑code
> 手动复刻简易版 Claude Code，本地实现大模型编码助手，可读取项目文件、执行工具调用、代码生成、修改文件。

## 📖 项目简介
`my‑claude‑code` 模仿 Anthropic Claude Code 的核心能力，打造一个本地命令行编码助手。
实现核心逻辑：上下文读取项目代码、工具调用（读文件/写文件/列目录）、多轮对话、代码修改输出，不依赖官方 Claude Code 二进制，纯手动实现。

> 本项目只是简易原型，对标 Claude Code 的交互范式：Agent + 工具调用 + 项目上下文编码。

## ✨ 核心特性
- 📂 读取本地项目文件、遍历目录，自动收集代码上下文
- ✍️ 文件写入、修改、片段替换工具（模拟 Claude Code 编辑块）
- 💬 多轮 Agent 对话，支持复杂编码任务
- 🔧 简单工具调用解析（XML 格式工具调用，对齐 Claude 协议）
- 🖥️ 命令行交互，直接在项目目录运行
- 🧩 可对接 OpenAI / Anthropic / 本地大模型（Ollama）后端
- 📝 输出修改预览，确认后再写入磁盘，防止误改

## 📦 环境依赖
- Python >= 3.11
- 依赖库
```bash
pip install openai python‑dotenv pydantic rich
