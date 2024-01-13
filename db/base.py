import typing as t
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncConnection

from init import ENGINE

METADATA = sa.MetaData()


# Основное подключение
def begin_connection() -> t.AsyncContextManager[AsyncConnection]:
    return ENGINE.begin()


# подключение для проверки конкурсных сообщений
def connection_for_check_msg() -> t.AsyncContextManager[AsyncConnection]:
    return ENGINE.begin()

async def init_models():
    async with ENGINE.begin() as conn:
        await conn.run_sync(METADATA.create_all)
