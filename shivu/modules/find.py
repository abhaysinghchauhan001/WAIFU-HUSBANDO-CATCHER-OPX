import asyncio
from pyrogram import filters, Client, types as t
from shivu import shivuu as bot
from shivu import user_collection, collection
import time
from datetime import datetime, timedelta

@bot.on_message(filters.command(["p"]))
async def p(_, message: t.Message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide the waifu ID.", quote=True)
    
    waifu_id = message.command[1]
    waifu = await collection.find_one({'id': waifu_id})
    
    if not waifu:
        return await message.reply_text("No waifu found with that ID.", quote=True)
    
    # Get the top 10 users with the most of this waifu in the current chat
    top_users = await user_collection.aggregate([
        {'$match': {'characters.id': waifu_id}},
        {'$unwind': '$characters'},
        {'$match': {'characters.id': waifu_id}},
        {'$group': {'_id': '$id', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]).to_list(length=10)
    
    # Get the usernames of the top users
    usernames = []
    for user_info in top_users:
        user_id = user_info['_id']
        try:
            user = await bot.get_users(user_id)
            usernames.append(user.username if user.username else f"User {username}")
        except Exception as e:
            print(e)
            usernames.append(f"User {username}")
    
    # Construct the caption
    caption = (
        f"Waifu Information:\n"
        f"Name: {waifu['name']}\n"
        f"Rarity: {waifu['rarity']}\n"
        f"Anime: {waifu['anime']}\n"
        f"ID: {waifu['id']}\n\n"
        f"Here is the list of users who have this character:\n\n"
    )
    for i, user_info in enumerate(top_users):
        count = user_info['count']
        username = usernames[i]
        caption += f"{i + 1}. {username} x{count}\n"
    
    # Reply with the waifu information and top users
    await message.reply_photo(photo=waifu['img_url'], caption=caption)