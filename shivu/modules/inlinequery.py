import re
import time
from html import escape
from cachetools import TTLCache
from pymongo import MongoClient, ASCENDING

from telegram import Update, InlineQueryResultPhoto
from telegram.ext import InlineQueryHandler, CallbackContext, CommandHandler 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from shivu import user_collection, collection, application, db


# collection
db.characters.create_index([('id', ASCENDING)])
db.characters.create_index([('anime', ASCENDING)])
db.characters.create_index([('img_url', ASCENDING)])
db.characters.create_index([('catagory', ASCENDING)])

# user_collection
db.user_collection.create_index([('characters.id', ASCENDING)])
db.user_collection.create_index([('characters.name', ASCENDING)])
db.user_collection.create_index([('characters.img_url', ASCENDING)])
db.user_collection.create_index([('characters.catagory', ASCENDING)])

all_characters_cache = TTLCache(maxsize=10000, ttl=36000)
user_collection_cache = TTLCache(maxsize=10000, ttl=60)

async def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0

    if query.startswith('collection.'):
        user_id, *search_terms = query.split(' ')[0].split('.')[1], ' '.join(query.split(' ')[1:])
        if user_id.isdigit():
            if user_id in user_collection_cache:
                user = user_collection_cache[user_id]
            else:
                user = await user_collection.find_one({'id': int(user_id)})
                user_collection_cache[user_id] = user

            if user:
                all_characters = list({v['id']:v for v in user['characters']}.values())
                if search_terms:
                    regex = re.compile(' '.join(search_terms), re.IGNORECASE)
                    all_characters = [character for character in all_characters if regex.search(character['name']) or regex.search(character['anime'])]
            else:
                all_characters = []
        else:
            all_characters = []
    else:
        if query:
            regex = re.compile(query, re.IGNORECASE)
            all_characters = list(await collection.find({"$or": [{"name": regex}, {"anime": regex}]}).to_list(length=None))
        else:
            if 'all_characters' in all_characters_cache:
                all_characters = all_characters_cache['all_characters']
            else:
                all_characters = list(await collection.find({}).to_list(length=None))
                all_characters_cache['all_characters'] = all_characters

    characters = all_characters[offset:offset+50]
    if len(characters) > 50:
        characters = characters[:50]
        next_offset = str(offset + 50)
    else:
        next_offset = str(offset + len(characters))

    results = []
    for character in characters:
        global_count = await user_collection.count_documents({'characters.id': character['id']})
        anime_characters = await collection.count_documents({'anime': character['anime']})

        if query.startswith('collection.'):
            user_character_count = sum(c['id'] == character['id'] for c in user['characters'])
            user_anime_characters = sum(c['anime'] == character['anime'] for c in user['characters'])
            caption = f"<b> Lᴏᴏᴋ Aᴛ <a href='tg://user?id={user['id']}'>{(escape(user.get('first_name', user['id'])))}</a>'s Character</b>\n\n <b>{character['id']}</b>:{character['name']} x{user_character_count}\n<b>{character['anime']}</b> {user_anime_characters}/{anime_characters}\n﹙{character['rarity'][0]}<b>𝙍𝘼𝙍𝙄𝙏𝙔:</b>{character['rarity'][2:]}﹚\n\n"

    

        
emojis = {
    "beach": "🏖️",
    "kimono": "👘",
    "umbrella": "☔",
    "maid": "☕",
    "valentine": "❤️",
    "star": "⭐" 
}

events = {
    "Sammer": {
        "emoji": emojis["beach"],
        "description": "Find the refreshment under the sun!",
    },
    "Jujutsu Kaisen": {
        "emoji": emojis["kimono"],
        "description": "A mystical adventure filled with thrills!",
    },
    "Coffee Break": { 
        "emoji": emojis["cup"], 
        "description": "Take a break and enjoy a cup of coffee!",
    }
}

# ... (rest of your code)

else:
    # Assuming 'character' now has an 'event' key, e.g., character['event'] = "Sammer"
    event_name = character.get('event') 
    event_info = events.get(event_name, {}) # Get event details, use empty dict if not found

    caption = (
        f"<b>Lᴏᴏᴋ Aᴛ Tʜɪs Wᴀɪғᴜ....!!</b>\n\n"
        f"<b>{character['id']}:</b> {character['name']}\n"
        f"<b>{character['anime']}</b>\n"
        f"﹙<b>{character['rarity'][0]} 𝙍𝘼𝙍𝙄𝙏𝙔:</b> {character['rarity'][2:]}﹚\n\n"
        f"{event_info.get('emoji', '')}{event_name}{event_info.get('emoji', '')}" # Event info 
        f"<b>Gʟᴏʙᴀʟʟʏ Gʀᴀʙ {global_count} Times...</b>\n\n"
        f"✳️ 𝖧𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 𝗅𝗂𝗌𝗍 𝗈𝖿 𝗎𝗌𝖾𝗋𝗌 𝗐𝗁𝗈 𝗁𝖺𝗏𝖾 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗋𝖺𝖼𝗍𝖾𝗋\n"
    )

    results.append(
        types.InlineQueryResultPhoto(
            title=title,
            thumb_url=character['img_url'],
            photo_url=character['img_url'],
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )
    )

    await update.inline_query.answer(results, next_offset=next_offset, cache_time=5)

application.add_handler(InlineQueryHandler(inlinequery, block=False))
