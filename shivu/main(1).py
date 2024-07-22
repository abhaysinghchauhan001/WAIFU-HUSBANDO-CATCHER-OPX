import importlib
import time
import random
import re
import asyncio
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

from shivu import (
    collection,
    top_global_groups_collection,
    group_user_totals_collection,
    user_collection,
    user_totals_collection,
    shivuu,
    application,
    LOGGER,
)
from shivu.modules import ALL_MODULES

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}

# Runway timing in seconds
RUNWAY_TIME = 120

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("shivu.modules." + module_name)

last_user = {}
warned_users = {}

def escape_markdown(text):
    escape_chars = r'\*_\\~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id

    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        chat_frequency = await user_totals_collection.find_one({'chat_id': chat_id})
        if chat_frequency:
            message_frequency = chat_frequency.get('message_frequency', 100)
        else:
            message_frequency = 100

        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id in warned_users and time.time() - warned_users[user_id] < 600:
                    return
                else:
                    await update.message.reply_text(
                        f"⚠️ 𝘿𝙤𝙣'𝙩 𝙎𝙥𝙖𝙢 {update.effective_user.first_name}...\n𝙔𝙤𝙪𝙧 𝙈𝙚𝙨𝙨𝙖𝙜𝙚𝙨 𝙒𝙞𝙡𝙡 𝙗𝙚 𝙞𝙜𝙣𝙤𝙧𝙚𝙙 𝙛𝙤𝙧 10 𝙈𝙞𝙣𝙪𝙩𝙚𝙨..."
                    )
                    warned_users[user_id] = time.time()
                    return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        if chat_id in message_counts:
            message_counts[chat_id] += 1
        else:
            message_counts[chat_id] = 1

        if message_counts[chat_id] % message_frequency == 0:
            await send_image(update, context)
            message_counts[chat_id] = 0

async def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    all_characters = list(await collection.find({}).to_list(length=None))

    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    character = random.choice(
        [c for c in all_characters if c['id'] not in sent_characters[chat_id]]
    )

    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character

    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"""***{character['rarity'][0]} ʟᴏᴏᴋ ᴀ ʜᴜsʙᴀɴᴅᴏ ʜᴀs ꜱᴘᴀᴡɴᴇᴅ !! ᴍᴀᴋᴇ ʜɪᴍ ʏᴏᴜʀ'ꜱ ʙʏ ɢɪᴠɪɴɢ 
 /grab 𝙷𝚞𝚜𝚋𝚊𝚗𝚍𝚘 𝚗𝚊𝚖𝚎***""",
        parse_mode='Markdown'
    )

    # Schedule runway message if no one grabs
    await asyncio.sleep(RUNWAY_TIME)
    if chat_id in last_characters and last_characters[chat_id] == character:
        await send_runway_message(context, chat_id, character)

async def send_runway_message(context: CallbackContext, chat_id: int, character: dict) -> None:
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"This character is in runway! Wait for the new one.",

reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{character['name']} [More Info]", callback_data=f"info_{character['id']}")]
        ])
    )
    del last_characters[chat_id]  # Reset the last character for the chat

async def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in last_characters:
        return

    if chat_id in first_correct_guesses:
        await update.message.reply_text(f'❌ 𝘼𝙡𝙧𝙚𝙖𝙙𝙮 𝘽𝙚𝙘𝙤𝙢𝙚 𝙎𝙤𝙢𝙚𝙤𝙣𝙚 𝙃𝙪𝙨𝙗𝙖𝙣𝙙𝙤..')
        return

    guess = ' '.join(context.args).lower() if context.args else ''

    if "()" in guess or "&" in guess.lower():
        await update.message.reply_text("𝙉𝙖𝙝𝙝 𝙔𝙤𝙪 𝘾𝙖𝙣'𝙩 𝙪𝙨𝙚 𝙏𝙝𝙞𝙨 𝙏𝙮𝙥𝙚𝙨 𝙤𝙛 𝙬𝙤𝙧𝙙𝙨 ❌️")
        return

    name_parts = last_characters[chat_id]['name'].lower().split()

    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id

        user = await user_collection.find_one({'id': user_id})
        if user:
            update_fields = {}
            if hasattr(update.effective_user, 'username') and update.effective_user.username != user.get('username'):
                update_fields['username'] = update.effective_user.username
            if update.effective_user.first_name != user.get('first_name'):
                update_fields['first_name'] = update.effective_user.first_name
            if update_fields:
                await user_collection.update_one({'id': user_id}, {'$set': update_fields})

            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
        elif hasattr(update.effective_user, 'username'):
            await user_collection.insert_one({
                'id': user_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'characters': [last_characters[chat_id]],
            })

        group_user_total = await group_user_totals_collection.find_one({'user_id': user_id, 'group_id': chat_id})
        if group_user_total:
            update_fields = {}
            if hasattr(update.effective_user, 'username') and update.effective_user.username != group_user_total.get('username'):
                update_fields['username'] = update.effective_user.username
            if update.effective_user.first_name != group_user_total.get('first_name'):
                update_fields['first_name'] = update.effective_user.first_name
            if update_fields:
                await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$set': update_fields})

            await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$inc': {'count': 1}})
        else:
            await group_user_totals_collection.insert_one({
                'user_id': user_id,
                'group_id': chat_id,
                'username': update.effective_user.username if hasattr(update.effective_user, 'username') else None,
                'first_name': update.effective_user.first_name,
                'count': 1,
            })

        await user_totals_collection.update_one({'id': user_id}, {'$inc': {'count': 1}}, upsert=True)

        await top_global_groups_collection.update_one({'group_id': chat_id}, {'$inc': {'count': 1}}, upsert=True)

        await update.message.reply_text(
            f"ᴡᴀᴏ🤯..!! {escape_markdown(update.effective_user.first_name)} {last_characters[chat_id]['name']}"
            f" ᴄᴏɴɢʀᴀᴛꜱ ʏᴏᴜ ʜᴀᴠᴇ ᴀ ʜᴜꜱʙᴀɴᴅᴏ ❤️❤️...",
            parse_mode='Markdown'
        )
        del last_characters[chat_id]
    else:
        await update.message.reply_text(f"𝙄 𝘿𝙤𝙣'𝙩 𝙆𝙣𝙤𝙬 𝙒𝙝𝙤 𝙏𝙝𝙞𝙨 𝙄𝙨 𝙋𝙡𝙨𝙨 𝙏𝙧𝙮 𝘼𝙜𝙖𝙞𝙣 {escape_markdown(update.effective_user.first_name)}...!", parse_mode='Markdown')

async def character_info(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    character_id = query.data.split('_')[1]

    character = await collection.find_one({'id': int(character_id)})

    if character:
        await query.answer()
        await query.edit_message_text(
            text=f"""Character Info:

Name: {character['name']}
Rarity: {character['rarity']}
Category: {character['category']}
Description: {character['description']}""",
            parse_mode='Markdown'
        )
    else:
        await query.answer("Character not found!")

application.add_handler(CommandHandler("grab", guess))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_counter))
application.add_handler(CallbackQueryHandler(character_info, pattern=r"info_\d+"))

LOGGER.info("Loaded Husbando Finder module")