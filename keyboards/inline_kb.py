from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

import db
from init import DATE_FORMAT


# клавиатура с каналами
def get_cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='❌ Отмена', callback_data=f'cancel')

    kb.adjust(1)
    return kb.as_markup()


# клавиатура с каналами
def get_channel_kb(channels: tuple[db.ChannelRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for channel in channels:
        kb.button(text=channel.chat_title, callback_data=f'create_give:{channel.chat_id}')

    kb.adjust(1)
    return kb.as_markup()


# клавиатура с каналами
def get_all_give_kb(all_give: tuple[db.GiveRow]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for give in all_give:
        text = f'({give.start_date.strftime(DATE_FORMAT)}) {give.channel_name}'
        kb.button(text=text[:64], callback_data=f'give_away_change:{give.chat_id}:{give.id}')

    kb.adjust(1)
    return kb.as_markup()


# клавиатура с каналами
def get_create_post_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='✅ Отправить пост', callback_data=f'start_give:conf')
    kb.button (text='🖍 Редактировать пост', callback_data=f'start_give:edit')
    kb.button (text='❌ Удалить пост', callback_data=f'cancel')

    kb.adjust (1)
    return kb.as_markup ()


# клавиатура начала гива
def get_give_kb(give_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='💬 Начать розыгрыш по сообщениям', callback_data=f'give_away_start:messages:{give_id}')
    kb.button (text='🧍 Начать розыгрыш по пользователям', callback_data=f'give_away_start:users:{give_id}')
    kb.button (text='🗑 Закончить без розыгрыша', callback_data=f'give_away_finish:{give_id}')
    kb.button (text='❌ Закрыть', callback_data=f'cancel')

    kb.adjust (1)
    return kb.as_markup ()


# клавиатура начала гива
def get_give_start_tour_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='🎰 Начать', callback_data=f'give_away_tour')
    kb.button (text='❌ Закрыть', callback_data=f'cancel')

    kb.adjust (1)
    return kb.as_markup ()


# клавиатура повтора гива
def get_give_restart_tour_kb(give_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button (text='🎰 Повторить розыгрыш', callback_data=f'give_away_tour')
    kb.button (text='🏁 Закончить розыгрыш', callback_data=f'give_away_finish:{give_id}')

    kb.adjust (1)
    return kb.as_markup ()


# клавиатура количества
def get_numeric_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in range(1, 11):
        kb.button(text=f'{i}', callback_data=f'give_away_numeric:{i}')

    kb.button (text='❌ Отмена', callback_data=f'cancel')
    kb.adjust(5, 5, 1)
    return kb.as_markup()


# написать победителю
def get_send_winner_kb(username: str) -> InlineKeyboardMarkup:
    # username = str(username).replace('"', '')
    kb = InlineKeyboardBuilder()
    kb.button(text='Написать', url=f'https://t.me/{username}')

    kb.adjust(1)
    return kb.as_markup()