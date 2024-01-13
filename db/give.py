import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection, connection_for_check_msg


class GiveRow(t.Protocol):
    id: int
    start_date: date
    channel_name: str
    chat_id: int
    message_id: int
    is_active: bool
    text: str
    entities: str
    media_id: str
    content_type: str


GiveTable = sa.Table(
    'give',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('start_date', sa.Date),
    sa.Column('channel_name', sa.String(255)),
    sa.Column('chat_id', sa.BigInteger),
    sa.Column('message_id', sa.Integer),
    sa.Column('is_active', sa.Boolean),
    sa.Column('text', sa.String(255)),
    sa.Column('entities', sa.Text),
    sa.Column('media_id', sa.String(255)),
    sa.Column('content_type', sa.String(255)),
)


# добавляет обновляет чат
async def add_give(
        chat_id: int,
        channel_name: str,
        message_id: int,
        text: str,
        entities: str,
        media_id: str,
        content_type: str
) -> int:
    today = datetime.now(TZ).date()
    async with begin_connection() as conn:
        result = await conn.execute(
            GiveTable.insert().values(
                start_date=today,
                channel_name=channel_name,
                chat_id=chat_id,
                message_id=message_id,
                is_active=True,
                text=text,
                entities=entities,
                media_id=media_id,
                content_type=content_type
            )
        )
    return result.lastrowid


# обновляет статус
async def update_active_give(give_id: int, is_active: bool) -> None:
    async with begin_connection() as conn:
        await conn.execute(
            GiveTable.update ().values (is_active=is_active).where(GiveTable.c.id == give_id)
        )


# обновляет статус
async def get_all_give(chat_id: int = 0) -> tuple[GiveRow]:
    query = GiveTable.select ().where(GiveTable.c.is_active == True)

    if chat_id:
        query = query.where(GiveTable.c.chat_id == chat_id)

    async with begin_connection() as conn:
        result = await conn.execute(query)
    return result.all()


# обновляет статус
async def get_give(
        give_id: int = None,
        chat_id: int = None,
        message_id: int = None
) -> GiveRow:
    query = GiveTable.select ()

    if give_id:
        query = query.where(GiveTable.c.id == give_id)

    if chat_id:
        query = query.where(GiveTable.c.chat_id == give_id)

    if message_id:
        query = query.where(GiveTable.c.message_id == give_id)

    async with begin_connection() as conn:
        result = await conn.execute (query)

    return result.first()


# проверяет конкурсное ли сообщение
async def check_give_message(chat_id: int, message_id: int) -> t.Union[GiveRow, None]:
    async with connection_for_check_msg () as conn:
        result = await conn.execute(
            GiveTable.select().where(
                GiveTable.c.chat_id == chat_id,
                GiveTable.c.message_id == message_id,
                GiveTable.c.is_active == True
            )
        )
    return result.first()


# удаляет гив
async def delete_give(give_id: int) -> None:
    async with connection_for_check_msg () as conn:
        await conn.execute(
            GiveTable.delete().where(GiveTable.c.id == give_id)
        )
