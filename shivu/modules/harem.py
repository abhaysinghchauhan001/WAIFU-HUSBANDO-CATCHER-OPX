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
        await update.message.reply_text("You need to register first by starting the bot in DM.")
        return
    
    characters = user.get('characters', [])
    hmode = user.get('smode')
    
    # Filter characters based on harem mode
    rarity_value = "all" if hmode in ["default", None] else harem_mode_mapping.get(hmode)
    characters = [char for char in characters if isinstance(char, dict) and (hmode == "default" or char.get('rarity') == rarity_value)]
    
    if not characters:
        await update.message.reply_text("No characters available for the selected rarity.")
        return
    
    total_pages = math.ceil(len(characters) / 10)
    page = max(0, min(page, total_pages - 1))
    
    current_characters = characters[page * 10:(page + 1) * 10]
    harem_message = f"<b>{escape(update.effective_user.first_name)}'s Harem - Page {page + 1}/{total_pages}</b>\n"
    
    for character in current_characters:
        harem_message += f"<b>{character['name']}</b> [Rarity: {character['rarity']}]\n"
    
    keyboard = [[InlineKeyboardButton("💠 Inline 💠", switch_inline_query_current_chat=f"collection.{user_id}")]]
    
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⤂", callback_data=f"harem:{page - 1}:{user_id}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("⤃", callback_data=f"harem:{page + 1}:{user_id}"))
        keyboard.append(nav_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(harem_message, reply_markup=reply_markup, parse_mode='HTML')

async def set_hmode(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ", callback_data="default"),
            InlineKeyboardButton("ʀᴀʀɪᴛʏ", callback_data="rarity"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose a harem mode:", reply_markup=reply_markup)

async def hmode_rarity(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("🟢 Common", callback_data="common"),
            InlineKeyboardButton("🟣 Rare", callback_data="rare"),
        ],
        [
            InlineKeyboardButton("🟡 Legendary", callback_data="legendary"),
            InlineKeyboardButton("💮 Special Edition", callback_data="spacial_edition"),
        ],
        [
            InlineKeyboardButton("🔮 Premium Edition", callback_data="premium_edition"),
            InlineKeyboardButton("🎗️ Supreme", callback_data="supreme"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query

    await query.edit_message_caption(
        caption="Choose a rarity:",
        reply_markup=reply_markup,
    )
    await query.answer()

async def rarity_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    rarity = query.data
    user_id = query.from_user.id
    
    await user_collection.update_one({'id': user_id}, {'$set': {'smode': rarity}})
    
    await query.answer(f"Rarity mode set to {rarity}.")
    await harem(update, context, 0, edit=True)  # Reset to page 0 after changing rarity

# Handlers registration (to be placed in your main application file)

def register_handlers(application):
    application.add_handler(CommandHandler("harem", harem))
    application.add_handler(CommandHandler("hmode", set_hmode))
    application.add_handler(CallbackQueryHandler(harem_callback, pattern=r'harem:\d+:\d+'))
    application.add_handler(CallbackQueryHandler(handle_hmode_selection, pattern='^default$|^rarity$'))
    application.add_handler(CallbackQueryHandler(rarity_callback, pattern='^common$|^rare$|^legendary$|^spacial_edition$|^premium_edition$|^supreme$'))