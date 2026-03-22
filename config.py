"""配置管理"""

import os
import json
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


@dataclass
class Configuration:
    """应用配置"""
    model: str = "gpt-5.4"
    api_key: str = ""
    base_url: str = ""

    def __post_init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.vectorengine.ai/v1")

    @staticmethod
    def load_servers(config_path: str = "servers_config.json") -> dict:
        """加载 MCP 服务器配置"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(base_dir, config_path)
        with open(config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        servers = data.get("mcpServers", data)
        # 将相对 cwd 解析为绝对路径
        for name, cfg in servers.items():
            if cfg.get("transport") == "stdio" and cfg.get("cwd") == ".":
                cfg["cwd"] = base_dir
        return servers

    @staticmethod
    def load_prompt(prompt_path: str = "agent_prompts.txt") -> str:
        """加载 Agent 提示词"""
        prompt_file = os.path.join(os.path.dirname(__file__), prompt_path)
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
