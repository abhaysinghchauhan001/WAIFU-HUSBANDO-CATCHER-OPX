#🔹𝐅𝐋𝐄𝐗 𝐁𝐎𝐘🔹 💠:
#Sᴘɪʀɪᴛ⚡ᴍᴏɴᴀʀᴄʜ:
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext
from itertools import groupby
import math
import random
from html import escape
from shivu import collection, user_collection, application

MAX_CAPTION_LENGTH = 1024

# Define rarity emojis
RARITY_MAPPING = {
    '🟤 Bronze waifu': '🟤',
    '⚪ Silver waifu': '⚪',
    '🟡 Gold waifu': '🟡',
    '💎 Daimond waifu': '💎',
    '💮 Elite waifu': '💮',
    '🎗 Master waifu': '🎗'
}

async def harem(update: Update, context: CallbackContext, page=0) -> None:
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})
    if not user:
        message = 'You Have Not Guessed any Characters Yet..'
        if update.message:
            await update.message.reply_text(message)
        else:
            await update.callback_query.edit_message_text(message)
        return

    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))
    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}
    rarity_mode = await get_user_rarity_mode(user_id)

    if rarity_mode!= 'All':
        characters = [char for char in characters if char.get('rarity') == rarity_mode]

    total_pages = math.ceil(len(characters) / 15)
    if page < 0 or page >= total_pages:
        page = 0

    harem_message = f"{escape(update.effective_user.first_name)}'s Harem - Page {page+1}/{total_pages}\n\n"
    current_characters = characters[page*15:(page+1)*15]
    current_grouped_characters = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}

    for anime, characters in current_grouped_characters.items():
        harem_message += f"➥ {anime} ｛{len(characters)}/{character_counts[characters[0]['id']]}｝\n"
        for character in characters:
            count = character_counts[character['id']]
            rarity = character['rarity']
            rarity_emoji = RARITY_MAPPING.get(rarity, 'Unknown')
            harem_message += f"➹ {character['id']} [{rarity_emoji}] {character['name']} ×{count}\n"
        harem_message += "\n"

    if len(harem_message) > MAX_CAPTION_LENGTH:
        harem_message = harem_message[:MAX_CAPTION_LENGTH]

    total_count = len(user['characters'])
    keyboard = [
        [InlineKeyboardButton(f"See Collection ({total_count})", switch_inline_query_current_chat=f"collection.{user_id}")]
    ]

    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"harem:{page-1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"harem:{page+1}"))
        keyboard.append(nav_buttons)
    
    # Add a close button
    keyboard.append([InlineKeyboardButton("Close", callback_data="close")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if 'favorites' in user and user['favorites']:
            fav_character_id = user['favorites'][0]
            fav_character = next((c for c in user['characters'] if c['id'] == fav_character_id), None)
            if fav_character and 'img_url' in fav_character:
                if update.message:
                    await update.message.reply_photo(photo=fav_character['img_url'], caption=harem_message, reply_markup=reply_markup)
                else:
                    try:
                        await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup)
                    except BadRequest:
                        await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
            else:
                await _send_harem_message(update, harem_message, reply_markup)
        else:
            await _send_harem_message(update, harem_message, reply_markup, user['characters'])
    except Exception as e:
        print(f"Failed to edit message: {e}")

async def _send_harem_message(update, harem_message, reply_markup, characters=None):
    if characters:
        random_character = random.choice(characters)
        if 'img_url' in random_character:
            if update.message:
                await update.message.reply_photo(photo=random_character['img_url'], caption=harem_message, reply_markup=reply_markup)
            else:
                try:
                    await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup)
                except BadRequest:
                    await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)
        else:
            await _send_text_message(update, harem_message, reply_markup)
    else:
        await _send_text_message(update, harem_message, reply_markup)

async def _send_text_message(update, text, reply_markup):
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        try:
            await update.callback_query.edit_message_caption(caption=text, reply_markup=reply_markup)
        except BadRequest:
            await update.callback_query.edit_message_reply_markup(reply_markup=reply_markup)

async def haremmode(update: Update, context: CallbackContext):
    rarities_buttons = [
        [InlineKeyboardButton("🟤 Bronze waifu", callback_data="rarity:🟤 Bronze waifu"), InlineKeyboardButton("⚪ Silver waifu", callback_data="rarity:⚪ Silver waifu"), InlineKeyboardButton("🟡 Gold waifu", callback_data="rarity:🟡 Gold waifu")],
        [InlineKeyboardButton("💎 Daimond waifu", callback_data="rarity:💎 Daimond waifu"), InlineKeyboardButton("💮 Elite waifu", callback_data="rarity:💮 Elite waifu"), InlineKeyboardButton("🎗 Master waifu", callback_data="rarity:🎗 Master waifu")],
        [InlineKeyboardButton("All", callback_data="rarity:All")]
    ]

    reply_markup = InlineKeyboardMarkup(rarities_buttons)

    image_url = "https://graph.org/file/784e1f73497c553604b46.jpg" # Replace with your actual image URL

    if update.message:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_url,
            caption="Select a rarity mode:",  
            reply_markup=reply_markup  
        )
    else:
        await update.callback_query.message.edit_media(
            media=InputMediaPhoto(media=image_url, caption="Select a rarity mode:"),
            reply_markup=reply_markup
        )

async def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")

async def get_user_rarity_mode(user_id: int) -> str:
    user = await user_collection.find_one({'id': user_id})
    return user.get('rarity_mode', 'All') if user else 'All'

async def update_user_rarity_mode(user_id: int, rarity_mode: int) -> None:
    await user_collection.update_one({'id': user_id}, {'$set': {'rarity_mode': rarity_mode}}, upsert=True)

async def pagination_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    print(f"Received callback query: {data}")
    page = int(data.split(':')[1])
    await harem(update, context, page)

async def haremmode_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    print(f"Received callback query: {data}")
    if data.startswith('rarity:'):
        rarity_mode = int(data.split(':')[1])
        user_id = update.effective_user.id
        await update_user_rarity_mode(user_id, rarity_mode)
        await query.answer()
        await harem(update, context, 0)  # Call the harem function with page 0
    else:
        await query.answer(text='Invalid callback query')

application.add_handler(CommandHandler("hmode", haremmode))
application.add_handler(CommandHandler("harem", harem))

application.add_handler(CallbackQueryHandler(pagination_callback, pattern='^harem:'))
application.add_handler(CallbackQueryHandler(lambda u, c: u.callback_query.message.delete(), pattern='^close$'))
application.add_handler(CallbackQueryHandler(haremmode_callback, pattern=r'rarity:\d+'))

application.add_error_handler(error)