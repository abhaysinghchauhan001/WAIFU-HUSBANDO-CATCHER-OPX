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

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id

        # Fallback for member count
        member_count = 0
        try:
            member_count = await client.get_chat_members_count(chat_id)
        except Exception as e:
            print(f"Error getting member count: {e}")

        # Generate invite link
        try:
            if message.chat.username:
                chat_link = f"https://t.me/{message.chat.username}"
            else:
                invite_link = await client.create_chat_invite_link(chat_id)
                chat_link = invite_link.invite_link if invite_link else "Invite link not available."
        except Exception as e:
            chat_link = "Invite link not available due to an error."
            print(f"Error creating invite link: {e}")

        lemda_text = (
            f"<b>🏠 Added To Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Added By:</b> {added_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> <a href='{chat_link}'>{chat_link}</a>"
        )
        await lul_message(JOINLOGS, lemda_text)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id

        # Fallback for member count
        member_count = 0
        try:
            member_count = await client.get_chat_members_count(chat_id)
        except Exception as e:
            print(f"Error getting member count: {e}")

        # Generate invite link
        try:
            if message.chat.username:
                chat_link = f"https://t.me/{message.chat.username}"
            else:
                invite_link = await client.create_chat_invite_link(chat_id)
                chat_link = invite_link.invite_link if invite_link else "Invite link not available."
        except Exception as e:
            chat_link = "Invite link not available due to an error."
            print(f"Error creating invite link: {e}")

        left_text = (
            f"<b>🚪 User Left Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Removed By:</b> {removed_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Group Link:</b> <a href='{chat_link}'>{chat_title}</a>"
        )
        await lul_message(LEAVELOGS, left_text)