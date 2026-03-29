from fastapi import FastAPI, Body
from openai import AsyncOpenAI
from typing import List
from fastapi.responses import StreamingResponse

app = FastAPI()

# -----------------------------
# 配置 Ollama/OpenAI 客户端
# 如果 Ollama 不需要 API key，可以改成 api_key=None
api_key = 'ollama'
base_url = "http://localhost:11434/v1"
aclient = AsyncOpenAI(api_key=api_key, base_url=base_url)

# -----------------------------
# 路由：聊天接口
@app.post("/chat")
async def chat(
    query: str = Body(..., description="用户输入"),
    sys_prompt: str = Body("你是一个有用的助手。", description="系统提示词"),
    history: List[dict] = Body([], description="历史对话，包含 role/content"),
    history_len: int = Body(1, description="保留历史对话轮数"),
    temperature: float = Body(0.5, description="LLM采样温度"),
    top_p: float = Body(0.5, description="LLM采样概率"),
    max_tokens: int = Body(None, description="LLM最大token数量")
):
    # 保留历史轮数
    if history_len > 0:
        history = history[-2 * history_len:]

    # 构建 messages 列表
    messages = [{"role": "system", "content": sys_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": query})

    # 发送请求到模型
    response = await aclient.chat.completions.create(
        model="my-qwen",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True
    )

    # -----------------------------
    # 流式输出
    async def generate_response():
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    return StreamingResponse(generate_response(), media_type="text/plain")

# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6066, log_level="info")