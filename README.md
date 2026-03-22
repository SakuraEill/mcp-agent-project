# 🤖 MCP Agent 出行助手

基于 LangChain + LangGraph + MCP 协议的智能出行助手，支持天气查询、文件管理等功能。

## 功能

- **天气查询** — 查询全球城市实时天气（需 OpenWeather API Key）
- **季节建议** — 获取春夏秋冬出行贴士
- **文件管理** — 写入、追加、读取、列出本地文件
- **多模式运行** — CLI 交互 / 单次查询 / FastAPI HTTP 服务 + Web 前端

## 技术栈

- LangChain + LangGraph（Agent 框架）
- langchain-mcp-adapters（MCP 协议适配）
- FastMCP（MCP Server 实现）
- FastAPI + Uvicorn（HTTP 服务）
- OpenAI 兼容 API（gpt-5.4）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.vectorengine.ai/v1
OPENWEATHER_API_KEY=your_openweather_key  # 可选，天气查询需要
```

### 3. 运行

**Web 模式（推荐）：**
```bash
python3 api_server.py
# 浏览器打开 http://localhost:8000
```

**CLI 交互模式：**
```bash
python3 client.py
```

**单次查询：**
```bash
python3 client_simple.py
```

## 项目结构

```
mcp-agent-project/
├── api_server.py        # FastAPI 服务器
├── client.py            # CLI 交互客户端
├── client_simple.py     # 单次查询示例
├── config.py            # 配置管理
├── weather_server.py    # 天气 MCP Server
├── write_server.py      # 文件管理 MCP Server
├── servers_config.json  # MCP 服务器配置
├── agent_prompts.txt    # Agent 系统提示词
├── index.html           # Web 前端
├── requirements.txt     # Python 依赖
└── .env                 # 环境变量
```

## MCP 工具列表

| 工具 | 来源 | 说明 |
|------|------|------|
| query_weather | WeatherServer | 查询城市实时天气 |
| get_weather_tips | WeatherServer | 获取季节出行建议 |
| write_file | WriteServer | 写入文件 |
| append_file | WriteServer | 追加文件内容 |
| read_file | WriteServer | 读取文件 |
| list_files | WriteServer | 列出文件列表 |
