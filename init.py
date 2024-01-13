from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

import logging
import traceback
from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from pytz import timezone

from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass


load_dotenv ()
loop = asyncio.get_event_loop()
dp = Dispatcher()
bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)

ENGINE = create_async_engine(url=getenv('DB_URL'))
MY_ID = int(getenv('MY_ID'))
TZ = timezone('europe/moscow')
# Europe/Moscow
DATE_FORMAT = '%d.%m'
DATETIME_FORMAT = '%d.%m:%Y %H:%M'


async def set_main_menu() -> None:
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запустить бот'),
        BotCommand (command='/new_give',
                    description='Начать новый конкурс'),
        BotCommand (command='/give_away',
                    description='Провести конкурс'),
    ]

    await bot.set_my_commands(main_menu_commands)


def log_error(message):
    timestamp = datetime.now (TZ)
    filename = traceback.format_exc () [1]
    line_number = traceback.format_exc () [2]
    logging.error (f'{timestamp} {filename} {line_number}: {message}')