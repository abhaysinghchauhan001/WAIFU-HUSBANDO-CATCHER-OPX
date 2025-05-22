class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5536473064"
    sudo_users = "5536473064", "6382664842",
    GROUP_ID = -1002559277065
    TOKEN = "7556031866:AAFRrkLSeK23mne7AqlNjV-Z4eFmJzuWi3M"
    mongo_url = "mongodb+srv://iamnobita1:nobitamusic1@cluster0.k08op.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://files.catbox.moe/ttk2n4.jpg", "https://files.catbox.moe/g8rtaj.jpg"]
    SUPPORT_CHAT = "https://t.me/+wPjAlUcObehiZDM1"
    UPDATE_CHAT = "NOBITA_MUSIC_SUPPORT"
    BOT_USERNAME = "NobitaGrabberBot"
    BOT_NAME = "『 𝐍𝐎𝐁𝐈𝐓𝐀 ✘ 𝐂𝐀𝐓𝐂𝐇𝐄𝐑 』"
    CHARA_CHANNEL_ID = "-1002559277065"
    api_id = 28269355
    api_hash = "805b8c6577a8c30db439d901af544cac"

    STRICT_GBAN = True
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
