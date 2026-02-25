import re
import html
import logging
import asyncio # Imported for FloodWait sleep
from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait # Imported to handle rate limits
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

    # 1. Remove URLs (Matches http://, https://, AND www.)
    text = re.sub(r'(?:https?://|www\.)\S+', '', text)
    
    # 2. Remove any stray Telegram @usernames
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)
    
    # 3. Clean up stray leading spaces, hyphens, pipes, or colons left behind after removing URLs
    text = re.sub(r'^[\s\-|_:]+', '', text)

    # 4. Extract content strictly up to the media extension
    match = re.search(r'([^\n]*?\.(?:mkv|mp4|avi|mka|zip|rar|pdf|webm))', text, flags=re.IGNORECASE)
    
    if match:
        clean_text = match.group(1).strip()
    else:
        # Fallback: Aggressively take ONLY the first non-empty line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = lines[0] if lines else ""

    # Clean leading characters again just in case the regex extraction left some behind
    clean_text = re.sub(r'^[\s\-|_:]+', '', clean_text).strip()

    # 5. Escape HTML characters (like <, >, &) to prevent Telegram HTML parse errors 
    if clean_text:
        clean_text = html.escape(clean_text)
    
    return clean_text

# Define filter for channel messages to strictly ONLY trigger on Document or Video
media_filter = filters.channel & (
    filters.document | filters.video
)

@Client.on_message(media_filter, group=-1)
@Client.on_edited_message(media_filter, group=-1)
async def handle_auto_edit(client: Client, message: Message) -> None:
    # ... (Keep the rest of your handle_auto_edit function exactly the same as before) ...
    
    # Check if restricted to specific channels
    if Config.ALLOWED_CHANNELS and message.chat.id not in Config.ALLOWED_CHANNELS:
        return

    original_text = message.caption if message.caption else ""
    media = message.document or message.video
    
    # If the post has no caption, fetch the raw file_name from the media object
    if not original_text:
        file_name = getattr(media, 'file_name', None)
        if file_name:
            original_text = file_name
        else:
            return

    cleaned_text = clean_caption_text(original_text)

    # Check if the text already contains a bold entity
    is_already_bold = False
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == enums.MessageEntityType.BOLD:
                is_already_bold = True
                break

    # Prevent unnecessary API calls ONLY if the text is perfectly clean AND already bolded
    if html.unescape(cleaned_text) == original_text.strip() and is_already_bold:
        return

    # Implement retry mechanism for FloodWait during bulk uploads
    while True:
        try:
            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=f"<b>{cleaned_text}</b>", 
                parse_mode=enums.ParseMode.HTML 
            )
            logger.info(f"Successfully formatted/cleaned caption for message ID {message.id} in chat {message.chat.id}")
            break 
            
        except FloodWait as e:
            logger.warning(f"FloodWait triggered! Sleeping for {e.value} seconds before retrying...")
            await asyncio.sleep(e.value)
            
        except Exception as e:
            logger.error(f"Error editing caption for message ID {message.id}: {e}")
            break
