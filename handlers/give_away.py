from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

import random


import db
from init import dp, bot
from keyboards import inline_kb as kb
from utils.access import check_is_channel_admin
from utils.message_utils import send_any_message, restore_entities, get_bottom_text


# старт розыгрыша
@dp.callback_query(lambda cb: cb.data.startswith('give_away_change'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    _, channel_id_str, give_id_str = cb.data.split(':')
    channel_id = int(channel_id_str)
    give_id = int(give_id_str)

    result = await bot.get_chat_member (
        chat_id=channel_id,
        user_id=cb.from_user.id
    )
    if result.status == ChatMemberStatus.ADMINISTRATOR or result.status == ChatMemberStatus.CREATOR:
        give = await db.get_give(give_id=give_id)

        give_info = await db.get_give_info (give_id)
        bottom_text = get_bottom_text (give_info)

        text = f'{give.text}{bottom_text}'
        keyboard = kb.get_give_kb (give_id)
        await cb.message.delete()
        await send_any_message (
            chat_id=cb.message.chat.id,
            text=text,
            entities=restore_entities(give.entities),
            media_id=give.media_id,
            content_type=give.content_type,
            keyboard=keyboard
        )

    else:
        await cb.answer ('❌ Вы не являетесь админом в канале.\n\n'
                         'Выберите розыгрыш канала в котором вы являетесь админом.')


# старт розыгрыша
@dp.callback_query(lambda cb: cb.data.startswith('give_away_start'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    _, type_, give_id_str = cb.data.split(':')
    give_id = int(give_id_str)

    if type_ == 'finish':
        await db.update_active_give(give_id, False)

    else:
        await state.set_state('give_away')
        await state.update_data(data={
            'give_id': give_id,
            'message_id': cb.message.message_id,
            'type_': type_,
            'step': 'prize',
            'count_prize': 0
        })

        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer('Сколько будет призов?', reply_markup=kb.get_numeric_kb())


# старт розыгрыша
@dp.callback_query(lambda cb: cb.data.startswith('give_away_numeric'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    _, numeric_str = cb.data.split(':')
    numeric = int (numeric_str)

    await state.update_data(data={
        'step': 'tour',
        'count_prize': numeric
    })

    data = await state.get_data ()
    give = await db.get_give (give_id=data['give_id'])

    give_info = await db.get_give_info (data['give_id'])
    bottom_text = get_bottom_text (
        give_info=give_info,
        prize_count=data['count_prize'],
    )

    text = f'{give.text}{bottom_text}'
    keyboard = kb.get_give_start_tour_kb ()
    await cb.message.delete ()
    await bot.delete_message(chat_id=cb.message.chat.id, message_id=data['message_id'])
    await send_any_message (
        chat_id=cb.message.chat.id,
        text=text,
        entities=restore_entities (give.entities),
        media_id=give.media_id,
        content_type=give.content_type,
        keyboard=keyboard
    )


# сам розыгрыш
@dp.callback_query(lambda cb: cb.data.startswith('give_away_tour'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    on_user = True if data['type_'] == 'users' else False
    users = await db.get_all_give_user_info(data['give_id'], on_users=on_user)

    sent = None

    lost_winners = data['count_prize']
    all_numbers = list (range (0, 20))
    random.shuffle (all_numbers)
    win_list = all_numbers [:lost_winners - 1]
    win_list.append (19)
    for tour in range (0, 20):
        champions_text = ''

        for i in range(0, lost_winners):
            user = random.choice (users)
            row = f'{user.full_name}\n'
            champions_text = f'{champions_text}{row}'

        text = f'Выбор победителей:\n\n{champions_text}'

        if not sent:
            sent = await cb.message.answer(text)
        else:
            await sent.edit_text(text)

        if tour in win_list:
            winner = random.choice (users)
            while winner.username is None:
                winner = random.choice (users)

            users.remove (winner)
            username = str(winner.username).replace('"', '')
            await cb.message.answer(
                text=f'🎉🎉🎉 {winner.full_name}',
                reply_markup=kb.get_send_winner_kb(username))

            lost_winners = lost_winners - 1

    await sent.delete()
    await cb.message.edit_reply_markup(reply_markup=kb.get_give_restart_tour_kb(data['give_id']))


# закрывает розыгрыша
@dp.callback_query(lambda cb: cb.data.startswith('give_away_finish'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    _, give_id_str = cb.data.split(':')
    give_id = int(give_id_str)

    await db.update_active_give(give_id, False)
    # await db.delete_give(give_id)
    # await db.delete_give_messages(give_id)

    await cb.message.delete()
    await cb.message.answer('Розыгрыш закончен')
