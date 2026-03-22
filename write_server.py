"""文件写入 MCP 服务器"""

import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WriteServer")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@mcp.tool()
async def write_file(filename: str, content: str) -> str:
    """
    将内容写入到本地文件。
    :param filename: 文件名（如 weather_report.txt）
    :param content: 要写入的文本内容
    :return: 写入结果
    """
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ 已成功写入文件: {file_path}"
    except Exception as e:
        return f"❌ 写入失败: {e}"


@mcp.tool()
async def append_file(filename: str, content: str) -> str:
    """
    向已有文件追加内容。
    :param filename: 文件名
    :param content: 要追加的文本内容
    :return: 追加结果
    """
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n{content}")
        return f"✅ 已追加内容到文件: {file_path}"
    except Exception as e:
        return f"❌ 追加失败: {e}"


@mcp.tool()
async def read_file(filename: str) -> str:
    """
    读取本地文件内容。
    :param filename: 文件名
    :return: 文件内容
    """
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(file_path):
            return f"❌ 文件不存在: {file_path}"
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ 读取失败: {e}"


@mcp.tool()
async def list_files() -> str:
    """
    列出 output 目录下的所有文件。
    :return: 文件列表
    """
    try:
        files = os.listdir(OUTPUT_DIR)
        if not files:
            return "📂 output 目录为空"
        file_list = "\n".join(f"  📄 {f}" for f in files)
        return f"📂 output 目录文件列表:\n{file_list}"
    except Exception as e:
        return f"❌ 列出文件失败: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
