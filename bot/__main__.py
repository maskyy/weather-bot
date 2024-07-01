import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from .config import CONFIG
from .database import create_tables
from .logger import logger, setup_logger


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
async def start(msg: Message):
    text = "hi **bruh**"
    await bot.reply_to(msg, text)


async def main():
    setup_logger()
    create_tables()

    logger.debug("Running...")
    await bot.polling()


if __name__ == "__main__":
    asyncio.run(main())
