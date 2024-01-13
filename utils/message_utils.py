import typing as t
import json
import random

from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, Message, MessageEntity
from aiogram.enums.content_type import ContentType

import db
from init import bot, DATETIME_FORMAT
from keyboards import inline_kb as kb


content_type_map = {
    'text': 'сообщение',
    'photo': 'фото',
    'video': 'видео',
    'video_note': 'видео заметку',
    'animation': 'gif',
    'voice': 'войс',
    'document': 'файл',
    'sticker': 'стикер'
}


# отправляет сообщение всех типов
async def send_any_message(
        chat_id: int,
        text: str,
        entities: list,
        media_id: str,
        content_type: str,
        keyboard: InlineKeyboardMarkup = None
) -> t.Union[Message, None]:
    if content_type == 'text':
        sent = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'photo':
        sent = await bot.send_photo (
            chat_id=chat_id,
            photo=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'video':
        sent = await bot.send_video (
            chat_id=chat_id,
            video=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'video_note':
        sent = await bot.send_video_note (
            chat_id=chat_id,
            video_note=media_id,
            reply_markup=keyboard
        )

    elif content_type == 'animation':
        sent = await bot.send_animation (
            chat_id=chat_id,
            animation=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'voice':
        sent = await bot.send_voice (
            chat_id=chat_id,
            voice=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'document':
        sent = await bot.send_document (
            chat_id=chat_id,
            voice=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    elif content_type == 'sticker':
        sent = await bot.send_voice (
            chat_id=chat_id,
            voice=media_id,
            caption=text,
            caption_entities=entities,
            reply_markup=keyboard
        )

    else:
        sent = None

    return sent


# извлекает id медиа из сообщения
async def get_media_id(msg: Message) -> str:
    if msg.content_type == 'photo':
        media_id = msg.photo[-1].file_id

    elif msg.content_type == 'video':
        media_id = msg.video.file_id

    elif msg.content_type == 'video_note':
        media_id = msg.video_note.file_id

    elif msg.content_type == 'animation':
        media_id = msg.animation.file_id

    elif msg.content_type == 'voice':
        media_id = msg.voice.file_id

    elif msg.content_type == 'document':
        media_id = msg.document.file_id

    elif msg.content_type == 'sticker':
        media_id = msg.sticker.file_id

    else:
        media_id = ''

    return media_id


# создаёт текст для розыгрыша
def get_bottom_text(
        give_info: dict,
        prize_count: int = None,
        tour_count: int = None,
):
    text = (f'\n\n➿➿➿➿➿➿➿➿➿➿➿➿➿➿➿➿➿\n\n'
            f'Всего сообщений: {give_info ["message_count"]}\n'
            f'Уникальных пользователей: {give_info ["unique_user_count"]}')

    if prize_count:
        text = (f'{text}\n'
                f'Призов: {prize_count}')

    if tour_count:
        text = (f'{text}\n'
                f'Туров: {tour_count}')

    return text


# преобразует в строку
def proces_entities(entities: list[MessageEntity]):
    entities_list = []
    if entities:
        for entity in entities:
            entities_list.append ({
                'type': entity.type,
                'url': entity.url,
                'user': entity.user,
                'language': entity.length,
                'offset': entity.offset,
                'length': entity.length,
                'custom_emoji_id': entity.custom_emoji_id})

    return json.dumps (entities_list)


# восстанавливает entities
def restore_entities(entities_string):
    entities = []
    if entities_string:
        entities_raw = json.loads (entities_string)
        for entity_raw in entities_raw:
            entities.append (MessageEntity (
                type=entity_raw ['type'],
                offset=entity_raw ['offset'],
                length=entity_raw ['length'],
                custom_emoji_id=entity_raw ['custom_emoji_id'],
                url=entity_raw ['url'],
                user=entity_raw ['user'],
                language=entity_raw ['user'],
            ))
    return entities


# текст победителя
def get_winner_text(winner_info: db.MessageRow):
    if winner_info.created_at:
        send_time = winner_info.created_at.strftime(DATETIME_FORMAT)
    else:
        send_time = datetime.now().strftime(DATETIME_FORMAT)
    message_format = content_type_map[winner_info.content_type]
    return (f'🎉🎉🎉 {winner_info.full_name}\n'
            f'{send_time} отправила {message_format}\n'
            f'{winner_info.text}')
