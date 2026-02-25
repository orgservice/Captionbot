import re
import html
import logging
from pyrogram import filters, Client, enums
from pyrogram.types import Message
from config import Config

logger = logging.getLogger(__name__)

def clean_caption_text(text: str) -> str:
    """
    Cleans the caption by strictly isolating the filename/title.
    Removes URLs, extensions, and Telegram handles.
    """
    if not text:
        return ""

    # 1. Remove raw HTTP/HTTPS links
    text = re.sub(r'https?://\S+', '', text)
    
    # 2. Extract content strictly up to the media extension
    match = re.search(r'([^\n]*?\.(?:mkv|mp4|avi|mka|zip|rar|pdf|webm))', text, flags=re.IGNORECASE)
    
    if match:
        clean_text = match.group(1).strip()
    else:
        # Fallback: Aggressively take ONLY the first non-empty line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = lines[0] if lines else ""

    # 3. Remove any stray Telegram @usernames
    clean_text = re.sub(r'@[a-zA-Z0-9_]+', '', clean_text).strip()

    # 4. Escape HTML characters (like <, >, &) to prevent Telegram HTML parse errors 
    # if a file name contains these symbols naturally.
    clean_text = html.escape(clean_text)

    # You can add custom HTML styling to the final output here if you wish:
    # Example: clean_text = f"<b>{clean_text}</b>"
    
    return clean_text

# Define filter for channel messages containing media or text
media_filter = filters.channel & (
    filters.document | filters.video | filters.audio | filters.photo | filters.text
)

@Client.on_message(media_filter, group=-1)
@Client.on_edited_message(media_filter, group=-1)
async def handle_auto_edit(client: Client, message: Message) -> None:
    """Listens for new channel posts and edits them automatically with HTML support."""
    
    # Check if restricted to specific channels
    if Config.ALLOWED_CHANNELS and message.chat.id not in Config.ALLOWED_CHANNELS:
        return

    original_text = message.caption if message.caption else message.text
    if not original_text:
        return

    cleaned_text = clean_caption_text(original_text)

    # Prevent unnecessary API calls if nothing changed
    # (Compare unescaped version to avoid loop-editing)
    if html.unescape(cleaned_text) == original_text.strip():
        return

    try:
        if message.caption:
            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=f"<b>{cleaned_text}</b>", # Adding bold HTML styling as an example
                parse_mode=enums.ParseMode.HTML 
            )
        elif message.text:
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=f"<b>{cleaned_text}</b>", # Adding bold HTML styling as an example
                parse_mode=enums.ParseMode.HTML
            )
        logger.info(f"Cleaned caption for message ID {message.id} in chat {message.chat.id}")
    except Exception as e:
        logger.error(f"Error editing caption for message ID {message.id}: {e}")
