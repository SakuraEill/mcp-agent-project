"""CLI 交互式客户端"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from config import Configuration

load_dotenv()


async def run_chat_loop() -> None:
    """启动 MCP-Agent 聊天循环"""
    cfg = Configuration()
    servers_cfg = cfg.load_servers()
    prompt = cfg.load_prompt()

    print("=" * 50)
    print("🤖 Agent 出行助手 - CLI 模式")
    print("=" * 50)
    print("输入 'quit' 退出\n")

    # 连接 MCP 服务器
    client = MultiServerMCPClient(servers_cfg)
    tools = await client.get_tools()
    print(f"🔧 已加载 {len(tools)} 个工具")

    # 初始化大模型
    model = ChatOpenAI(
        model=cfg.model,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
    )

    # 构造 Agent（带记忆）
    checkpointer = InMemorySaver()
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt,
        checkpointer=checkpointer,
    )

    # 聊天循环
    while True:
        try:
            user_input = input("\n你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("👋 再见！")
            break

        try:
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"configurable": {"thread_id": "cli-session-1"}},
            )
            ai_message = result["messages"][-1].content
            print(f"\nAI: {ai_message}")
        except Exception as e:
            print(f"\n❌ 出错了: {e}")


if __name__ == "__main__":
    asyncio.run(run_chat_loop())
