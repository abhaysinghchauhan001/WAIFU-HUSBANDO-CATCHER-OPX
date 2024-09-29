import asyncio
from pyrogram import filters, Client, types as t
from pymongo import MongoClient
from shivu import shivuu as bot 

# Database setup
client = MongoClient("mongodb+srv://Epic2:w85NP8dEHmQxA5s7@cluster0.tttvsf9.mongodb.net/?retryWrites=true&w=majority")
db = client["character_catcherr"]  # Replace with your DB name
admin_collection = db["admins"]  # Collection for admin list

# Owner ID (replace with your actual owner ID)
OWNER_ID = 6584789596

# Command to add an admin
@bot.on_message(filters.command(["aadmin"]) & filters.reply)
async def add_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user  # Get the user info from the replied message
    new_admin_id = new_user.id

    # Check if the user is already an admin
    if admin_collection.find_one({"user_id": new_admin_id}):
        return await message.reply_text("⚠️ This user is already an admin.", quote=True)

    # Add the user to the admin list
    admin_collection.insert_one({
        "user_id": new_admin_id,
        "first_name": new_user.first_name,
        "username": new_user.username
    })

    # Notify the user that they have been added as admin
    try:
        await bot.send_message(new_admin_id, "🎉 You have been added as an admin!", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    # Reply to the user who issued the command
    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been added as an admin.", quote=True)

# Command to remove an admin
@bot.on_message(filters.command(["radmin"]) & filters.reply)
async def remove_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user
    if not new_user:
        return await message.reply_text("🔖 Please reply to a user's message to remove them.", quote=True)

    # Remove user from the admin list
    result = admin_collection.delete_one({"user_id": new_user.id})
    if result.deleted_count == 0:
        return await message.reply_text("⚠️ This user is not an admin.", quote=True)

    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been removed from admins.", quote=True)

# Command to check current admins
@bot.on_message(filters.command(["checkadmins"]) & filters.user(OWNER_ID))
async def check_admins(_, message: t.Message):
    admins = admin_collection.find()
    
    if admins.count() == 0:
        return await message.reply_text("⚠️ No admins found.", quote=True)

    admin_list = "\n".join([f"<a href='tg://user?id={admin['user_id']}'>{admin['first_name']} (ID: {admin['user_id']})</a>" for admin in admins])
    await message.reply_text(f"📋 <b>Current Admins:</b>\n\n{admin_list}", disable_web_page_preview=True)

# Command to upload a file (only for admins)
@bot.on_message(filters.command(["uploading"]) & filters.user(admin_collection.find()))
async def upload_file(_, message: t.Message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        file_name = document.file_name
        # Handle the document upload logic here
        await message.reply_text(f"File '{file_name}' uploaded successfully.")
    else:
        await message.reply_text("🔖 Please reply to a document to upload it.", quote=True)

# Command to check stats (only for admins)
@bot.on_message(filters.command(["wstats"]) & filters.user(admin_collection.find()))
async def check_stats(_, message: t.Message):
    total_users = await user_collection.count_documents({})
    total_admins = admin_collection.count_documents({})

    stats_message = (
        "📊 <b>Bot Statistics:</b>\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🛠️ Total Admins: {total_admins}\n"
    )

    await message.reply_text(stats_message)

# Shutdown code 
@bot.on_message(filters.command("shutdown") & filters.user(OWNER_ID))
async def shutdown(_, message: t.Message):
    await message.reply_text("🔒 Shutting down the bot...")
    await bot.stop()

#Help Command for owner 
@bot.on_message(filters.command("help") & filters.user(OWNER_ID))
async def help_command(_, message: t.Message):
    help_text = (
        "🆘 Available Commands:\n"
        "/faddadmin - Add an admin user.\n"
        "/fremovesudo - Remove a sudo user.\n"
        "/faddsudo - Add a sudo user.\n"
        "/fremoveadmin - Remove an admin user.\n"
        "/fupload - Upload a file (sudo only).\n"
        "/fstats - Show bot statistics (sudo only).\n"
        "/shutdown - Shutdown the bot.\n"
        "/checkadmins - List all admins.\n"
        "/checksudo - List all sudo users.\n"
    )
    await message.reply_text(help_text, quote=True)

# commands for owner 
@bot.on_message(filters.command("commands") & filters.user(OWNER_ID))
async def commands_command(_, message: t.Message):
    commands_text = (
        "📋 Owner Commands:\n"
        "/help - Show available commands.\n"
        "/status - Check the bot's status.\n"
        "/shutdown - Shut down the bot.\n"
        "/checkadmins - List all admins.\n"
        "/checksudo - List all sudo users.\n"
    )
    await message.reply_text(commands_text, quote=True)

#status command for owner 
@bot.on_message(filters.command("status") & filters.user(OWNER_ID))
async def status_command(_, message: t.Message):
    status_text = (
        "🔍 Bot Status:\n"
        f"🔧 Current Status: Running\n"
        f"👥 Total Admins: {len(admin_ids)}\n"
        f"🔑 Total Sudo Users: {len(sudo_ids)}\n"
        f"🗓️ Last Restart: <insert last restart time here>\n"
    )
    await message.reply_text(status_text, quote=True)