import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from shivu import user_collection, shivuu as app, LEAVELOGS, JOINLOGS

async def lul_message(chat_id: int, message: str):
    try:
        await app.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")

async def get_member_count(client: Client, chat_id: int) -> int:
    try:
        return await client.get_chat_members_count(chat_id)
    except Exception as e:
        print(f"Error getting member count: {e}")
        return 0  # Fallback to 0

async def get_chat_link(client: Client, chat_id: int) -> str:
    try:
        chat = await client.get_chat(chat_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        else:
            invite_link = await client.create_chat_invite_link(chat_id)
            return invite_link.invite_link if invite_link else "Invite link not available."
    except Exception as e:
        print(f"Error creating invite link: {e}")
        return "Invite link not available due to an error."

async def is_admin(client: Client, chat_id: int) -> bool:
    try:
        admin_list = await client.get_chat_administrators(chat_id)
        me = await client.get_me()
        return any(admin.user.id == me.id for admin in admin_list)
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    me = await client.get_me()
    
    if me.id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id

        member_count = await get_member_count(client, chat_id)
        chat_link = await get_chat_link(client, chat_id)

        lemda_text = (
            f"<b>🏠 Added To Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Added By:</b> {added_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> <a href='{chat_link}'>{chat_link}</a>"
        )
        
        if await is_admin(client, chat_id):
            await lul_message(JOINLOGS, lemda_text)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    me = await app.get_me()
    
    if me.id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id

        member_count = await get_member_count(client, chat_id)
        chat_link = await get_chat_link(client, chat_id)

        left_text = (
            f"<b>🚪 User Left Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Removed By:</b> {removed_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> <a href='{chat_link}'>{chat_title}</a>"
        )
        
        if await is_admin(client, chat_id):
            await lul_message(LEAVELOGS, left_text)