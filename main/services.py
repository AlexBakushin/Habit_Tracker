from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from django.conf import settings


api_id = settings.API_ID
api_hash = settings.API_HASH
bot_token = settings.TELEGRAM_BOT_TOKEN


async def get_user(username):
    async with TelegramClient(bot_token, api_id, api_hash) as client:
        user = await client(GetFullUserRequest(username))
    return user


async def main(username):
    data = await get_user(username)
    position = data.stringify().find("id=")
    user_id_full = data.stringify()[position + 3:position + 13]
    if user_id_full.endswith(","):
        user_id = user_id_full[:-1]
        return user_id
    else:
        return user_id_full
