import asyncio
import logging
import sys
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage as ms
from yestabak.api_wrapper import ApiWrapper
from yestabak.routes import userRouter
from yestabak.configs import BOT_TOKEN
from yestabak.helpers import render_text


# main function to run
async def main():
    from yestabak import handlers

    try:
        # Initialize Bot
        bot = Bot(BOT_TOKEN, parse_mode="HTML")

        # Initialize Dispatcher
        dp = Dispatcher(storage=ms())

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] | %(levelname)-8s | %(message)s",
        )

        render_text()

        # Drop pending updates
        await bot.delete_webhook(drop_pending_updates=True)

        # Initialize routers and attach it to main Router/Dispatcher
        dp.include_router(userRouter)

        # Initialize api wrapper
        api = ApiWrapper()

        # Start polling
        await dp.start_polling(bot, api=api)

    except Exception as e:
        logging.error(f"An error occurred while starting bot: {e}")
        sys.exit(0)


if __name__ == "__main__":
    # Run it f#cking up
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
