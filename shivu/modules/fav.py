import asyncio
from pyrogram import filters, Client, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot
from shivu import user_collection, collection

# ... (your database setup and user_collection definition)


    """Set a character as favorite."""

    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text('𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙒𝘼𝙄𝙁𝙐 𝙞𝙙...')
        return

    character_id = context.args[0]
    user = await user_collection.find_one({'id': user_id})

    if not user:
        await update.message.reply_text('𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙣𝙤𝙩 𝙂𝙤𝙩 𝘼𝙣𝙮 𝙒𝘼𝙄𝙁𝙐 𝙮𝙚𝙩...')
        return

    character = next((c for c in user['characters'] if c['id'] == character_id), None)

    if not character:
        await update.message.reply_text('𝙏𝙝𝙞𝙨 𝙒𝘼𝙄𝙁𝙐 𝙞𝙨 𝙉𝙤𝙩 𝙄𝙣 𝙮𝙤𝙪𝙧 𝙒𝘼𝙄𝙁𝙐 𝙡𝙞𝙨𝙩')
        return

    # Prepare inline keyboard
    keyboard = [
        [InlineKeyboardButton("💖 Yes", callback_data=f"favorite_yes_{character_id}"), 
         InlineKeyboardButton("💔 No", callback_data=f"favorite_no_{character_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=character["img_url"], 
        caption=f'ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴍᴀᴋᴇ ᴛʜɪs ᴡᴀɪғᴜ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ?\n ↬ {character["name"]} ({character["anime"]})',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_favorite_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user's choice from the inline keyboard."""
    query = update.callback_query
    await query.answer() 

    choice, _, character_id = query.data.split("_")
    user_id = update.effective_user.id

    user = await user_collection.find_one({'id': user_id})

    if choice == "favoriteyes":
        user['favorites'] = [character_id] 
        await user_collection.update_one({'id': user_id}, {'$set': {'favorites': user['favorites']}})
        await query.edit_message_caption(
            caption=f"You made {character['name']} your favorite! 💖" 
        )
    else:
        await query.edit_message_caption(
            caption=f"No worries! Maybe another time. 😊"
        )

    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    application.add_handler(CommandHandler("setfavorite", set_favorite))
    application.add_handler(CallbackQueryHandler(handle_favorite_choice))

    application.run_polling()