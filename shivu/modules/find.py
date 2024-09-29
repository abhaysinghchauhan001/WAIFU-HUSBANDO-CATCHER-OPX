import asyncio
from pyrogram import filters, Client, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot
from shivu import user_collection, collection

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
            "🔖<b>𝖯𝗅𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗍𝗁𝖺𝗍 𝖨𝖣 </b>☘️", 
            quote=True
        )

    waifu_id = message.command[1]
    waifu = await collection.find_one({'id': waifu_id})

    if not waifu:
        return await message.reply_text(
            "𝖭𝗈 𝗐𝖺𝗂𝖿𝗎 𝖿𝗈𝗎𝗻𝖽 𝗐𝗂𝗍𝗁 𝗍𝗁𝖺𝗍 𝖨𝖣 ❌", 
            quote=True
        )

    try:
        # Get the top 10 users with the most of this waifu in the current chat
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
        for i, user in enumerate(top_users, start=1):
            first_name = user.get('first_name', 'Unknown')[:15]
            character_count = user.get('count', 0)
            user_id = user.get('_id')
            leaderboard_message += f'<b>➥</b> <a href="tg://user?id={user_id}"> {first_name}...</a> <b>→</b> <b>≺ {character_count} ≻</b>\n'

        # Construct the caption
        caption = (
            f"🧩 <b>ᴡᴀɪғᴜ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:</b>\n\n"
            f"🪭 <b>ɴᴀᴍᴇ:</b> {waifu.get('name')}\n"
            f"⚕️ <b>ʀᴀʀɪᴛʏ:</b> {waifu.get('rarity')}\n"
            f"⚜️ <b>ᴀɴɪᴍᴇ:</b> {waifu.get('anime')}\n"
            f"🪅 <b>ɪᴅ:</b> {waifu.get('id')}\n"
        )

        # Append special tags if present
        for tag, description in tag_mappings.items():
            if tag in waifu.get('name', ''):
                caption += f"<b>event:</b>\n\n{description}\n\n"
                break  # Only add the first matching tag

        caption += (
            f"✳️ <b>ʜᴇʀᴇ ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ ᴛʜɪs ᴄʜᴀʀᴀᴄᴛᴇʀ 〽️</b>:\n\n"
            f"{leaderboard_message}"
        )

        # Reply with the waifu information and top users
        await message.reply_photo(photo=waifu.get('img_url', ''), caption=caption)

    except Exception as e:
        print(f"Error in find command: {e}")
        await message.reply_text("⚠️ An error occurred while processing your request.", quote=True)