import asyncio
import sys
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

        leaderboard_message += "✳️ <b>Top Users for <i>{waifu.get('name')}</i>:</b>\n\n"

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

#tags
@bot.on_message(filters.command("tags") & filters.user(OWNER_ID))
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