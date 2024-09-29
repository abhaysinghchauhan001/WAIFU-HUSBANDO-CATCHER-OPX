import asyncio
import sys
from pyrogram import filters, Client, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot
from shivu import user_collection, collection

# Owner ID (replace with your actual owner ID)
OWNER_ID = 6584789596

# List of admin and sudo IDs
admin_ids = []
sudo_ids = []

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

@bot.on_message(filters.command(["help"]))
async def help_command(_, message: t.Message):
    help_text = (
        "🆘 <b>Available Commands:</b>\n"
        "/faddadmin [user_id] - Add an admin\n"
        "/fremovesudo [user_id] - Remove a sudo user\n"
        "/faddsudo [user_id] - Add a sudo user\n"
        "/fupload - Upload a file (sudo only)\n"
        "/fstats - Check bot stats (sudo only)\n"
        "/shutdown - Shut down the bot (owner only)\n"
        "/checkadmins - List current admins\n"
        "/checksudo - List current sudo users\n"
        "/tags - Show available tags\n"
        "/find [waifu_id] - Find waifu info\n"
        "/config - Show current configuration\n"
        "/status - Show bot status\n"
    )
    await message.reply_text(help_text, disable_web_page_preview=True)

@bot.on_message(filters.command(["config"]))
async def config_command(_, message: t.Message):
    config_text = (
        "⚙️ <b>Current Configuration:</b>\n"
        f"Owner ID: {OWNER_ID}\n"
        f"Total Admins: {len(admin_ids)}\n"
        f"Total Sudo Users: {len(sudo_ids)}\n"
    )
    await message.reply_text(config_text, disable_web_page_preview=True)

@bot.on_message(filters.command(["status"]))
async def status_command(_, message: t.Message):
    status_text = (
        "✅ <b>Bot Status:</b>\n"
        "Running smoothly.\n"
        f"Total Users: {await user_collection.count_documents({})}\n"
    )
    await message.reply_text(status_text, disable_web_page_preview=True)

