from textwrap import dedent

from aiohttp import ClientSession
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from .api import get_weather
from .config import CONFIG


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"])


@bot.message_handler(commands=["start", "help"])
async def help(msg: Message):
    text = "Hello World"
    await bot.reply_to(msg, text)


@bot.message_handler(func=lambda _: True)
async def print_weather(msg: Message):
    locations = msg.text.split(",")
    template = dedent(
        """
        Город: {name}
        Температура: {temp} °C
        Скорость ветра: {wind} м/с
        """
    )

    output = []
    async with ClientSession() as s:
        for l in locations:
            data = await get_weather(l, s)
            output.append(template.format(**data))

    await bot.reply_to(msg, "\n".join(output))


@bot.message_handler()
async def run_bot():
    await bot.polling()
