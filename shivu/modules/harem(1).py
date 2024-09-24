from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from html import escape
import random
import math
from itertools import groupby
from shivu import collection, user_collection, application

async def harem(update: Update, context: CallbackContext, page=0, edit=False) -> None:
    user_id = update.effective_user.id
    harem_mode_mapping = {
        "common": "🟢 Common",
        "rare": "🟣 Rare",
        "legendary": "🟡 Legendary",
        "spacial_edition": "💮 Spacial Edition",
        "premium_edition": "🔮 Premium Edition",
        "supreme": "🎗️ Supreme",
        "default": None
    }
    
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text(
    "<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇɢɪsᴛᴇʀ ғɪʀsᴛ ʙʏ sᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ ɪɴ DM.</b>",
    parse_mode="HTML"
)
        return

    characters = user.get('characters', [])
    fav_character_id = user.get('favorites', [])[0] if 'favorites' in user else None
    fav_character = None

    if fav_character_id:
        for c in characters:
            if isinstance(c, dict) and c.get('id') == fav_character_id:
                fav_character = c
                break

    hmode = user.get('smode')
    if hmode == "default" or hmode is None:
        characters = [char for char in characters if isinstance(char, dict)]
        characters = sorted(characters, key=lambda x: (x.get('anime', ''), x.get('id', '')))
        rarity_value = "all"
    else:
        rarity_value = harem_mode_mapping.get(hmode, "Unknown Rarity")
        characters = [char for char in characters if isinstance(char, dict) and char.get('rarity') == rarity_value]
        characters = sorted(characters, key=lambda x: (x.get('anime', ''), x.get('id', '')))

    if not characters:
        await update.message.reply_text(
    f"<b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ</b> (<i>{rarity_value}</i>) <b>ᴡᴀɪғᴜ ᴘʟᴇᴀsᴇ ᴄʜᴀɴɢᴇ ɪᴛ ғʀᴏᴍ</b> /hmode.",
    parse_mode="HTML"
)
        return

    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}
    total_pages = math.ceil(len(characters) / 10)
    if page < 0 or page >= total_pages:
        page = 0

    harem_message = f"<b>{escape(update.effective_user.first_name)}'s (<i>{rarity_value}</i>) ʜᴀʀᴇᴍ - ᴘᴀɢᴇ {page + 1}/{total_pages}</b>\n"
    current_characters = characters[page * 10:(page + 1) * 10]
    current_grouped_characters = {anime: list(chars) for anime, chars in groupby(current_characters, key=lambda x: x['anime'])}

    included_characters = set()
    for anime, chars in current_grouped_characters.items():
        user_anime_count = sum(1 for char in user['characters'] if isinstance(char, dict) and char.get('anime') == anime)
        total_anime_count = await collection.count_documents({"anime": anime})

        harem_message += f'\n<b>𖤍</b> <b>{anime} ｛{user_anime_count}/{total_anime_count}｝</b>\n'

        for character in chars:
            if character['id'] not in included_characters:
                count = character_counts[character['id']]
                formatted_id = f"{int(character['id']):04d}"
                harem_message += f'<b>𒄬</b> {formatted_id}  [ {character["rarity"][0]} ] {character["name"]} ×{count}\n'
                included_characters.add(character['id'])

    keyboard = [
        [InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="ignore")],
        [InlineKeyboardButton("Inline", switch_inline_query_current_chat=f"collection.{user_id}")]
    ]

    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⤂", callback_data=f"harem:{page - 1}:{user_id}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("⤃", callback_data=f"harem:{page + 1}:{user_id}"))
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = update.message or update.callback_query.message

    if 'favorites' in user and user['favorites']:
        fav_character_id = user['favorites'][0]
        fav_character = next((c for c in user['characters'] if isinstance(c, dict) and c.get('id') == fav_character_id), None)
        if fav_character and 'img_url' in fav_character:
            if edit:
                await message.edit_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
            else:
                await message.reply_photo(photo=fav_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
        else:
            if edit:
                await message.edit_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
            else:
                await message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
    else:
        if user['characters']:
            random_character = random.choice(user['characters'])
            if 'img_url' in random_character:
                if edit:
                    await message.edit_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
                else:
                    await message.reply_photo(photo=random_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
            else:
                if edit:
                    await message.edit_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
                else:
                    await message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
        else:
            if edit:
                await message.edit_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
            else:
                await message.reply_text(harem_message, reply_markup=reply_markup)

async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data
    _, page, user_id = data.split(':')
    page = int(page)
    user_id = int(user_id)
    if query.from_user.id != user_id:
        await query.answer("It's Not Your Harem", show_alert=True)
        return
    await query.answer()

    await harem(update, context, page, edit=True)

async def set_hmode(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    keyboard = [
        [
            InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ", callback_data="default"),
            InlineKeyboardButton("ʀᴀʀɪᴛʏ", callback_data="rarity"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.message.reply_photo(
        photo="https://graph.org/file/4b0da20b223036b6c7989.jpg",
        caption=f"{escape(update.effective_user.first_name)} <b>ᴘʟᴇᴀꜱᴇ ᴄʜᴏᴏꜱᴇ ʀᴀʀɪᴛʏ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ꜱᴇᴛ ᴀꜱ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ</>",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def hmode_rarity(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🟢 Common", callback_data="common"),
         InlineKeyboardButton("🟣 Rare", callback_data="rare")],
        [InlineKeyboardButton("🟡 Legendary", callback_data="legendary"),
         InlineKeyboardButton("💮 Special Edition", callback_data="spacial_edition")],
        [InlineKeyboardButton("🔮 Premium Edition", callback_data="premium_edition"),
         InlineKeyboardButton("🎗️ Supreme", callback_data="supreme")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.edit_message_caption(
    caption="<b>ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ʀᴀʀɪᴛʏ ᴀꜱ :</b> <i>ʀᴀʀɪᴛʏ</i>",
    reply_markup=reply_markup,
    parse_mode="HTML"
)
    await query.answer()

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "default":
        await user_collection.update_one({'id': user_id}, {'$set': {'smode': data}})
        await query.answer()
        await query.edit_message_caption(
    caption="<b>ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ʀᴀʀɪᴛʏ ᴀꜱ :</b> <i>ᴅᴇꜰᴀᴜʟᴛ</i>",
    parse_mode="HTML"
)
    elif data == "rarity":
        await hmode_rarity(update, context)
    else:
        await user_collection.update_one({'id': user_id}, {'$set': {'smode': data}})
        await query.answer()
        await query.edit_message_caption(
    f"<b>ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ʀᴀʀɪᴛʏ ᴀꜱ :</b> <i>{data}</I>",
    parse_mode="HTML"
)

# Command Handlers
application.add_handler(CommandHandler(["myslave", "slaves", "grabbers"], harem, block=False))
harem_handler = CallbackQueryHandler(harem_callback, pattern='^harem', block=False)
application.add_handler(harem_handler)
application.add_handler(CommandHandler("hmode", set_hmode))
application.add_handler(CallbackQueryHandler(button, pattern='^default$|^rarity$|^common$|^rare$|^legendary$|^spacial_edition$|^premium_edition$|^supreme$', block=False))