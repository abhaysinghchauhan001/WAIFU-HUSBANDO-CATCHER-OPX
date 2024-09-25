from pyrogram import Client, filters
import shivu  # Import your custom module

# Your session name
app = Client("shivu")

GROUP_CHAT_ID = '-1002000314620'  # Replace with your group chat ID

@app.on_chat_member_updated(filters.new_chat_members)
async def log_added(client, update):
    print("New member added event triggered.")  # Debugging line
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
    await client.send_message(GROUP_CHAT_ID, log_message, parse_mode='html')

@app.on_chat_member_updated(filters.left_chat_member)
async def log_left(client, update):
    print("Member left event triggered.")  # Debugging line
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
    await client.send_message(GROUP_CHAT_ID, log_message, parse_mode='html')