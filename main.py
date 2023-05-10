import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import exceptions as tg_ex
import random

from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InputFile, FSInputFile

import joining

CHAT_ID = '-1001727181740'
ADMIN_IDS = [753529002, 6161307295]

# Токен вашего бота
TOKEN = ''

# Создаем экземпляр класса Bot
bot = Bot(token=TOKEN)

# Создаем экземпляр класса Dispatcher
dp = Dispatcher(storage=MemoryStorage())

# Функция, которая будет вызываться при команде /mlg
# async def send_gif(message: types.Message):
#     try:
#         # Получаем случайную гифку из папки gifs
#         # gif_file =
#         gif = FSInputFile(f"gifs/{random.choice(os.listdir('gifs/'))}")
#         # Отправляем гифку пользователю
#         await bot.send_animation(message.chat.id, gif)
#         # Удаление сообщения с командой
#         await message.delete()
#
#     except tg_ex.TelegramRetryAfter as e:
#         # Ошибка FloodWait, ожидаем указанное количество секунд и пытаемся снова
#         print(e)
#         # Ждем пока ошибка пройдет
#         await asyncio.sleep(e.retry_after.imag)
#         # Пытаемся еще раз отправить
#         # await send_gif(message)
#
#     except tg_ex.TelegramAPIError as e:
#         # Другие ошибки API Telegram обрабатываем по своему усмотрению
#         await message.reply(f'Произошла ошибка при отправке гифки: {e}')


# async def start_mlg(message: types.Message):

async def main():
    print(1)
    # Регистрируем обработчик команды /mlg
    # dp.message.register(send_gif, Command('mlg'))
    dp.include_routers(joining.router)
    # Пропуск апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск полинга
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

# Запускаем бота
if __name__ == '__main__':
    asyncio.run(main())
