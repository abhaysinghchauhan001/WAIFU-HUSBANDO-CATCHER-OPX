import importlib
import time
import random
import re
import asyncio
from html import escape
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from shivu import collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection, shivuu
from shivu import LOGGER
from shivu import shivuu as app 

locks = {}
message_counts = {}
warned_users = {}
last_user = {}
sent_characters = {}
first_correct_guesses = {}
last_characters = {}

# Import all modules
for module_name in ALL_MODULES:
    importlib.import_module("shivu.modules." + module_name)


def escape_markdown(text):
    escape_chars = r'\\\*\_\`\\\\\~&gt;#+-=|{}.!'
    return re.sub(r'(\[%s\])' % re.escape(escape_chars), r'\\\\\\1', text)


async def get_random_character(chat_id):
    rarity_weights = {
        "🟢 Common": 50,
        "🟣 Rare": 30,
        "🟡 Legendary": 20,
        "💮 Special Edition": 5,
        "🔮 Premium Edition": 2,
        "🎗️ Supreme": 1
    }

    characters = await collection.find({}).to_list(length=None)

    weighted_characters = [
        character for character in characters
        for _ in range(rarity_weights.get(character['rarity'], 0))
    ]

    selected_character = random.choice(weighted_characters)

    if selected_character['rarity'] == "🎗️ Supreme":
        if chat_id != -1003782282782:  # Replace with your chat ID
            return None

    return selected_character


@app.on_message(filters.text)
async def message_counter(client, message):
    chat_id = str(message.chat.id)
    user_id = message.from_user.id

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
                    await message.reply_text(f"**ᴅᴏɴ'ᴛ 𝗌ᴘᴀᴍ** {escape(message.from_user.first_name)}... \n**ʏᴏᴜʀ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ɪɢɴᴏʀᴇᴅ ғᴏʀ 10 ᴍɪɴᴜᴛᴇs...!!**")
                    warned_users[user_id] = time.time()
                    return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        if chat_id in message_counts:
            message_counts[chat_id] += 1
        else:
            message_counts[chat_id] = 1

        if message_counts[chat_id] % message_frequency == 0:
            await send_image(message)
            message_counts[chat_id] = 0


async def send_image(message):
    chat_id = message.chat.id
    all_characters = list(await collection.find({}).to_list(length=None))

    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])
    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character

    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    await app.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"**{character['rarity'][0]} ʟᴏᴏᴋ ᴀ ʜᴜsʙᴀɴᴅᴏ ʜᴀꜱ ꜱᴘᴀᴡɴᴇᴅ !! ᴍᴀᴋᴇ ʜɪᴍ ʏᴏᴜʀ'ꜱ ʙʏ ɢɪᴠɪɴɢ /grab 𝙷𝚞𝚜𝚋𝚊𝚗𝚍𝚘 𝚗𝚊𝚖𝚎**",
        parse_mode='markdown'
    )


