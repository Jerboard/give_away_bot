from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state


import db
from init import dp, bot
from keyboards import inline_kb as kb
from utils.access import check_access
from utils.message_utils import send_any_message, restore_entities


# старт
# @dp.message(CommandStart())
@dp.message(Command('start', 'new_give', 'give_away'))
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    # await test(msg.chat.id)
    await state.clear()
    channels = await db.get_all_channels ()
    access = await check_access(msg.from_user.id, channels)
    if not access:
        await msg.answer(f'У вас нет доступа. Бот доступен только администраторам зарегистрированных каналов')
    else:
        if msg.text == '/give_away':
            give = await db.get_all_give()
            await msg.answer ('Выберите конкурс', reply_markup=kb.get_all_give_kb (give))
        else:
            await msg.answer('Выберите канал', reply_markup=kb.get_channel_kb(channels))


# отмена действия
@dp.callback_query(lambda cb: cb.data.startswith('cancel'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
    await cb.answer('❌ Отмена')
