import sqlalchemy as sa
import typing as t

from db.base import METADATA, begin_connection


class ChannelRow(t.Protocol):
    id: int
    chat_id: int
    chat_title: str
    is_active: bool


ChannelTable = sa.Table(
    'channels',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('chat_id', sa.BigInteger, unique=True),
    sa.Column('chat_title', sa.String(255)),
    sa.Column('is_active', sa.Boolean),
)


# добавляет обновляет чат
async def add_update_channel(chat_id: int,  chat_title: str)-> None:
    async with begin_connection() as conn:
        result = await conn.execute(
            ChannelTable.select().where(ChannelTable.c.chat_id == chat_id)
        )
        chat = result.first()
        if not chat:
            await conn.execute (
                ChannelTable.insert ().values (chat_id=chat_id, chat_title=chat_title, is_active=True)
            )

        else:
            await conn.execute (
                ChannelTable.update ().values (
                    chat_title=chat_title,
                    is_active=True
                ).where(ChannelTable.c.chat_id == chat_id)
            )


# делает неактивным
async def update_active_channel(chat_id: int, is_active: bool) -> None:
    async with begin_connection() as conn:
        await conn.execute(
            ChannelTable.update ().values (is_active=is_active).where(ChannelTable.c.chat_id == chat_id)
        )


# возвращает все канал
async def get_all_channels() -> tuple[ChannelRow]:
    async with begin_connection() as conn:
        result = await conn.execute(
            ChannelTable.select().where(ChannelTable.c.is_active == True)
        )
    return result.all()


# возвращает канал по id
async def get_channel(channel_id: int) -> ChannelRow:
    async with begin_connection() as conn:
        result = await conn.execute(
            ChannelTable.select().where(ChannelTable.c.chat_id == channel_id)
        )
    return result.first()