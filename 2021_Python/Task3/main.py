import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN

from handlers.game import register_handlers_game
from handlers.common import register_handlers_common


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Что делать?"),
        BotCommand(command="/start", description="Играть"),
        BotCommand(command="/cancel", description="Отменить игру")
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)
    print("Завязываю узел... Повдвешиваю...")

    register_handlers_common(dp)
    register_handlers_game(dp)
    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
