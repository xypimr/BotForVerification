import asyncio
import random

from aiogram import Bot, F, Router, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.fsm.state import State
from aiogram.types import ChatMemberUpdated, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

ver = []
router = Router()

# Функция которая будет кикать через 60 секунд
async def kick(memberId: int, bot: Bot, channelId: int, mesId: int):
    await asyncio.sleep(60)
    if memberId not in ver:
        await bot.ban_chat_member(channelId, memberId)
        await bot.unban_chat_member(channelId, memberId)
        await bot.delete_message(channelId, mesId)
        print(1)
    else:
        ver.remove(memberId)

# Создание клавиатуры для верификации
def ver_ikb(correct: int, memberId: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    wrong = random.randint(0, 20)
    if wrong == correct:
        wrong += 5
    if wrong > correct:
        ikb.button(text=f"{correct}", callback_data=memberId)
        ikb.button(text=f'{wrong}', callback_data='No')
    else:
        ikb.button(text=f'{wrong}', callback_data='No')
        ikb.button(text=f"{correct}", callback_data=memberId)
    ikb.adjust(2)
    return ikb.as_markup()

# Функции хендлеров
async def new_member(event: ChatMemberUpdated, bot: Bot):
    f = random.randint(0, 10)
    s = random.randint(0, 10)
    m = await bot.send_photo(chat_id=event.chat.id,
            photo='AgACAgIAAxkBAAIFs2Rb3VuqiM1dxgJZMRbT-WUsufIZAAJnyDEb-YHgSrqxFIr23iTYAQADAgADcwADLwQ',
            caption=f"Добро пожаловать <b>@{event.new_chat_member.user.username}</b>!\nПройди верификацию: \n{f} + {s} = ",
            reply_markup=ver_ikb(f + s, event.new_chat_member.user.id),
            parse_mode='HTML'
        )
    await kick(event.new_chat_member.user.id, bot, event.chat.id, m.message_id)


# @router.callback_query(lambda callback: callback.data == str(callback.from_user.id))
async def not_kick(callback: types.CallbackQuery):
    ver.append(callback.from_user.id)
    await callback.answer('Вы успешно верифицировались!', show_alert=True)
    await callback.message.delete()

async def wrong_ans(callback: types.CallbackQuery):
    await callback.answer('Попробуй еще раз...')

async def wrong_user(callback: types.CallbackQuery):
    await callback.answer('Ты уже здесь свой, успокойся!')

# Регистрация хендлеров в роутер

router = Router()

router.chat_member.register(new_member, ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
router.callback_query.register(not_kick, lambda callback: callback.data == str(callback.from_user.id))
router.callback_query.register(wrong_ans, F.data == 'No')
router.callback_query.register(wrong_user, State())