@app.on_message(filters.command("grab"))
async def guess(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in last_characters:
        return

    if chat_id in first_correct_guesses:
        await message.reply_text("🚫 **ʜᴜsʙᴀɴᴅᴏᴜ ᴀʟʀᴇᴀᴅʏ ɢʀᴀʙʙᴇᴅ ʙʏ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ ⚡. ʙᴇᴛᴛᴇʀ ʟᴜᴄᴋ ɴᴇxᴛ ᴛɪᴍᴇ..!!**")
        return

    guess = ' '.join(message.command[1:]).lower() if message.command[1:] else ''

    if "()" in guess or "&" in guess.lower():
        await message.reply_text("**ɴᴀʜʜ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴛʏᴘᴇs ᴏғ ᴡᴏʀᴅs...❌**")
        return

    name_parts = last_characters[chat_id]['name'].lower().split()

    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id

        user = await user_collection.find_one({'id': user_id})
        if user:
            update_fields = {}
            if hasattr(message.from_user, 'username') and message.from_user.username != user.get('username'):
                update_fields['username'] = message.from_user.username
            if message.from_user.first_name != user.get('first_name'):
                update_fields['first_name'] = message.from_user.first_name
            if update_fields:
                await user_collection.update_one({'id': user_id}, {'$set': update_fields})
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
        else:
            await user_collection.insert_one({
                'id': user_id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'characters': [last_characters[chat_id]],
            })

        await update_group_user_totals(user_id, chat_id, message)

        keyboard = [[InlineKeyboardButton("🪼 ʜᴀʀᴇᴍ", switch_inline_query_current_chat=f"collection.{user_id}")]]
        await message.reply_text(f'Congratulations 🎊\n**{escape(message.from_user.first_name)} You grabbed a new Husbando!! ✅️**\n\n✨ 𝙉𝙖𝙢𝙚: <code>{last_characters[chat_id]["name"]}</code>\n{last_characters[chat_id]["rarity"][0]} 𝙍𝙖𝙧𝙞𝙩𝙮: <code>{last_characters[chat_id]["rarity"][2:]}</code>\n⚡ 𝘼𝙣𝙞𝙢𝙚: <code>{last_characters[chat_id]["anime"]}</code>\n\n✧ Character successfully added in your /hharem', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text("**ᴘʟᴇᴀsᴇ ᴡʀɪᴛᴇ ᴀ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ..❌**")


@app.on_message(filters.command("hfav"))
async def fav(client, message):
    user_id = message.from_user.id
    if not message.command[1:]:
        await message.reply_text("**ᴘʀᴏᴠɪᴅᴇ ᴀ ʜᴜsʙᴀɴᴅᴏ ɪᴅ....!!**")
        return

    character_id = message.command[1]
    user = await user_collection.find_one({'id': user_id})

    if not user:
        await message.reply_text("**ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ ɢᴏᴛ ᴀɴʏ ʜᴜsʙᴀɴᴅᴏ ʏᴇᴛ..!**")
        return

    character = next((c for c in user['characters'] if c['id'] == character_id), None)

    if not character:
        await message.reply_text("**ᴛʜɪs ʜᴜsʙᴀɴᴅᴏ ɪs ɴᴏᴛ ɪɴ ʏᴏᴜʀ ʜᴀʀᴇᴍ ʟɪsᴛ**")
        return

    buttons = [
        [InlineKeyboardButton("🟢 Yes", callback_data=f"yes_{character_id}"),
         InlineKeyboardButton("🔴 No", callback_data=f"no_{character_id}")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await app.send_photo(
        chat_id=chat_id,
        photo=character["img_url"],
        caption=f"**ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴍᴀᴋᴇ ᴛʜɪs ʜᴜsʙᴀɴᴅᴏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ..! \n↬ <code>{character['name']}</code> (<code>{character['anime']}</code>)**",
        reply_markup=reply_markup
    )


@app.on_callback_query(filters.regex('^yes_'))
async def handle_yes(client, query):
    await query.answer()
    user_id = query.from_user.id
    character_id = query.data.split('_')[1]

    try:
        result = await user_collection.update_one(
            {'id': user_id},
            {'$set': {'favorites': [character_id]}}
        )

        if result.matched_count > 0:
            await query.edit_message_caption(
                caption="**ʜᴜsʙᴀɴᴅᴏ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴀs ᴀ ғᴀᴠᴏʀɪᴛᴇ!**"
            )
        else:
            await query.edit_message_caption(
                caption="**ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ᴜsᴇʀ' s ғᴀᴠᴏʀɪᴛᴇ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.**"
            )

    except Exception as e:
        await query.edit_message_caption(
            caption=f"**ᴇʀʀᴏʀ: {str(e)}**"
        )


@app.on_callback_query(filters.regex('^no_'))
async def handle_no(client, query):
    await query.answer(text="Okay, no worries!")  # Optional message
    await query.edit_message_caption(caption="**ᴄᴀɴᴄᴇʟᴇᴅ.**")


async def update_group_user_totals(user_id, chat_id, message):
    group_user_total = await group_user_totals_collection.find_one({'user_id': user_id, 'group_id': chat_id})
    if group_user_total:
        update_fields = {}
        if hasattr(message.from_user, 'username') and message.from_user.username != group_user_total.get('username'):
            update_fields['username'] = message.from_user.username
        if message.from_user.first_name != group_user_total.get('first_name'):
            update_fields['first_name'] = message.from_user.first_name
        if update_fields:
            await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$set': update_fields})
        await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$inc': {'count': 1}})
    else:
        await group_user_totals_collection.insert_one({
            'user_id': user_id,
            'group_id': chat_id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'count': 1,
        })


def main():
    app.run()


if __name__ == "__main__":
    shivuu.start()
    LOGGER.info("Bot started")
    main()