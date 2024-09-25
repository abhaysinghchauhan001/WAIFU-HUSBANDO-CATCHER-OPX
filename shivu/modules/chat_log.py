from pyrogram import Client, filters
import shivu  # Import your custom module

# Replace with your actual API ID and Hash
API_ID = '24089031'
API_HASH = '0615e3afe13ddaaf8e9ddbd3977d35ff'

# Your session name
app = Client("shivu", api_id=API_ID, api_hash=API_HASH)

GROUP_CHAT_ID = '-1002000314620'  # Replace with your group chat ID

@app.on_chat_member_updated(filters.new_chat_members)
async def log_added(client, update):
    print("New member added event triggered.")  # Debugging line
    for new_member in update.new_chat_members:
        print(f"New member: {new_member.first_name}")  # Log the new member's name
        chat = update.chat
        added_by = update.from_user if update.from_user else "Unknown User"
        member_count = chat.members_count if chat.members_count else 0  # Safely get member count
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
    left_by = update.left_chat_member
    member_count = chat.members_count if chat.members_count else 0  # Safely get member count
    log_message = (
        "<b>👋 Left Group</b>\n\n"
        f"<b>🆔 Group ID:</b> {chat.id}\n"
        f"<b>📛 Group Name:</b> {chat.title}\n"
        f"<b>👤 Left By:</b> {left_by.first_name}\n"
        f"<b>🔗 Username:</b> @{left_by.username or 'N/A'}\n"
        f"<b>👥 Total Members:</b> {member_count}"
    )
    await client.send_message(GROUP_CHAT_ID, log_message, parse_mode='html')