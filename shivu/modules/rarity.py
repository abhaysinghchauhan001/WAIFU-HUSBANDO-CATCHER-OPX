from telegram import Update
from itertools import groupby
import urllib.request
import re
import math
import html
import random
from collections import Counter
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
from shivu import collection, user_collection, application
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto, InputTextMessageContent, InputMediaPhoto
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
from telegram.ext import InlineQueryHandler, CallbackQueryHandler, ChosenInlineResultHandler




async def add_rarity(update: Update, context: CallbackContext) -> None:
    """Handles the "/hmode" command to allow users to choose a rarity for their harem."""
    user_id = update.effective_user.id
    user_collection = update.effective_user.get_collection("user_data")
    rarities = ["🟢 Common", "🟣 Rare", "🟡 Legendary", "💮 Special Edition", "🔮 Premium Edition", "🎗️ Supreme"]

    # Get current rarity from the user's collection
    current_rarity = await user_collection.find_one({"id": user_id}, {"selected_rarity": 1})
    current_rarity = current_rarity.get("selected_rarity") if current_rarity else "Default"

    keyboard = []
    for i in range(0, len(rarities), 2):
        row = [InlineKeyboardButton(f"{rarities[i].title()} {'✅️' if rarities[i] == current_rarity else ''}",
                                    callback_data=f"add_rarity:{rarities[i]}")]
        if i + 1 < len(rarities):
            row.append(InlineKeyboardButton(f"{rarities[i + 1].title()} {'✅️' if rarities[i + 1] == current_rarity else ''}",
                                        callback_data=f"add_rarity:{rarities[i + 1]}"))
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ ✅️" if current_rarity == "Default" else "ᴅᴇꜰᴀᴜʟᴛ",
                                    callback_data="add_rarity:Default")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the keyboard with the user's current rarity highlighted
    await update.message.reply_text("Select your desired Harem rarity:", reply_markup=reply_markup)


async def add_rarity_callback(update: Update, context: CallbackContext) -> None:
    """Handles callbacks from the rarity selection keyboard."""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    user_collection = update.effective_user.get_collection("user_data")

    if data == "add_rarity:Default":
        await user_collection.update_one({'id': user_id}, {'$set': {'selected_rarity': 'Default'}})
        await query.message.edit_caption(caption="ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ᴀꜱ ᴅᴇꜰᴀᴜʟᴛ")
    else:
        rarity = data.split(":")[1]
        await user_collection.update_one({'id': user_id}, {'$set': {'selected_rarity': rarity}})
        await query.message.edit_caption(caption=f"ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ʀᴀʀɪᴛʏ ᴀꜱ {rarity}")

    # Update the rarity selection buttons with the new selection highlighted
    rarities = ["🟢 Common", "🟣 Rare", "🟡 Legendary", "💮 Special Edition", "🔮 Premium Edition", "🎗️ Supreme"]
    keyboard = []
    for i in range(0, len(rarities), 2):
        row = [InlineKeyboardButton(f"{rarities[i].title()} {'✅️' if rarities[i] == rarity else ''}",
                                    callback_data=f"add_rarity:{rarities[i]}")]
        if i + 1 < len(rarities):
            row.append(InlineKeyboardButton(f"{rarities[i + 1].title()} {'✅️' if rarities[i + 1] == rarity else ''}",
                                        callback_data=f"add_rarity:{rarities[i + 1]}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ ✅️" if rarity == "Default" else "ᴅᴇꜰᴀᴜʟᴛ",
                                    callback_data="add_rarity:Default")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)


# ... rest of your code ...

application.add_handler(CommandHandler("hmode", add_rarity, block=False))
add_rarity_handler = CallbackQueryHandler(add_rarity_callback, pattern='^add_rarity', block=False)
application.add_handler(add_rarity_handler)