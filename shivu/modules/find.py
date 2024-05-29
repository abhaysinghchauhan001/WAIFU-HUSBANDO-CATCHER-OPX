import asyncio
from pyrogram import filters, Client, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot
from shivu import user_collection, collection
from datetime import datetime, timedelta
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant


DEVS =  (1643054031) # Devloper user IDs
SUPPORT_CHAT_ID = -1002134049876  # Change this to your group's chat ID

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Join Chat To Use Me", url="https://t.me/Catch_Your_WH_Group")],
    [InlineKeyboardButton("Join Chat To Use Me", url="https://t.me/CATCH_YOUR_WH_UPDATES")]
])


# Functions from the second code
async def claim_toggle(claim_state):
    try:
        await collection.update_one({}, {"$set": {"claim": claim_state}}, upsert=True)
    except Exception as e:
        print(f"Error in claim_toggle: {e}")