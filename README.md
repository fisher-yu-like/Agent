## 天气agent
Weather-Agent: 基于开源大模型与和风天气的 ReAct 智能体
本项目利用 Ollama 本地部署的 Qwen2.5-7B 模型，结合 LangChain 框架，构建了一个具备多工具调用能力的“天气智能体”。它能够通过自然语言交互，自动拆解任务，调用和风天气 API 获取实时天气、空气质量、分钟级降水及生活建议。

🚀 核心特性
本地大模型驱动：基于 Ollama 部署 Qwen2.5-7B，保证数据私密性与快速响应。

ReAct 逻辑架构：通过 Thought -> Action -> Observation 的循环推理模式，实现复杂问题的自动化解决。

多维度 API 集成：集成了和风天气的 6 大功能接口（城市搜索、实时天气、空气质量、分钟降水、气象预警、生活指数）。

鲁棒的输入清洗：针对模型输出可能携带的 JSON 冗余或格式错误，设计了正则表达式和字符串清洗逻辑。

代理与请求管理：支持网络代理配置，并具备简单的接口调用防刷逻辑。

🛠️ 技术栈
LLM: Ollama (Qwen2.5:7b)

Framework: LangChain, Pydantic

API: 和风天气 (QWeather) RESTful API

Library: Requests, Re, Python

📦 快速开始
启动 Ollama 服务: ollama run qwen2.5:7b

配置 API Key: 在 QWeather 类中修改 X-QW-Api-Key。

运行项目: 直接执行 Python 脚本，智能体会根据 query 自动执行多步查询。
