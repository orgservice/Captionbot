import os


class Config(object):
    # env vars
    BOT_TOKEN = "7372474546:AAHY6OwSess3qxfP886CGKKWVVItZohX1KM"  # string
    API_ID = 25465082 # int
    API_HASH = "4a6b5e40c8bc08c8af09add6cca23b18"  # string
    
    # db vars
    # keep empty if don't want to add any extra caption
    CAPTION_TEXT = ""  
    # BOTTOM or TOP or NIL
    CAPTION_POSITION = "BOTTOM"  
    ADMIN_USERNAME = "adultsupport"  # without "@". 

    # a list of strings of words to remove from the existing caption
    WORDS_TO_REMOVE = []  
    # a list of regex pattern strings to remove from the existing caption. 
    # For eg. r".*Join.*" will remove the entire line having word Join
    REGEX_PATTERNS = []  

    # keep empty to allow in all channels. Can add multiple channels separated by a comma.
    # Don't forget -100 before the channel ID
    ALLOWED_CHANNELS = [-100123456789]

    # REMOVE or POSTFIX or NIL. Useful for tamilblasters, tamilmv and other webites
    WEBSITE_PREFIX = "POSTFIX"  

    # True or False. Replaces YIFY website with YTS
    YTS_WEBSITE_REPLACE = True 

    # Dictionary of words to replace
    REPLACE_DICTIONARY = {}

    # Replace dot separator with space
    SEPARATOR_SPACE = True
