import asyncio
import logging
import os
import uvicorn
from dotenv import load_dotenv
from src.bot.main import create_bot, create_dispatcher, run_bot
from src.db.session import init_db
from src.api.main import app as fastapi_app

async def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    await init_db()

    bot = create_bot()
    dp = create_dispatcher()

    config = uvicorn.Config(app=fastapi_app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    await asyncio.gather(
        run_bot(bot, dp),
        server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())
