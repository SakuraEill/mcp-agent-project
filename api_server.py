"""FastAPI 服务器 - 提供 HTTP API"""

import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from config import Configuration

load_dotenv()

# 全局变量
mcp_client: MultiServerMCPClient = None
agent = None


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default"


class ChatResponse(BaseModel):
    content: str
    thread_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 生命周期管理"""
    global mcp_client, agent

    cfg = Configuration()
    servers_cfg = cfg.load_servers()
    prompt = cfg.load_prompt()

    # 连接 MCP 服务器（新版 API 不再使用 async with）
    mcp_client = MultiServerMCPClient(servers_cfg)
    tools = await mcp_client.get_tools()
    print(f"🔧 已加载 {len(tools)} 个工具")

    # 初始化 Agent
    model = ChatOpenAI(
        model=cfg.model,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
    )
    checkpointer = InMemorySaver()
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt,
        checkpointer=checkpointer,
    )

    print("🚀 Agent 出行助手 API 已启动")
    yield

    print("👋 服务已关闭")


app = FastAPI(title="Agent 出行助手 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
async def root():
    """返回前端页面"""
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": agent is not None}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """聊天接口"""
    if agent is None:
        return ChatResponse(content="❌ Agent 未初始化", thread_id=request.thread_id)

    try:
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            {"configurable": {"thread_id": request.thread_id}},
        )
        content = result["messages"][-1].content
        return ChatResponse(content=content, thread_id=request.thread_id)
    except Exception as e:
        return ChatResponse(
            content=f"❌ 处理失败: {e}", thread_id=request.thread_id
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
