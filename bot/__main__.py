import asyncio
import logging

from telebot.async_telebot import AsyncTeleBot

from .config import CONFIG


logger = logging.getLogger(__name__)


bot = AsyncTeleBot(CONFIG["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
async def start(msg):
    text = "hi **bruh**"
    await bot.reply_to(msg, text)


async def main():
    logger.setLevel(getattr(logging, CONFIG["LOG_LEVEL"]))
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug("Running...")
    await bot.polling()


if __name__ == "__main__":
    asyncio.run(main())
