from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state


import db
from init import dp, bot
# from keyboards import inline_kb as kb
from utils.message_utils import get_media_id, proces_entities


# Ловит каналы, пишет их
@dp.channel_post()
async def view_channel_posts(msg: Message):
    await db.add_update_channel(
        chat_id=msg.chat.id,
        chat_title=msg.chat.title,
    )


# Посты в чате комментариев
@dp.message(StateFilter(default_state))
async def view_comment(msg: Message):
    if msg.reply_to_message:
        give = await db.check_give_message(
            chat_id=msg.reply_to_message.forward_from_chat.id,
            message_id=msg.reply_to_message.forward_from_message_id
        )

        if give:
            text = msg.text if msg.text else msg.caption
            entities = msg.entities if msg.entities else msg.caption_entities
            media_id = await get_media_id (msg)

            await db.add_message(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                user_id=msg.from_user.id,
                full_name=msg.from_user.full_name,
                username=msg.from_user.username,
                give_id=give.id,
                text=text,
                entities=proces_entities (entities),
                media_id=media_id,
                content_type=msg.content_type
            )




    # print ('Коммент:')
    # print(msg.chat.title)
    # print(msg.chat.id)
    # if msg.reply_to_message:
    #     print(msg.reply_to_message.forward_from_chat.id)
    #     print(msg.reply_to_message.forward_from_message_id)

