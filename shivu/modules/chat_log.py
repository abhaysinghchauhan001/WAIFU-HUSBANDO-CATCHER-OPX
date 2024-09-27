import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from shivu import user_collection, shivuu as app, LEAVELOGS, JOINLOGS

async def lul_message(chat_id: int, message: str):
    try:
        await app.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")
        await asyncio.sleep(2)  # Wait 2 seconds before retrying
        try:
            await app.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending message on retry: {e}")

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_id = message.chat.id
        chat_title = message.chat.title
        member_count = await client.get_chat_members_count(chat_id)

        # Attempt to create invite link
        try:
            invite_link = await client.create_chat_invite_link(chat_id)
            invite_url = invite_link.invite_link
        except Exception as e:
            print(f"Error creating invite link: {e}")
            invite_url = f"https://t.me/joinchat/{chat_id}"  # Fallback if unable to create invite

        lemda_text = (
            f"<b>🏠 User Added To Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Added By:</b> {added_by}\n"
            f"<b>👥 Total Members:</b> {member_count}\n"
            f"<b>🔗 Invite Link:</b> {invite_url}"
        )
        await lul_message(JOINLOGS, lemda_text)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡн ᴜsᴇʀ"
        chat_id = message.chat.id
        chat_title = message.chat.title
        
        # Attempt to get member count
        try:
            member_count = await client.get_chat_members_count(chat_id)
        except Exception as e:
            print(f"Error getting member count: {e}")
            member_count = "Unknown"

        left_message = (
            f"<b>🚪 User Left Group</b>\n\n"
            f"<b>🆔 Group ID:</b> {chat_id}\n"
            f"<b>📛 Group Name:</b> {chat_title}\n"
            f"<b>👤 Left By:</b> {remove_by}\n"
            f"<b>👥 Total Members:</b> {member_count}"
        )
        await lul_message(LEAVELOGS, left_message)