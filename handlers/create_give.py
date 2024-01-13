from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state


import db
from init import dp, bot, log_error
from keyboards import inline_kb as kb
from utils.access import check_is_channel_admin
from utils.message_utils import send_any_message, proces_entities, get_media_id, get_bottom_text


# старт создания гива
@dp.callback_query(lambda cb: cb.data.startswith('create_give'))
async def start_create_give(cb: CallbackQuery, state: FSMContext):
    _, channel_id_str = cb.data.split(':')
    channel_id = int(channel_id_str)

    is_admin = await check_is_channel_admin(channel_id, user_id=cb.from_user.id)

    if not is_admin.access_user:
        await cb.answer('❌ Вы не являетесь админом в канале.\n'
                        'Получите права администратора и повторите попытку')

    elif not is_admin.access_bot:
        await db.update_active_channel(chat_id=channel_id, is_active=False)
        await cb.answer('❌ Бот не является админом в канале. '
                        'Дайте боту права администратора и повторите попытку')

    else:
        await state.set_state('create_give')
        await state.update_data(data={
            'message_id': cb.message.message_id,
            'channel_id': channel_id,
        })
        await cb.message.edit_text('Отправьте конкурсный пост', reply_markup=kb.get_cancel_kb())


# принимает сообщение
@dp.message(StateFilter('create_give'))
async def preview_post(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()

    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=data['message_id']
    )

    text = msg.text if msg.text else msg.caption
    entities = msg.entities if msg.entities else msg.caption_entities
    media_id = await get_media_id(msg)
    keyboard = kb.get_create_post_kb()
    sent = await send_any_message(
        chat_id=msg.chat.id,
        text=text,
        entities=entities,
        media_id=media_id,
        content_type=msg.content_type,
        keyboard=keyboard
    )
    await state.update_data (data={'message_id': sent.message_id})


# начинает конкурс
@dp.callback_query(lambda cb: cb.data.startswith('start_give'))
async def send_give(cb: CallbackQuery, state: FSMContext):
    _, action = cb.data.split (':')

    if action == 'edit':
        await cb.answer('Отправьте новый пост', show_alert=True)

    else:
        try:
            await cb.answer('🎉 Конкурс начат\n\n'
                            '‼️ Проверьте является ли бот администратором в чате комментариев. '
                            'В противном случае бот не сможет регистрировать участников', show_alert=True)
            data = await state.get_data ()
            await state.clear()

            text = cb.message.text if cb.message.text else cb.message.caption
            entities = cb.message.entities if cb.message.entities else cb.message.caption_entities
            media_id = await get_media_id (cb.message)
            sent = await send_any_message(
                chat_id=data['channel_id'],
                text=text,
                entities=entities,
                media_id=media_id,
                content_type=cb.message.content_type,
            )

            entities = sent.entities if sent.entities else sent.caption_entities
            media_id = await get_media_id(sent)
            give_id = await db.add_give(
                chat_id=sent.chat.id,
                channel_name=sent.chat.title,
                message_id=sent.message_id,
                text=sent.text if sent.text else sent.caption,
                entities=proces_entities(entities),
                media_id=media_id,
                content_type=sent.content_type
            )

            give_info = await db.get_give_info(give_id)
            bottom_text = get_bottom_text(give_info)
            keyboard = kb.get_give_kb(give_id)

            if cb.message.text:
                await cb.message.edit_text(text=f'{cb.message.text}{bottom_text}', reply_markup=keyboard)
            else:
                await cb.message.edit_caption(caption=f'{cb.message.caption}{bottom_text}', reply_markup=keyboard)

        except Exception as ex:
            log_error(ex)
            await cb.message.answer('‼️ Произошёл сбой. Конкурс не может быть проведён')
