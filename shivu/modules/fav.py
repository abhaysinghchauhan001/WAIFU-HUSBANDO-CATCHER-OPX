from telegram import Update
from itertools import groupby
import math
from html import escape 
import random

from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from shivu import collection, user_collection, application

def main() -> None:
    application = asyncio.run(
        setup_application().extra_types[0]
    )

async def setup_application() -> CommandObject:
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    application.add_handler(CommandHandler("fav", fav, block=False))

    return application

async def find_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[int]:
    user_id = update.effective_user.id
    return user_id

async def find_user(user_id: int):
    user = await user_collection.find_one({ "id": user_id })
    return user

async def find_favorite(user: dict, character_id: str):
    character = next((c for c in user["characters"] if c["id"] == character_id), None)
    return character

async def fav(update: Update, context: CallbackContext) -> None:
    user_id = await find_user_id(update, context)

    if not context.args:
        await update.message.reply_text('Please enter waifu ID.')
        return

    character_id = context.args[0]

    user = await find_user(user_id)
    if not user:
        await update.message.reply_text("You are not registered yet!")
        return

    character = await find_favorite(user, character_id)

    if not character:
        await update.message.reply_text('Character not found.')
        return

    user["favorites"] = [character_id]

    user = await user_collection.find_one({"id": user_id})
    if "-1" not in user["favorites"]:
        user["favorites"].append("-1")
        await user_collection.update_one({"id": user_id}, {'$set': {"favorites": user["favorites"]}})

    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"fav_yes_{character_id}"),
            InlineKeyboardButton("❌ No", callback_data=f"fav_no_{character_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo( photo=character["img_url"], caption=f'Do you want to make this waifu your favourite ?\n ↬ {character["name"]} ({character["anime"]})', parse_mode="Markdownv2", reply_markup=reply_markup )

async def button_answer(update, context) -> None:
    query = update.callback_query

    if query and query.data:
        callback_data = query.data
        split_callback = callback_data.split("_")