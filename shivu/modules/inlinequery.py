from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
from pyrogram import Client, filters, types, enums
import asyncio
import time
from html import escape
from cachetools import TTLCache
from pymongo import MongoClient, ASCENDING
from shivu import shivuu as app
from shivu import user_collection, collection, db

# --- Constants for Event Categories ---
EVENT_EMOJIS = ["👘", "☔", "🎄", "☃️", "🥻", "💖", "🏖️"]
EVENT_NAMES = ["KIMONO", "MONSOON", "CHRISTMAS", "WINTER", "SAREE", "VALENTINE", "SUMMER"]

# --- MongoDB indexes ---
db.characters.create_index([('id', ASCENDING)])
db.characters.create_index([('anime', ASCENDING)])
db.characters.create_index([('img_url', ASCENDING)])

db.user_collection.create_index([('characters.id', ASCENDING)])
db.user_collection.create_index([('characters.name', ASCENDING)])
db.user_collection.create_index([('characters.img_url', ASCENDING)])

# --- Caching for performance ---
all_characters_cache = TTLCache(maxsize=10000, ttl=36000)
user_collection_cache = TTLCache(maxsize=10000, ttl=60)

@app.on_inline_query()
async def inlinequery(client: Client, query: types.InlineQuery):
    offset = int(query.offset) if query.offset else 0

    # --- Determine search scope (global or user collection) ---
    if query.query.startswith('collection.'):
        user_id, *search_terms = query.query.split(' ')[0].split('.')[1], ' '.join(query.query.split(' ')[1:])
        try:
            user_id = int(user_id)
            user = user_collection_cache.get(user_id) or await user_collection.find_one({'id': user_id})
            user_collection_cache[user_id] = user

            if user:
                all_characters = list({v['id']: v for v in user['characters']}.values())
                if search_terms:
                    regex = re.compile(' '.join(search_terms), re.IGNORECASE)
                    all_characters = [char for char in all_characters if any(regex.search(str(char.get(field, ''))) for field in ['name', 'rarity', 'id', 'anime'])]
            else:
                all_characters = []
        except ValueError:
            all_characters = []
    else:
        # --- Global character search ---
        if query.query:
            regex = re.compile(query.query, re.IGNORECASE)
            all_characters = list(await collection.find({"$or": [
                {"name": regex}, {"rarity": regex}, {"id": regex}, {"anime": regex}
            ]}).to_list(length=None))
        else:
            all_characters = all_characters_cache.get('all_characters') or list(await collection.find({}).to_list(length=None))
            all_characters_cache['all_characters'] = all_characters

    # --- Pagination for results ---
    characters = all_characters[offset:offset + 50]
    next_offset = str(offset + 50) if len(all_characters) > offset + 50 else None

    results = []
    for character in characters:
        global_count = await user_collection.count_documents({'characters.id': character['id']})
        anime_characters = await collection.count_documents({'anime': character['anime']})
        total_characters = len(all_characters)

        # --- Determine event (if any) and format event details ---
        event_details = ""
        for i, event_emoji in enumerate(EVENT_EMOJIS):
            if event_emoji in character.get("event", ""):  # Check if the emoji is in the character's "event" field
                event_details = f" **•** __{EVENT_NAMES[i]} EVENT__"
                break  # Stop checking after finding the first event

        # --- Customized result display for user collections ---
        if query.query.startswith('collection.'):
            user_character_count = sum(c['id'] == character['id'] for c in user['characters'])
            user_anime_characters = sum(c['anime'] == character['anime'] for c in user['characters'])
                        caption = f"<b> Lᴏᴏᴋ Aᴛ <a href='tg://user?id={user['id']}'>{(escape(user.get('first_name', user['id'])))}</a>'s wᴀɪғᴜ....!!</b>\n\n <b>{character['id']}:</b> {character['name']} x{user_character_count}\n<b>{character['anime']}</b> {user_anime_characters}/{anime_characters}\n﹙<b>{character['rarity'][0]} 𝙍𝘼𝙍𝙄𝙏𝙔:</b> {character['rarity'][2:]}﹚\n\n{event_details}\n\n"  # Add event details here
            )
            # ... rest of your code ... 
        else:
            caption = f"<b>Lᴏᴏᴋ Aᴛ Tʜɪs wᴀɪғᴜ....!!</b>\n\n<b>{character['id']}:</b> {character['name']}\n <b>{character['anime']}</b>\n﹙<b>{character['rarity'][0]} 𝙍𝘼𝙍𝙄𝙏𝙔:</b> {character['rarity'][2:]}﹚\n\n{event_details}\n\n<b>Gʟᴏʙᴀʟʟʏ Gʀᴀʙ {global_count} Times...</b>"
        results.append(
            InlineQueryResultPhoto(
                thumbnail_url=character['img_url'],
                id=f"{character['id']}_{time.time()}",
                photo_url=character['img_url'],
                caption=caption,
                parse_mode='HTML'
            )
        )

    await update.inline_query.answer(results, next_offset=next_offset, cache_time=5)

application.add_handler(InlineQueryHandler(inlinequery, block=False))