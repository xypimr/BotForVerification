import asyncio
import random

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS, RAFFLE_WORD, RAFFLE_MINUTES

participants = []

# Машина состояний
class Raffle(StatesGroup):
    Gets = State()
    Push = State()

# Клавиатура

def raffle_ikb():
    ikb = InlineKeyboardBuilder()
    ikb.button(text=str(len(participants)), callback_data='add')
    return ikb.as_markup()
# Функции просто

async def raffleCalc(chatId: int, bot: Bot, state: FSMContext):
    await asyncio.sleep(RAFFLE_MINUTES*60)
    await state.clear()
    if participants:
        winner = random.choice(participants)
        participants.clear()
        await bot.send_photo(
                chat_id=chatId,
                photo='https://media.istockphoto.com/id/1199025903/vector/congratulations-greeting-card-vector-lettering.jpg?s=612x612&w=0&k=20&c=JBjYOnkRerY0uxBrYAtKccIk6tdiBCuzwClegCucpmw=',
                caption=f'Поздравления победителю: @{winner.username}! \nА всем остальным удачи в следущий раз!'
        )
    else:
        await bot.send_message(
                chat_id=chatId,
                text=f'Никто не поучавствовал((')

# Функции для хендлеров
async def start_raffle(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(f'Розыгрышь начался!!! \nДля участия пишите в чат \'{RAFFLE_WORD}\' \n\n Итоги через {RAFFLE_MINUTES} !')
    await state.set_state(Raffle.Gets)
    await raffleCalc(message.chat.id, bot, state)
    await message.delete()

async def new_participant(message: types.Message, state: FSMContext):
    participants.append(message.from_user)


async def start_button_raffle(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer(f'Нажми на кнопку чтобы учавствовать', reply_markup=raffle_ikb())
    await state.set_state(Raffle.Push)
    await message.delete()
    await raffleCalc(message.chat.id, bot, state)


async def new_push(callback: types.CallbackQuery):
    participants.append(callback.from_user)
    await callback.message.edit_reply_markup(reply_markup=raffle_ikb())
    await callback.answer('Зарегистрировали тебя')

# Регистрация хендлеров в роутер
router = Router()
# Фильтрация на вызов всего этого говна только в группе
router.message.filter(lambda m: m.chat.type in ("group", "supergroup"))

router.message.register(start_raffle,
        State(),
        Command('give_away_m'),
        F.from_user.id.in_(ADMIN_IDS),
        )
router.message.register(new_participant,
        Raffle.Gets,
        F.text == RAFFLE_WORD,
        ~F.from_user.id.in_(ADMIN_IDS),
        ~F.from_user.in_(participants)
        )
router.message.register(start_button_raffle,
        State(),
        Command('give_away_c'),
        F.from_user.id.in_(ADMIN_IDS),
        )
router.callback_query.register(new_push,
        Raffle.Push,
        F.data == 'add',
        ~F.from_user.id.in_(ADMIN_IDS),
        ~F.from_user.in_(participants)
        )