import asyncio
from pyrogram import filters, Client, types as t
from pymongo import MongoClient
from shivu import shivuu as bot

# Database setup
client = MongoClient("mongodb+srv://Epic2:w85NP8dEHmQxA5s7@cluster0.tttvsf9.mongodb.net/?retryWrites=true&w=majority")
db = client["character_catcherr"]
admin_collection = db["admins"]

# Owner ID
OWNER_ID = 6584789596

# Tag mappings
tag_mappings = {
    '👘': '👘𝑲𝒊𝒎𝒐𝒏𝒐👘',
    '☃️': '☃️𝑾𝒊𝒏𝒕𝒆𝒓☃️',
    '🐰': '🐰𝑩𝒖𝒏𝒏𝒚🐰',
    '🎮': '🎮𝑮𝒂𝒎𝒆🎮',
    '🎄': '🎄𝑪𝒓𝒊𝒔𝒕𝒎𝒂𝒔🎄',
    '🎃': '🎃𝑯𝒆𝒍𝒍𝒐𝒘𝒆𝒆𝒏🎃',
    '🏖️': '🏖️𝑺𝒖𝒎𝒎𝒆𝒓🏖️',
    '🧹': '🧹𝑴𝒂𝒅𝒆🧹',
    '🥻': '🥻𝑺𝒂𝒓𝒆𝒆🥻',
    '☔': '☔𝑴𝒐𝒏𝒔𝒐𝒐𝒏☔',
    '🎒': '🎒𝑺𝒄𝒉𝒐𝒐𝒍🎒',
    '🎩': '🎩𝑻𝒖𝒙𝒆𝒅𝒐🎩',
    '👥': '👥𝐃𝐮𝐨👥',
    '🤝🏻': '🤝🏻𝐆𝐫𝐨𝐮𝐩🤝🏻',
    '👑': '👑𝑳𝒐𝒓𝒅👑',
    '🩺': '🩺𝑵𝒖𝒓𝒔𝒆🩺',
    '💍': '💍𝑾𝒆𝒅𝒅𝒊𝒏𝒈💍',
    '🎊': '🎊𝑪𝒉𝒆𝒆𝒓𝒍𝒆𝒂𝒅𝒆𝒓𝒔🎊',
    '⚽': '⚽𝑺𝒐𝒄𝒄𝒆𝒓⚽',
    '🏀': '🏀𝑩𝒂𝒔𝒌𝒆𝒕𝒃𝒂𝒍𝒍🏀',
    '💐': '💐𝑮𝒓𝒐𝒐𝒎💐',
    '🥂': '🥂𝑷𝒂𝒓𝒕𝒚🥂',
    '💞': '💞𝑽𝒂𝒍𝒆𝒏𝒕𝒊𝒏𝒆💞',
}

# Fetch existing admin IDs
admin_ids = [admin['user_id'] for admin in await admin_collection.find().to_list(length=None)]
sudo_ids = []  # Populate this as needed

# Command to add an admin
@bot.on_message(filters.command(["aadmin"]) & filters.reply)
async def add_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user
    new_admin_id = new_user.id

    if admin_collection.find_one({"user_id": new_admin_id}):
        return await message.reply_text("⚠️ This user is already an admin.", quote=True)

    admin_collection.insert_one({
        "user_id": new_admin_id,
        "first_name": new_user.first_name,
        "username": new_user.username
    })

    try:
        await bot.send_message(new_admin_id, "🎉 You have been added as an admin!", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been added as an admin.", quote=True)

# Command to remove an admin
@bot.on_message(filters.command(["radmin"]) & filters.reply)
async def remove_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user
    if not new_user:
        return await message.reply_text("🔖 Please reply to a user's message to remove them.", quote=True)

    result = admin_collection.delete_one({"user_id": new_user.id})
    if result.deleted_count == 0:
        return await message.reply_text("⚠️ This user is not an admin.", quote=True)

    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been removed from admins.", quote=True)

# Command to check current admins
@bot.on_message(filters.command(["checkadmins"]) & filters.user(OWNER_ID))
async def check_admins(_, message: t.Message):
    admins = await admin_collection.find().to_list(length=None)

    if len(admins) == 0:
        return await message.reply_text("⚠️ No admins found.", quote=True)

    admin_list = "\n".join([f"<a href='tg://user?id={admin['user_id']}'>{admin['first_name']} (ID: {admin['user_id']})</a>" for admin in admins])
    await message.reply_text(f"📋 <b>Current Admins:</b>\n\n{admin_list}", disable_web_page_preview=True)

# Command to upload a file (only for admins)
@bot.on_message(filters.command(["uploading"]) & filters.user(admin_ids))
async def upload_file(_, message: t.Message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        file_name = document.file_name
        # Handle the document upload logic here
        await message.reply_text(f"File '{file_name}' uploaded successfully.")
    else:
        await message.reply_text("🔖 Please reply to a document to upload it.", quote=True)

# Command to check stats (only for admins)
@bot.on_message(filters.command(["wstats"]) & filters.user(admin_ids))
async def check_stats(_, message: t.Message):
    total_users = await user_collection.count_documents({})
    total_admins = await admin_collection.count_documents({})

    stats_message = (
        "📊 <b>Bot Statistics:</b>\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🛠️ Total Admins: {total_admins}\n"
    )

    await message.reply_text(stats_message)

# Shutdown command
@bot.on_message(filters.command("shutdown") & filters.user(OWNER_ID))
async def shutdown(_, message: t.Message):
    await message.reply_text("🔒 Shutting down the bot...")
    await bot.stop()

# Help Command for owner 
@bot.on_message(filters.command("help") & filters.user(OWNER_ID))
async def help_command(_, message: t.Message):
    help_text = (
        "🆘 Available Commands:\n"
        "/aadmin - Add an admin user.\n"
        "/radmin - Remove an admin user.\n"
        "/checkadmins - List all admins.\n"
        "/uploading - Upload a file (admin only).\n"
        "/wstats - Show bot statistics (admin only).\n"
        "/shutdown - Shutdown the bot.\n"
        "/tags - Show available tags.\n"
    )
    await message.reply_text(help_text, quote=True)

# Command to show available tags
@bot.on_message(filters.command("tags") & filters.user(lambda u: u.id == OWNER_ID or admin_collection.find_one({"user_id": u.id})))
async def list_tags(_, message: t.Message):
    if not tag_mappings:
        return await message.reply_text("⚠️ No tags available at the moment.", quote=True)

    tags_list = "\n".join([f"<b>{tag}</b>: <i>{description}</i>" for tag, description in tag_mappings.items()])

    response = (
        "🔖 <b>Available Tags:</b>\n\n" +
        tags_list + 
        "\n\n✨ Use these tags to enhance your search experience!"
    )

    await message.reply_text(response, quote=True)

# Status command for owner 
@bot.on_message(filters.command("status") & filters.user(OWNER_ID))
async def status_command(_, message: t.Message):
    total_admins = await admin_collection.count_documents({})
    total_sudo_users = len(sudo_ids)  # Populate as needed

    status_text = (
        "🔍 Bot Status:\n"
        f"🔧 Current Status: Running\n"
        f"👥 Total Admins: {total_admins}\n"
        f"🔑 Total Sudo Users: {total_sudo_users}\n"
        f"🗓️ Last Restart: <insert last restart time here>\n"
    )
    await message.reply_text(status_text, quote=True)

# Main function to run the bot
if __name__ == "__main__":
    bot.run()