import re
import logging
from pyrogram import filters, enums
from bot import AutoCaptionBot
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

allowed_channels = Config.ALLOWED_CHANNELS

def clean_caption_text(text):
    """
    Cleans the caption by strictly isolating the filename/title.
    If an extension is found, it cuts off everything after it.
    If NO extension is found, it aggressively takes ONLY the first line.
    """
    if not text:
        return ""

    # 1. Clean out any raw HTTP/HTTPS links from the whole text right away
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # 2. Check for an extension (.mkv, .mp4, etc.)
    # This grabs the line from the beginning up to the extension and stops.
    match = re.search(r'([^\n]*?\.(?:mkv|mp4|avi|mka|zip|rar|pdf|webm))', text, flags=re.IGNORECASE)
    
    if match:
        # Scenario A: Extension FOUND.
        # Keep exactly up to the extension and drop the rest.
        clean_text = match.group(1).strip()
    else:
        # Scenario B: NO extension found (e.g., Bloody.Babu...H.264-Archie)
        # Aggressive fallback: Split the caption by newlines, ignore empty lines, 
        # and strictly keep ONLY the very first line.
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            clean_text = lines[0]
        else:
            clean_text = ""

    # 3. Final polish: Remove any stray Telegram @usernames just in case 
    # someone put "@Channel MovieName" on the first line.
    clean_text = re.sub(r'@[a-zA-Z0-9_]+', '', clean_text).strip()

    return clean_text

# Define filters for messages containing media or text
f = filters.channel & (filters.document | filters.video | filters.audio | filters.photo | filters.text)

@AutoCaptionBot.on_message(f, group=-1)
@AutoCaptionBot.on_edited_message(f, group=-1)
async def editing(bot, message):
    # Check if the current channel is in the list of allowed channels
    if allowed_channels and message.chat.id not in allowed_channels:
        return

    # Extract the original text/caption from the post
    original_text = message.caption if message.caption else message.text
    
    if not original_text:
        return

    # Clean the text using our perfect cleaning function
    cleaned_text = clean_caption_text(original_text)

    # Check if the text actually changed to prevent unnecessary API calls
    if cleaned_text.strip() == original_text.strip():
        return

    try:
        # Edit the message with the perfectly cleaned text
        if message.caption:
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=cleaned_text,
                parse_mode=enums.ParseMode.DISABLED # Prevents markdown from triggering on "_" or "*" characters
            )
        elif message.text:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=cleaned_text,
                parse_mode=enums.ParseMode.DISABLED
            )
        logger.info(f"Successfully cleaned caption for message {message.id}")
    except Exception as e:
        logger.error(f"Error editing caption: {e}")
