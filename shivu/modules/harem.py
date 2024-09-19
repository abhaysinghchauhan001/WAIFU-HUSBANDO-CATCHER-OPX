from telegram import Update
from itertools import groupby
import math
import random
from html import escape
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from shivu import collection, user_collection, application

async def harem(update: Update, context: CallbackContext, page=0) -> None:
    user_id = update.effective_user.id
    user = await user_collection.find_one({'id': user_id})

    if not user:
        response_text = '𝙔𝙤𝙪 𝙃𝙖𝙫𝙚 𝙉𝙤𝙩 𝙂𝙧𝙖𝙗 𝙖𝙣𝙮 𝙒𝙖𝙞𝙛𝙪 𝙔𝙚𝙩...'
        await (update.message.reply_text(response_text) if update.message else update.callback_query.edit_message_text(response_text))
        return

    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))
    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}
    unique_characters = list({character['id']: character for character in characters}.values())
    total_pages = math.ceil(len(unique_characters) / 7)
    page = max(0, min(page, total_pages - 1))

    harem_message = f"<b>{escape(update.effective_user.first_name)}'s Harem - Page {page + 1}/{total_pages}</b>\n"
    current_characters = unique_characters[page * 7:(page + 1) * 7]
    current_grouped_characters = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}

    for anime, characters in current_grouped_characters.items():
        harem_message += f'\n𖤍 <b>{anime} ｛{len(characters)}/{await collection.count_documents({"anime": anime})}｝</b>\n'
        harem_message += '⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'
        for character in characters:
            count = character_counts[character['id']]
            harem_message += f'𒄬 {character["id"]} [ {character["rarity"][0]} ] {character["name"]} ×{count}\n'
        harem_message += '⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋⚋\n'

    total_count = len(user['characters'])
    keyboard = [[InlineKeyboardButton(f"See Collection ({total_count})", switch_inline_query_current_chat=f"collection.{user_id}")]]
    
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"harem:{page-1}:{user_id}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"harem:{page+1}:{user_id}"))
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if 'favorites' in user and user['favorites']:
        fav_character_id = user['favorites'][0]
        fav_character = next((c for c in user['characters'] if c['id'] == fav_character_id), None)

        if fav_character and 'img_url' in fav_character:
            if update.message:
                await update.message.reply_photo(photo=fav_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
            else:
                if update.callback_query.message.caption != harem_message:
                    await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
        else:
            await respond_with_message(update, harem_message, reply_markup)
    else:
        await respond_with_random_character(update, user, harem_message, reply_markup)

async def respond_with_message(update, message, reply_markup):
    if update.message:
        await update.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
    else:
        if update.callback_query.message.text != message:
            await update.callback_query.edit_message_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def respond_with_random_character(update, user, harem_message, reply_markup):
    if user['characters']:
        random_character = random.choice(user['characters'])
        if 'img_url' in random_character:
            if update.message:
                await update.message.reply_photo(photo=random_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
            else:
                if update.callback_query.message.caption != harem_message:
                    await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup)
        else:
            await respond_with_message(update, harem_message, reply_markup)
    else:
        await update.message.reply_text("Your List is Empty :)")

async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    _, page, user_id = query.data.split(':')
    page = int(page)
    user_id = int(user_id)

    if query.from_user.id != user_id:
        await query.answer("its Not Your Harem", show_alert=True)
        return

    await harem(update, context, page)

application.add_handler(CommandHandler("harem", harem, block=False))
application.add_handler(CallbackQueryHandler(harem_callback, pattern='^harem', block=False))