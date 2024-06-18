import os


class Config(object):
    # env vars
    BOT_TOKEN = "7372474546:AAHY6OwSess3qxfP886CGKKWVVItZohX1KM"  # string
    API_ID = 25465082 # int
    API_HASH = "4a6b5e40c8bc08c8af09add6cca23b18"  # string
    
    # db vars
    # keep empty if don't want to add any extra caption
    CAPTION_TEXT = "#𝙊𝙍𝙂𝙋𝙧𝙞𝙢𝙚 – #𝙉𝙤𝟏 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝙈𝙤𝙫𝙞𝙚𝙨 𝘼𝙣𝙙 𝙒𝙚𝙗 𝙎𝙚𝙧𝙞𝙚𝙨 𝙀𝙣𝙩𝙚𝙧𝙩𝙖𝙞𝙣𝙢𝙚𝙣𝙩 𝘾𝙝𝙖𝙣𝙣𝙚𝙡.\n\n**⏤͟͞𝗝⌡𝗼𝗶𝗻 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 –「 @ORGPrime 」**"  
    # BOTTOM or TOP or NIL
    CAPTION_POSITION = "BOTTOM"  
    ADMIN_USERNAME = "adultsupport"  # without "@". 

    # a list of strings of words to remove from the existing caption
    WORDS_TO_REMOVE = ["©@piro_files & 🤖@piroxbots", "@piro_files", "@piroxbots", "⚡ Join :- [@flimyworld_17]", "💥Join:- @ViSHWA_MOViEX", "🍿 𝖩𝗈𝗂𝗇  ➥ 「 @RJMoviessWorld 」"]  
    # a list of regex pattern strings to remove from the existing caption. 
    # For eg. r".*Join.*" will remove the entire line having word Join
    REGEX_PATTERNS = []  

    # keep empty to allow in all channels. Can add multiple channels separated by a comma.
    # Don't forget -100 before the channel ID
    ALLOWED_CHANNELS = []

    # REMOVE or POSTFIX or NIL. Useful for tamilblasters, tamilmv and other webites
    WEBSITE_PREFIX = "NIL"  

    # True or False. Replaces YIFY website with YTS
    YTS_WEBSITE_REPLACE = True 

    # Dictionary of words to replace
    REPLACE_DICTIONARY = {}

    # Replace dot separator with space
    SEPARATOR_SPACE = True
