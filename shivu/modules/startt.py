import random
import logging
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Application

from shivu import PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, BOT_NAME, db, GROUP_ID, Application 

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Database collection for user data
collection = db['total_pm_users']

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username or "N/A"

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=GROUP_ID, text=f"🎋 <b>ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ</b>\n\n"
               f"💠 <b>ᴜsᴇʀ ɪᴅ:</b> {user_id}\n"
               f"🔰 <b>ғɪʀsᴛ ɴᴀᴍᴇ:</b> {first_name}\n"
               f"🏷️ <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{username}", parse_mode='HTML')

    await update.message.reply_text(f"Welcome {first_name}!")

    caption = f"""
    ***ʜᴇʟʟᴏ....💫  {escape(first_name)}***

    ***ᴡʜᴏ ᴀᴍ ɪ - ɪ'ᴍ*** {BOT_NAME}

    ***◈ ━━━━━━━━ ● ━━━━━━━━ ◈***

    ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ...✨️ ᴀɴᴅ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀғᴛᴇʀ.. ᴇᴠᴇʀʏ 𝟷𝟶𝟶 ᴍᴇssᴀɢᴇs ɪɴ ɢʀᴏᴜᴘ.

    ──────────────────
    ✧ COMMAND - ᴜsᴇ /ɢʀᴀʙ ᴛᴏ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀɴᴅ sᴇᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ʙʏ ᴜsɪɴɢ /ʜᴀʀᴇᴍ...✨️

    ◈ ━━━━━━━━ ● ━━━━━━━━ ◈***
    """

    keyboard = [
        [InlineKeyboardButton("✤ ᴀᴅᴅ ᴍᴇ ✤", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
        [InlineKeyboardButton("☊ 𝗌ᴜᴘᴘᴏʀᴛ ☊", url=f'https://t.me/{SUPPORT_CHAT}'),
         InlineKeyboardButton("✠ ᴜᴘᴅᴀᴛᴇ𝗌 ✠", url=f'https://t.me/{UPDATE_CHAT}')],
        [InlineKeyboardButton("✇ ʜᴇʟᴘ ✇", callback_data='help'),
         InlineKeyboardButton("≎ ᴄʀᴇᴅɪᴛ ≎", url=f'https://t.me/{UPDATE_CHAT}')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_url = random.choice(PHOTO_URL)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
        ***Help Section :***

        **/grab** - to grab a character (only works in group)  
        **/fav** - add your favorite  
        **/trade** - to trade character  
        **/gift** - give any character from your collection  
        **/harem** - to see your harem  
        **/top** - to see top users  
        **/changetime** - change character appearance time  
        """ 
        help_keyboard = [[InlineKeyboardButton("⤂ʙᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':
        first_name = escape(query.from_user.first_name)  
        caption = f"""
        ***ʜᴇʟʟᴏ....💫  {first_name}***

        ***ᴡʜᴏ ᴀᴍ ɪ - ɪ'ᴍ*** [{BOT_NAME}](https://t.me/{BOT_USERNAME})***

        ***◈ ━━━━━━━━ ● ━━━━━━━━ ◈***

        ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ...✨️ ᴀɴᴅ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀғᴛᴇʀ.. ᴇᴠᴇʀʏ 𝟷𝟶𝟶 ᴍᴇssᴀɢᴇs ɪɴ ɢʀᴏᴜᴘ.

        ───────────────────
        ✧ COMMAND - ᴜsᴇ /ɢʀᴀʙ ᴛᴏ ᴄᴏʟʟᴇᴄᴛ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀɴᴅ sᴇᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ʙʏ ᴜsɪɴɢ /ʜᴀʀᴇᴍ...✨️

        ◈ ━━━━━━━━ ● ━━━━━━━━ ◈***
        """

        keyboard = [
            [InlineKeyboardButton("✤ ᴀᴅᴅ ᴍᴇ ✤", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("☊ 𝗌ᴜᴘᴘᴏʀᴛ ☊", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("✠ ᴜᴘᴅᴀᴛᴇ𝗌 ✠", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("✇ ʜᴇʟᴘ ✇", callback_data='help'),
             InlineKeyboardButton("≎ ᴄʀᴇᴅɪᴛ ≎", url=f'https://t.me/{UPDATE_CHAT}')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode='markdown'
        )

# Add command and callback query handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))