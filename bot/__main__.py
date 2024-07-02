import asyncio

from .bot import run_bot
from .database import create_tables
from .logger import log, setup_logger


async def main():
    setup_logger()
    create_tables()

    log.debug("Starting...")
    await run_bot()


if __name__ == "__main__":
    asyncio.run(main())
