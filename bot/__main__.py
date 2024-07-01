import asyncio

from .bot import run_bot
from .database import create_tables
from .logger import logger, setup_logger


async def main():
    setup_logger()
    create_tables()

    logger.debug("Running...")
    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())
