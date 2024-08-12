from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackContext, CommandHandler, CallbackQueryHandler, InlineQueryHandler, ChosenInlineResultHandler
import asyncio
from shivu import application
from telegram.ext import Updater, MessageHandler, Filters
from shivu import user_collection
from telegram.ext import CallbackContext
import collection

async def add_rarity(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_collection = context.user_data
    rarities = ["🟢 Common", "🟣 Rare", "🟡 Legendary", "💮 Special Edition", "🔮 Premium Edition", "🎗️ Supreme"]

    current_rarity = (await user_collection.get_data(user_id)).get("selected_rarity", "Default")

    keyboard = []
    for i in range(0, len(rarities), 2):
        row = [InlineKeyboardButton(f"{rarities[i].title()} {'✅️' if rarities[i] == current_rarity else ''}",
                                    callback_data=f"add_rarity:{rarities[i]}")]
        if i + 1 &lt; len(rarities):
            row.append(InlineKeyboardButton(f"{rarities[i + 1].title()} {'✅️' if rarities[i + 1] == current_rarity else ''}",
                                        callback_data=f"add_rarity:{rarities[i + 1]}")]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ ✅️" if current_rarity == "Default" else "ᴅᴇꜰᴀᴜʟᴛ",
                                    callback_data="add_rarity:Default")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select your desired Harem rarity:", reply_markup=reply_markup)

def add_rarity_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    user_collection = context.user_data

    rarity = data.split(":")[1]
    await user_collection.set_data(user_id, {"selected_rarity": rarity})

    await query.message.edit_caption(caption=f"ʏᴏᴜ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ʏᴏᴜʀ ʜᴀʀᴇᴍ ᴍᴏᴅᴇ ʀᴀʀɪᴛʏ ᴀꜱ {rarity}")

    rarities = ["🟢 Common", "🟣 Rare", "🟡 Legendary", "💮 Special Edition", "🔮 Premium Edition", "🎗️ Supreme"]
    keyboard = []
    for i in range(0, len(rarities), 2):
        row = [InlineKeyboardButton(f"{rarities[i].title()} {'✅️' if rarities[i] == rarity else ''}",
                                    callback_data=f"add_rarity:{rarities[i]}")]
        if i + 1 &lt; len(rarities):
            row.append(InlineKeyboardButton(f"{rarities[i + 1].title()} {'✅️' if rarities[i + 1] == rarity else ''}",
                                        callback_data=f"add_rarity:{rarities[i + 1]}")]
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("ᴅᴇꜰᴀᴜʟᴛ ✅️" if rarity == "Default" else "ᴅᴇꜰᴀᴜʟᴛ",
                                    callback_data="add_rarity:Default")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup=reply_markup)

application.add_handler(CommandHandler("hmode", add_rarity, pass_user_data=True))
add_rarity_handler = CallbackQueryHandler(add_rarity_callback, pass_user_data=True)
application.add_handler(add_rarity_handler)