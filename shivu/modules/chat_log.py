from pyrogram import Client, filters
import shivu  # Import your custom module

# Your session name
app = Client("shivuu")

CHANNEL_ID = '-1002000314620'  # Replace with your channel ID

@app.on_chat_member_updated(filters.status_update.new_chat_members)
async def log_added(client, update):
    chat = update.chat
    added_by = update.from_user
    member_count = chat.members_count  # Get the current member count
    log_message = (
        "<b>🏠 Added To New Group</b>\n\n"
        f"<b>🆔 Group ID:</b> {chat.id}\n"
        f"<b>📛 Group Name:</b> {chat.title}\n"
        f"<b>👤 Added By:</b> {added_by.first_name}\n"
        f"<b>🔗 Username:</b> @{added_by.username or 'N/A'}\n"
        f"<b>👥 Total Members:</b> {member_count}"
    )
    await client.send_message(CHANNEL_ID, log_message, parse_mode='html')

@app.on_chat_member_updated(filters.status_update.left_chat_member)
async def log_left(client, update):
    chat = update.chat
    left_by = update.from_user
    member_count = chat.members_count  # Get the updated member count
    log_message = (
        "<b>👋 Left Group</b>\n\n"
        f"<b>🆔 Group ID:</b> {chat.id}\n"
        f"<b>📛 Group Name:</b> {chat.title}\n"
        f"<b>👤 Left By:</b> {left_by.first_name}\n"
        f"<b>🔗 Username:</b> @{left_by.username or 'N/A'}\n"
        f"<b>👥 Total Members:</b> {member_count}"
    )
    await client.send_message(CHANNEL_ID, log_message, parse_mode='html')