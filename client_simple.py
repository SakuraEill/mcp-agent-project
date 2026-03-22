"""单次调用示例"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from config import Configuration

load_dotenv()


async def single_query(question: str = "北京今天天气怎么样？") -> str:
    """单次查询"""
    cfg = Configuration()
    servers_cfg = cfg.load_servers()
    prompt = cfg.load_prompt()

    client = MultiServerMCPClient(servers_cfg)
    tools = await client.get_tools()

    model = ChatOpenAI(
        model=cfg.model,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=prompt,
    )

    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    answer = result["messages"][-1].content
    print(f"❓ 问题: {question}")
    print(f"💡 回答: {answer}")
    return answer


if __name__ == "__main__":
    asyncio.run(single_query())
