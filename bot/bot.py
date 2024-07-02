import asyncio

from aiohttp import ClientSession
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from .api import get_current_weather
from .config import CONFIG
from .const import MAX_LOCATIONS_PER_MESSAGE


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"])


@bot.message_handler(commands=["start", "help"])
async def help(msg: Message):
    text = "Hello World"
    await bot.reply_to(msg, text)


def parse_weather_response(location: str, data: dict) -> str:
    if "error" in data:
        return f"Ошибка: {data["error"]}"
    template = "Город: {name}\nТемпература: {temp} °C\nСкорость ветра: {wind} м/с" ""

    return template.format(**data)


async def get_weather_task(location: str, session: ClientSession) -> str:
    data = await get_current_weather(location, session)
    return parse_weather_response(location, data)


@bot.message_handler(func=lambda _: True)
async def print_weather(msg: Message):
    locations = msg.text.split(",", maxsplit=MAX_LOCATIONS_PER_MESSAGE)

    if len(locations) > MAX_LOCATIONS_PER_MESSAGE:
        await bot.reply_to(
            msg,
            f"Пожалуйста, укажите не более {MAX_LOCATIONS_PER_MESSAGE} городов",
        )
        return

    locations = [l.strip() for l in locations]
    locations = list(filter(len, locations))

    async with ClientSession() as s:
        tasks = [asyncio.create_task(get_weather_task(l, s)) for l in locations]
        output = await asyncio.gather(*tasks)

    await bot.reply_to(msg, "\n".join(output))


@bot.message_handler()
async def run_bot():
    await bot.polling(non_stop=True)
