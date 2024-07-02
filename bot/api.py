from json import dumps
from typing import Any
from urllib.parse import urlencode

from aiohttp import ClientSession
from limiter import Limiter

from .config import CONFIG
from .const import FETCH_CAPACITY, FETCH_RATE, MAX_RETRIES, REQUEST_TIMEOUT
from .logger import log


BASE_URL = "https://api.openweathermap.org"

_limiter = Limiter(rate=FETCH_RATE, capacity=FETCH_CAPACITY)


def _dumps(obj) -> str:
    return dumps(obj, ensure_ascii=False)


def build_request(path: str, **kwargs) -> str:
    kwargs["appid"] = CONFIG["WEATHER_API_TOKEN"]
    return f"{BASE_URL}/{path}?{urlencode(kwargs)}"


@_limiter
async def fetch(
    path: str,
    session: ClientSession,
    retries: int = MAX_RETRIES,
    **kwargs,
) -> (int, Any):
    url = build_request(path, **kwargs)
    log.debug("GET %s", url)

    exc = ""
    for i in range(retries):
        log.debug("Attempt %s", i + 1)
        try:
            async with session.get(url, timeout=REQUEST_TIMEOUT) as response:
                status = response.status
                data = await response.json()
                return status, data
        except Exception as e:
            log.info("Exception happened: %s %s", type(e), e)
            exc = str(e)
    return 0, {"message": f"сервис погоды недоступен: {exc}"}


async def get_coordinates(location: str, session: ClientSession) -> dict:
    """Returns the location's name, latitude and longtitude"""

    status, data = await fetch(
        "geo/1.0/direct",
        session,
        q=location,
        limit=1,
    )
    if status != 200:
        log.info("get_coordinates(%s) error: %s", location, _dumps(data))
        return {"error": f"место {location}: {data['message']}"}

    if len(data) == 0:
        return {"error": f"место {location} не найдено"}

    r = data[0]
    ru_name = ""
    if "local_names" in r and "ru" in r["local_names"]:
        ru_name = f" ({r['local_names']['ru']})"
    return {
        "name": f"{r['name']}, {r['country']}{ru_name}",
        "lat": r["lat"],
        "lon": r["lon"],
    }


async def get_current_weather(location: str, session: ClientSession) -> dict:
    """Returns the location's name, current temperature and wind speed"""

    city = await get_coordinates(location, session)
    if "error" in city:
        return {"error": city["error"]}

    name = city.pop("name")
    status, data = await fetch(
        "data/2.5/weather",
        session,
        **city,
        units="metric",
    )
    if status != 200:
        log.info("get_current_weather error: %s", _dumps(data))
        return {"error": f"получение погоды: {data['message']}"}

    temp = "?"
    if data.get("main", {}).get("temp", None) is not None:
        temp = data["main"]["temp"]

    wind = "?"
    if data.get("wind", {}).get("speed", None) is not None:
        wind = data["wind"]["speed"]

    return {
        "name": name,
        "temp": temp,
        "wind": wind,
    }
