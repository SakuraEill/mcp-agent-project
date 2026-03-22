"""天气查询 MCP 服务器"""

import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("WeatherServer")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_openweather_key")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(city: str) -> dict:
    """调用 OpenWeather API 获取天气数据"""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "zh_cn",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


def format_weather(data: dict) -> str:
    """格式化天气数据"""
    city = data.get("name", "未知")
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    return (
        f"🏙️ 城市: {city}\n"
        f"🌡️ 温度: {temp}°C（体感 {feels_like}°C）\n"
        f"🌤️ 天气: {description}\n"
        f"💧 湿度: {humidity}%\n"
        f"🌬️ 风速: {wind_speed} m/s"
    )


@mcp.tool()
async def query_weather(city: str) -> str:
    """
    输入指定城市的英文名称，返回今日天气查询结果。
    :param city: 城市名称（需使用英文，如 Beijing, Shanghai, Tokyo）
    :return: 格式化后的天气信息
    """
    try:
        data = await fetch_weather(city)
        return format_weather(data)
    except httpx.HTTPStatusError as e:
        return f"❌ 查询失败: HTTP {e.response.status_code}"
    except Exception as e:
        return f"❌ 查询失败: {e}"


@mcp.tool()
async def get_weather_tips(season: str) -> str:
    """
    获取指定季节的天气贴士。
    :param season: 季节名称 (spring, summer, autumn, winter)
    :return: 季节性天气建议
    """
    tips = {
        "spring": "🌸 春季多风，注意防风保暖，早晚温差大，建议带一件外套。",
        "summer": "🌞 夏季炎热，注意防暑降温，多喝水，外出注意防晒。",
        "autumn": "🍂 秋季干燥，注意补水保湿，早晚渐凉，适时添衣。",
        "winter": "❄️ 冬季寒冷，注意防寒保暖，出行注意路面结冰。",
    }
    return tips.get(season.lower(), "❓ 未知季节，请输入: spring, summer, autumn, winter")


if __name__ == "__main__":
    mcp.run(transport="stdio")
