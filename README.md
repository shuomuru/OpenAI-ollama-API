# Ollama 本地 LLM 聊天机器人

这是一个基于 **Ollama 本地大语言模型（LLM）** + **FastAPI** + **Gradio** 的聊天机器人示例项目。

特点：

- 本地调用 Ollama 模型，无需真实 API Key  
- FastAPI 提供 REST/Streaming 接口  
- Gradio 前端聊天界面  
- 支持流式输出，可边生成边显示  
- 聊天历史管理，可保留指定轮数或清空  
- 可调参数：`temperature`、`top_p`、`max_tokens` 等  

---
```bash
## 项目结构


.
├── backend.py # FastAPI 后端服务
├── frontend.py # Gradio 前端界面
├── README.md
└── requirements.txt # 项目依赖
```

---

## 安装依赖

建议使用虚拟环境：

```bash
conda create -n rag python=3.10 -y
conda activate rag

安装依赖：

pip install fastapi uvicorn openai gradio requests
FastAPI 后端使用

backend.py 提供 /chat 接口：

POST JSON 参数示例：
{
  "query": "你好，帮我写一首诗",
  "sys_prompt": "你是一个有用的助手。",
  "history": [
    {"role": "user", "content": "之前的用户消息"},
    {"role": "assistant", "content": "之前的助手回复"}
  ],
  "history_len": 1,
  "temperature": 0.5,
  "top_p": 0.5,
  "max_tokens": 1024
}
注意：
历史消息必须是 {role, content} 字典
支持流式输出（StreamingResponse）

启动服务：

python backend.py

默认监听：

http://127.0.0.1:6066
Gradio 前端使用

frontend.py 提供 Web 界面与 FastAPI 后端交互：

左侧面板：
系统提示词
历史轮数
temperature / top_p / max_tokens
流式输出开关
清空历史按钮
右侧面板：
聊天界面 + 输入框 + 发送按钮
历史消息自动转换为 API 可用格式
支持流式显示生成内容

启动前端：

python frontend.py

如果本地无法访问 localhost，可以使用：

demo.launch(share=True)

Gradio 会生成公网可访问的链接。

注意事项
Ollama 本地模型不需要真实 API Key，但 OpenAI SDK 初始化必须传入一个占位 key：
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key="unused", base_url="http://localhost:11434/v1")
消息历史必须严格符合 {role, content} 格式，否则会报错：
数据与消息格式不兼容
stream 参数必须通过 Gradio Checkbox 传入，不能直接传布尔值，否则会报：
TypeError: argument of type 'bool' is not iterable
如果 Gradio 前端报：
ValueError: When localhost is not accessible...

请在 demo.launch(share=True) 或检查本地网络/防火墙设置。

示例界面
左侧：参数控制
右侧：聊天窗口
总结
FastAPI + AsyncOpenAI 调用本地 Ollama 模型
Gradio 构建可交互聊天界面
支持流式输出、历史管理、参数调节
轻量易用，适合本地部署和快速测试 LLM
