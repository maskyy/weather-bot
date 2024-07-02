import asyncio

from aiohttp import ClientSession
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from .api import get_current_weather
from .config import CONFIG
from .const import LOCATION_SEPARATOR, MAX_LOCATIONS_PER_MESSAGE
from .database import add_record
from .logger import log


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"])


async def _reply_to(msg: Message, text: str) -> Message:
    from_id = None if msg.from_user is None else msg.from_user.id
    chat_id = None if msg.sender_chat is None else msg.sender_chat.id

    insert_id = add_record(
        msg.message_id,
        from_id,
        chat_id,
        msg.date,
        msg.text,
        text,
    )

    reply = await bot.reply_to(msg, text)
    return reply


@bot.message_handler(commands=["start", "help"])
async def help(msg: Message):
    text = "Hello World"
    await _reply_to(msg, text)


def parse_weather_response(location: str, data: dict) -> str:
    if "error" in data:
        return f"Ошибка: {data["error"]}"
    template = "Город: {name}\nТемпература: {temp} °C\nСкорость ветра: {wind} м/с\n"

    return template.format(**data)


async def get_weather_task(location: str, session: ClientSession) -> str:
    data = await get_current_weather(location, session)
    return parse_weather_response(location, data)


@bot.message_handler(func=lambda _: True)
async def print_weather(msg: Message):
    locations = msg.text.split(LOCATION_SEPARATOR, maxsplit=MAX_LOCATIONS_PER_MESSAGE)

    if len(locations) > MAX_LOCATIONS_PER_MESSAGE:
        await _reply_to(
            msg,
            f"Пожалуйста, укажите не более {MAX_LOCATIONS_PER_MESSAGE} городов",
        )
        return

    locations = [l.strip() for l in locations]
    locations = list(filter(len, locations))

    async with ClientSession() as s:
        tasks = [asyncio.create_task(get_weather_task(l, s)) for l in locations]
        output = await asyncio.gather(*tasks)

    await _reply_to(msg, "\n".join(output))


@bot.message_handler()
async def run_bot():
    try:
        await bot.polling(non_stop=True, allowed_updates=["message"])
    # Log fatal exceptions (invalid token, no network on start)
    except Exception as e:
        log.fatal("Cannot run bot: %s", e)
    await bot.close_session()
