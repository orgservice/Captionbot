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
    Removes URLs, extensions, Telegram handles, emojis, brackets, and replaces underscores/dots.
    """
    if not text:
        return ""

    # 1. Remove Emojis and Special Symbols (like ©, ®, ™, ⚠)
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text) 
    text = re.sub(r'[\u2600-\u27BF]', '', text)         
    text = re.sub(r'[©®™⚠]', '', text)                 

    # 2. Remove URLs (Matches http://, https://, AND www.)
    text = re.sub(r'(?:https?://|www\.)\S+', '', text)
    
    # 3. Remove Telegram @usernames ALONG WITH surrounding brackets/parentheses
    text = re.sub(r'[\[\(]?\s*@[a-zA-Z0-9_]+\s*[\]\)]?', '', text)
    
    # 4. Clean up any empty brackets/parentheses left behind
    text = re.sub(r'\[\s*\]|\(\s*\)|\{\s*\}', '', text)
    
    # 5. Extract content strictly up to the media extension
    match = re.search(r'([^\n]*?\.(?:mkv|mp4|avi|mka|zip|rar|pdf|webm))', text, flags=re.IGNORECASE)
    
    if match:
        clean_text = match.group(1).strip()
    else:
        # Fallback: Aggressively take ONLY the first non-empty line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = lines[0] if lines else ""

    # 6. Aggressive leading character cleanup:
    clean_text = re.sub(r'^[^a-zA-Z0-9\[\(]+', '', clean_text).strip()

    # 7. Format the filename by replacing underscores and dots with spaces (excluding the extension)
    last_dot_idx = clean_text.rfind('.')
    if last_dot_idx != -1:
        # Separate the name from the extension
        base_name = clean_text[:last_dot_idx]
        extension = clean_text[last_dot_idx:]
        
        # Replace underscores and dots with spaces in the base name
        base_name = base_name.replace('_', ' ').replace('.', ' ')
        
        # Clean up any accidental double spaces created during replacement
        base_name = re.sub(r'\s+', ' ', base_name).strip()
        
        # Reattach the extension
        clean_text = base_name + extension
    else:
        # If no extension is found, just replace everything
        clean_text = clean_text.replace('_', ' ').replace('.', ' ')
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    # 8. Escape HTML characters (like <, >, &) to prevent Telegram HTML parse errors 
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
    """Listens for new channel posts and edits them automatically with HTML support."""
    
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
