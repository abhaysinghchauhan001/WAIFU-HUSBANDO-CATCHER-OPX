from pyrogram import Client, filters
from pyrogram.types import Message
import youtube_dl
import os
import config  # Import your config module

# Create a Client instance named 'shivuu'
shivuu = Client("shivuu", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Function to download Instagram videos
def download_instagram(url: str) -> str:
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@shivuu.on_message(filters.regex(r'https?://(www\.)?instagram\.com/p/'))
def handle_instagram_link(client: Client, message: Message) -> None:
    url: str = message.text.strip()
    try:
        file_name: str = download_instagram(url)
        with open(file_name, "rb") as video_file:
            shivuu.send_video(message.chat.id, video_file)
        os.remove(file_name)  # Optionally remove the file after sending
    except Exception as e:
        message.reply("Failed to download the video. Please check the URL.")