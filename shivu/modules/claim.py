import asyncio
from pyrogram import filters, Client, types as t
from shivu import shivuu as bot
from shivu import user_collection, collection
import time
from datetime import datetime, timedelta

DEVS = (6584789596)

async def get_unique_characters(receiver_id, target_rarities=['🟢 Common', '🟣 Rare', '🟡 Legendary']):
    try:
        pipeline = [
            {'$match': {'rarity': {'$in': target_rarities}, 'id': {'$nin': [char['id'] for char in (await user_collection.find_one({'id': receiver_id}, {'characters': 1}))['characters']]}}},
            {'$sample': {'size': 1}}  # Adjust Num
        ]

        cursor = collection.aggregate(pipeline)
        characters = await cursor.to_list(length=None)
        return characters
    except Exception as e:
        return []

# Dictionary to store last claim time for each user
last_claim_time = {}

@bot.on_message(filters.command(["claimwaifu"]))
async def claim_waifu(_: bot, message: t.Message):
    chat_id = message.chat.id
    mention = message.from_user.mention
    user_id = message.from_user.id

    # Check if the user is banned
    if user_id == 7162166061:
        return await message.reply_text(f"Sorry {mention}, you are banned from using this command.")

    # Check if the user has already claimed a waifu today
    now = datetime.now()
    if user_id in last_claim_time:
        last_claim_date = last_claim_time[user_id]
        if last_claim_date.date() == now.date():
            next_claim_time = (last_claim_date + timedelta(days=1)).strftime("%H:%M:%S")
            return await message.reply_text(f"Please wait until {next_claim_time} to claim your next waifu.", quote=True)

    # Update the last claim time for the user
    last_claim_time[user_id] = now

    receiver_id = message.from_user.id
    unique_characters = await get_unique_characters(receiver_id)
    try:
        await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': {'$each': unique_characters}}})
        img_urls = [character['img_url'] for character in unique_characters]
        captions = [
            f"Congratulations {mention}! You have received a new waifu for your harem 💍!\n"
            f"Name: {character['name']}\n"
            f"Rarity: {character['rarity']}\n"
            f"Anime: {character['anime']}\n"
            for character in unique_characters
        ]
        for img_url, caption in zip(img_urls, captions):
            await message.reply_photo(photo=img_url, caption=caption)
    except Exception as e:
        print(e)