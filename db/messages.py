import sqlalchemy as sa
import typing as t

from datetime import datetime

from init import TZ
from db.base import METADATA, begin_connection, connection_for_check_msg


class MessageRow(t.Protocol):
    id: int
    created_at: datetime
    chat_id: int
    message_id: int
    user_id: int
    full_name: str
    username: str
    give_id: int
    created_at: datetime
    text: str
    entities: str
    media_id: str
    content_type: str


MessageTable = sa.Table(
    'messages',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column ('created_at', sa.DateTime),
    sa.Column('chat_id', sa.BigInteger),
    sa.Column('message_id', sa.Integer),
    sa.Column('give_id', sa.Integer),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('text', sa.Text),
    sa.Column('entities', sa.Text),
    sa.Column('media_id', sa.String(255)),
    sa.Column('content_type', sa.String(255)),
)


# добавляет сообщение
async def add_message(
        chat_id: int,
        message_id: int,
        user_id: int,
        full_name: str,
        username: str,
        give_id: int,
        text: str,
        entities: str,
        media_id: str,
        content_type: str
) -> None:
    now = datetime.now(TZ)
    async with begin_connection() as conn:
        await conn.execute(
            MessageTable.insert().values(
                created_at=now,
                chat_id=chat_id,
                message_id=message_id,
                user_id=user_id,
                full_name=full_name,
                username=username,
                give_id=give_id,
                text=text,
                entities=entities,
                media_id=media_id,
                content_type=content_type
            )
        )


# возвращает инфо по гиву
async def get_give_info(give_id: int) -> dict:
    query = (
        MessageTable.select().where(MessageTable.c.give_id == give_id))
    async with begin_connection () as conn:
        message_count = await conn.execute (query)
        unique_user_count = await conn.execute (
            query.with_only_columns(sa.distinct(MessageTable.c.user_id))
        )

    return {'message_count': len(message_count.all()), 'unique_user_count': len(unique_user_count.all())}


# возвращает инфо по гиву
async def get_all_give_user_info(give_id: int, on_users: bool) -> list[MessageRow]:
    query = MessageTable.select ().with_only_columns(
        MessageTable.c.user_id,
        MessageTable.c.full_name,
        MessageTable.c.username
    ).where (MessageTable.c.give_id == give_id)

    if on_users:
        query = query.distinct()

    async with begin_connection () as conn:
        result = await conn.execute(query)

    return list(result.all())


# удаляет записи гива
async def get_winner(give_id: int, user_id: int) -> MessageRow:
    async with connection_for_check_msg () as conn:
        result = await conn.execute(
            MessageTable.select().where(MessageTable.c.give_id == give_id, MessageTable.c.user_id == user_id)
        )
    return result.first()


# удаляет записи гива
async def delete_give_messages(give_id: int) -> None:
    async with connection_for_check_msg () as conn:
        await conn.execute(
            MessageTable.delete().where(MessageTable.c.give_id == give_id)
        )