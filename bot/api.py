from urllib.parse import urlencode

import aiohttp

from .config import CONFIG
from .logger import logger


BASE_URL = "https://api.openweathermap.org"


def build_request(path: str, **kwargs) -> str:
    kwargs["appid"] = CONFIG["WEATHER_API_TOKEN"]
    return f"{BASE_URL}/{path}?{urlencode(kwargs)}"


async def fetch(path: str, session: aiohttp.ClientSession, **kwargs):
    async with session.get(build_request(path, **kwargs)) as response:
        status = response.status
        data = await response.json()
        return status, data


async def get_coordinates(location: str, session: aiohttp.ClientSession) -> dict:
    """Returns the location's name, latitude and longtitude"""

    status, data = await fetch(
        "geo/1.0/direct",
        session,
        q=location,
        limit=1,
    )
    if status != 200:
        logger.info("get_coordinates error: %s", data)
        return f"Ошибка: {data}"

    if len(data) == 0:
        return f"Место {location} не найдено!"

    entry = data[0]
    return {
        "name": f"{entry["name"]}, {entry["country"]}",
        "lat": entry["lat"],
        "lon": entry["lon"],
    }


async def get_weather(location: str, session: aiohttp.ClientSession) -> str:
    """Returns the location's name, its current temperature and wind"""

    city = await get_coordinates(location, session)
    name = city.pop("name")
    status, data = await fetch(
        "data/2.5/weather",
        session,
        **city,
        units="metric",
    )

    return {
        "name": name,
        "temp": data["main"]["temp"],
        "wind": data["wind"]["speed"],
    }
