import asyncio
import logging
import os
from dotenv import load_dotenv
from src.bot.main import create_bot, create_dispatcher, run_bot
from src.db.session import init_db

async def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    await init_db()

    bot = create_bot()
    dp = create_dispatcher()

    await run_bot(bot, dp)

if __name__ == "__main__":
    asyncio.run(main())
