import logging
import os
import asyncio
from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from dotenv import load_dotenv

import giveaway
import joining

# Загрузка переменных окружения из файла
load_dotenv()

# Создаем экземпляр класса Bot
bot = Bot(token=os.getenv('TOKEN'))

# Создаем экземпляр класса Dispatcher
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

# Запускаем логи
logging.basicConfig(filename='all.log', encoding='utf-8', level=logging.DEBUG)

async def main():
    # Регистрация роутеров
    dp.include_routers(joining.router)
    dp.include_routers(giveaway.router)
    # Пропуск апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск полинга
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# Запускаем бота
if __name__ == '__main__':
    asyncio.run(main())
