from aiogram.enums.chat_member_status import ChatMemberStatus

import db
from init import bot, MY_ID
from utils.objects import AccessResult


async def check_access(user_id: int, channels: tuple[db.ChannelRow]) -> bool:
    access = False
    for channel in channels:
        result = await bot.get_chat_member(
            chat_id=channel.chat_id,
            user_id=user_id
        )
        if result.status == ChatMemberStatus.ADMINISTRATOR or result.status == ChatMemberStatus.CREATOR:
            access = True
            break

    return access


# проверяет не кикнули ли с канала
async def check_is_channel_admin(channel_id: int, user_id: int) -> AccessResult:
    access_bot = False
    access_user = False
    admins = await bot.get_chat_administrators (channel_id)
    for admin in admins:
        if admin.user.id == MY_ID:
            access_bot = True
        if admin.user.id == user_id:
            access_user = True

    return AccessResult(access_bot, access_user)
