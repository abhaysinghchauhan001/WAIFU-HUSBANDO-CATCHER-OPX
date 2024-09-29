import asyncio
from pyrogram import filters, Client, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot
from shivu import user_collection, collection

# Owner ID (replace with your actual owner ID)
OWNER_ID = 123456789  # Replace with your Telegram user ID

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

@bot.on_message(filters.command(["find"]))
async def find(_, message: t.Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "🔖<b>𝖯𝗅𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗍𝗁𝖺𝗍 𝖭𝖽 </b>☘️", 
            quote=True
        )

    waifu_id = message.command[1]
    waifu = await collection.find_one({'id': waifu_id})

    if not waifu:
        return await message.reply_text(
            "𝖭𝗈 𝗐𝖺𝗂𝖿𝗎 𝖿𝗈𝗎𝗻𝖽 𝗐𝗂𝗍𝗁 𝗍𝗁𝖺𝗍 𝖭𝖽 ❌", 
            quote=True
        )

    try:
        # Construct the caption for waifu information
        caption = (
            f"🧩 <b>ᴡᴀɪғᴜ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:</b>\n\n"
            f"🪭 <b>ɴᴀᴍᴇ:</b>  <b><i>{waifu.get('name')}</i></b>\n"
            f"⚕️ <b>ʀᴀʀɪᴛʏ:</b>  <b><i>{waifu.get('rarity')}</i></b>\n"
            f"⚜️ <b>ᴀɴɪᴍᴇ:</b>  <b><i>{waifu.get('anime')}</i></b>\n"
            f"🪅 <b>ɪᴅ:</b>  <b><i>{waifu.get('id')}</i></b>\n"
        )

        # Append special tags if present
        matching_tags = [description for tag, description in tag_mappings.items() if tag in waifu.get('name', '')]
        if matching_tags:
            caption += f"<b>🧩 event:</b> {' '.join(matching_tags)}\n\n"

        # Add an inline button to view the leaderboard
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏆 View Top 10 Users", callback_data=f"top_users_{waifu_id}")]
        ])

        # Reply with the waifu information
        await message.reply_photo(photo=waifu.get('img_url', ''), caption=caption, reply_markup=inline_buttons)

    except Exception as e:
        print(f"Error in find command: {e}")
        await message.reply_text("⚠️ An error occurred while processing your request.", quote=True)

@bot.on_callback_query(filters.regex(r"top_users_(\w+)"))
async def show_top_users(_, callback_query: t.CallbackQuery):
    waifu_id = callback_query.data.split("_")[2]
    waifu = await collection.find_one({'id': waifu_id})

    if not waifu:
        return await callback_query.answer("No data found for this waifu.", show_alert=True)

    try:
        # Get the top users again
        top_users = await user_collection.aggregate([
            {'$match': {'characters.id': waifu_id}},
            {'$unwind': '$characters'},
            {'$match': {'characters.id': waifu_id}},
            {'$group': {'_id': '$id', 'first_name': {'$first': '$first_name'}, 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]).to_list(length=10)

        # Create the leaderboard message
        leaderboard_message = ""
        for user in top_users:
            first_name = user.get('first_name', 'Unknown')[:15]
            character_count = user.get('count', 0)
            user_id = user.get('_id')
            leaderboard_message += f'<b>➥</b> <a href="tg://user?id={user_id}">{first_name}...</a> <b>→</b> <b>≺ {character_count} ≻</b>\n'

        # Reply to the callback query with the leaderboard in a new message
        await callback_query.answer()
        await callback_query.message.reply_text(
            f"✳️ <b>Top Users for {waifu.get('name')}:</b>\n\n{leaderboard_message}",
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Error in show_top_users: {e}")
        await callback_query.answer("⚠️ An error occurred while processing your request.", show_alert=True)

@bot.on_message(filters.command(["tags"]))
async def show_tags(_, message: t.Message):
    # Check if the user is the owner
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⚠️ You do not have permission to access this command.", quote=True)

    # Create a formatted message for tag mappings
    tag_message = "📜 <b>Available Tags:</b>\n\n"
    
    for tag, description in tag_mappings.items():
        tag_message += f"<b>{tag}</b>: {description}\n"

    # Reply with the tags message
    await message.reply_text(tag_message, parse_mode="html")