@bot.on_message(filters.command(["faddadmin"]) & filters.reply)
async def add_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user  # Get the user info from the replied message
    new_admin_id = new_user.id

    if new_admin_id in admin_ids:
        return await message.reply_text("⚠️ This user is already an admin.", quote=True)

    admin_ids.append(new_admin_id)
    
    # Notify the user that they have been added as admin
    try:
        await bot.send_message(new_admin_id, "🎉 You have been added as an admin!", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    # Reply to the user who issued the command
    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been added as an admin.", quote=True)

@bot.on_message(filters.command(["fremovesudo"]) & filters.reply)
async def remove_sudo(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    if message.reply_to_message:
        sudo_id_to_remove = message.reply_to_message.from_user.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("🔖 Please reply to a user's message to remove them from sudo.", quote=True)
        sudo_id_to_remove = int(message.command[1])

    if sudo_id_to_remove not in sudo_ids:
        return await message.reply_text("⚠️ This user is not a sudo user.", quote=True)

    sudo_ids.remove(sudo_id_to_remove)

    # Notify the user that they have been removed from sudo access
    try:
        await bot.send_message(sudo_id_to_remove, "🚫 You have been removed from sudo access.", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    # Reply to the user who issued the command
    await message.reply_text(f"✅ User with ID {sudo_id_to_remove} has been removed from sudo users.", quote=True)

@bot.on_message(filters.command(["faddsudo"]) & filters.reply)
async def add_sudo(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    new_user = message.reply_to_message.from_user  # Get the user info from the replied message
    new_sudo_id = new_user.id

    if new_sudo_id in sudo_ids:
        return await message.reply_text("⚠️ This user is already a sudo user.", quote=True)

    sudo_ids.append(new_sudo_id)

    # Notify the user that they have been granted sudo access
    try:
        await bot.send_message(new_sudo_id, "🎉 You have been granted sudo access!", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    # Reply to the user who issued the command
    await message.reply_text(f"✅ User @{new_user.username or new_user.first_name} has been added as a sudo user.", quote=True)

#FLEX

@bot.on_message(filters.command(["fupload"]) & filters.user(sudo_ids))
async def upload_file(_, message: t.Message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        file_name = document.file_name
        # Handle the document (e.g., save it)
        await message.reply_text(f"File '{file_name}' uploaded successfully.")
    else:
        await message.reply_text("🔖 Please reply to a document.", quote=True)

@bot.on_message(filters.command(["fstats"]) & filters.user(sudo_ids))
async def check_stats(_, message: t.Message):
    total_users = await user_collection.count_documents({})
    total_admins = len(admin_ids)
    total_sudo = len(sudo_ids)

    stats_message = (
        "📊 <b>Bot Statistics:</b>\n\n"
        f"👥 Total Users: {total_users}\n"
        f"🛠️ Total Admins: {total_admins}\n"
        f"🔑 Total Sudo Users: {total_sudo}\n"
    )

    await message.reply_text(stats_message)

@bot.on_message(filters.command(["shutdown"]) & filters.user(OWNER_ID))
async def shutdown(_, message: t.Message):
    await message.reply_text("🔴 Shutting down the bot...")
    await bot.stop()
    sys.exit()

@bot.on_message(filters.command(["checkadmins"]))
async def check_admins(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission.", quote=True)

    if not admin_ids:
        return await message.reply_text("⚠️ No admins found.", quote=True)

    admin_list = "\n".join([f"<a href='tg://user?id={admin_id}'>{admin_id}</a>" for admin_id in admin_ids])
    await message.reply_text(f"📋 <b>Current Admins:</b>\n\n{admin_list}", disable_web_page_preview=True)

@bot.on_message(filters.command(["checksudo"]))
async def check_sudos(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission.", quote=True)

    if not sudo_ids:
        return await message.reply_text("⚠️ No sudo users found.", quote=True)

    sudo_list = "\n".join([f"<a href='tg://user?id={sudo_id}'>{sudo_id}</a>" for sudo_id in sudo_ids])
    await message.reply_text(f"📋 <b>Current Sudo Users:</b>\n\n{sudo_list}", disable_web_page_preview=True)

# Additional functionalities...

@bot.on_message(filters.command(["find"]))
async def find(_, message: t.Message):
    if len(message.command) < 2:
        return await message.reply_text("🔖 Please provide the waifu ID.", quote=True)

    waifu_id = message.command[1]
    waifu = await collection.find_one({'id': waifu_id})

    if not waifu:
        return await message.reply_text("❌ No waifu found with that ID.", quote=True)

    caption = (
        f"🧩 <b>Waifu Information:</b>\n\n"
        f"🪭 <b>Name:</b> <b><i>{waifu.get('name')}</i></b> [{waifu.get('tag', '')}]\n"
        f"⚕️ <b>Rarity:</b> <b><i>{waifu.get('rarity')}</i></b>\n"
        f"⚜️ <b>Anime:</b> <b><i>{waifu.get('anime')}</i></b>\n"
        f"🪅 <b>ID:</b> <b><i>{waifu.get('id')}</i></b>\n"
    )

    matching_tags = [description for tag, description in tag_mappings.items() if tag in waifu.get('name', '')]
    if matching_tags:
        caption += f"<b>🧩 Event:</b> {' '.join(matching_tags)}\n\n"

    inline_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 View Top 10 Users", callback_data=f"top_users_{waifu_id}")]
    ])

    await message.reply_photo(photo=waifu.get('img_url', ''), caption=caption, reply_markup=inline_buttons)

@bot.on_callback_query(filters.regex(r"top_users_(\w+)"))
async def show_top_users(_, callback_query: t.CallbackQuery):
    waifu_id = callback_query.data.split("_")[2]
    waifu = await collection.find_one({'id': waifu_id})

    if not waifu:
        return await callback_query.answer("No data found for this waifu.", show_alert=True)

    try:
        top_users = await user_collection.aggregate([
            {'$match': {'characters.id': waifu_id}},
            {'$unwind': '$characters'},
            {'$match': {'characters.id': waifu_id}},
            {'$group': {'_id': '$id', 'first_name': {'$first': '$first_name'}, 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]).to_list(length=10)

        leaderboard_message = (
            f"🧩 <b>Waifu Information:</b>\n\n"
            f"🪭 <b>Name:</b> <b><i>{waifu.get('name')}</i></b> [{waifu.get('tag', '')}]\n"
            f"⚕️ <b>Rarity:</b> <b><i>{waifu.get('rarity')}</i></b>\n"
            f"⚜️ <b>Anime:</b> <b><i>{waifu.get('anime')}</i></b>\n"
            f"🪅 <b>ID:</b> <b><i>{waifu.get('id')}</i></b>\n\n"
        )

        # Matching tags logic
        matching_tags = [description for tag, description in tag_mappings.items() if tag in waifu.get('name', '')]
        if matching_tags:
            leaderboard_message += f"<b>🧩 Event:</b> {' '.join(matching_tags)}\n\n"

        leaderboard_message += "✳️ <b>Top Users for {waifu.get('name')}:</b>\n\n"

        for user in top_users:
            first_name = user.get('first_name', 'Unknown')[:15]
            character_count = user.get('count', 0)
            leaderboard_message += f"<b>➥</b> <a href=\"tg://user?id={user['_id']}\">{first_name}...</a> <b>→</b> <b>≺ {character_count} ≻</b>\n"

        await callback_query.message.edit_text(
            leaderboard_message,
            disable_web_page_preview=True,
            reply_markup=None
        )
        await callback_query.answer()

    except Exception as e:
        print(f"Error in show_top_users: {e}")
        await callback_query.answer("⚠️ An error occurred while processing your request.", show_alert=True)

# tags 

@bot.on_message(filters.command(["tags"]))
async def show_tags(_, message: t.Message):
    if message.from_user.id not in admin_ids and message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    tag_count = len(tag_mappings)
    tag_message = (
        "📜 <b>Available Tags:</b>\n"
        f"Total: <b>{tag_count}</b>\n\n"
        "<b>Tag List:</b>\n"
    )

    for tag, description in tag_mappings.items():
        tag_message += f"<b>{tag}</b>: {description}\n"

    tag_message += "\n🔗 Use these tags to enhance your experience!"

    await message.reply_text(tag_message, disable_web_page_preview=True)

@bot.on_message(filters.command(["removeadmin"]) & filters.reply)
async def remove_admin(_, message: t.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    if message.reply_to_message:
        admin_id_to_remove = message.reply_to_message.from_user.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("🔖 Please reply to a user's message to remove them from admin.", quote=True)
        admin_id_to_remove = int(message.command[1])

    if admin_id_to_remove not in admin_ids:
        return await message.reply_text("⚠️ This user is not an admin.", quote=True)

    admin_ids.remove(admin_id_to_remove)

    # Notify the user that they have been removed from admin access
    try:
        await bot.send_message(admin_id_to_remove, "🚫 You have been removed from admin access.", disable_notification=True)
    except Exception as e:
        print(f"Failed to notify the user: {e}")

    # Reply to the user who issued the command
    await message.reply_text(f"✅ User with ID {admin_id_to_remove} has been removed from admins.", quote=True)