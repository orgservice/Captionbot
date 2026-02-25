import re
import html
import logging
import asyncio
from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from config import Config

logger = logging.getLogger(__name__)

def clean_caption_text(text: str) -> str:
    """Isolates and formats the filename from the caption."""
    if not text:
        return ""

    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text) 
    text = re.sub(r'[\u2600-\u27BF]', '', text)         
    text = re.sub(r'[©®™⚠]', '', text)                 

    text = re.sub(r'(?:https?://|www\.)\S+', '', text)
    text = re.sub(r'[\[\(]?\s*@[a-zA-Z0-9_]+\s*[\]\)]?', '', text)
    text = re.sub(r'\[\s*\]|\(\s*\)|\{\s*\}', '', text)
    
    match = re.search(r'([^\n]*?\.(?:mkv|mp4|avi|mka|zip|rar|pdf|webm))', text, flags=re.IGNORECASE)
    
    if match:
        clean_text = match.group(1).strip()
    else:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = lines[0] if lines else ""

    clean_text = re.sub(r'^[^a-zA-Z0-9\[\(]+', '', clean_text).strip()

    last_dot_idx = clean_text.rfind('.')
    if last_dot_idx != -1:
        base_name = clean_text[:last_dot_idx]
        extension = clean_text[last_dot_idx:]
        base_name = base_name.replace('_', ' ')
        base_name = re.sub(r'\s+', ' ', base_name).strip()
        clean_text = base_name + extension
    else:
        clean_text = clean_text.replace('_', ' ').replace('.', ' ')
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    if clean_text:
        clean_text = html.escape(clean_text)
    
    return clean_text


media_filter = filters.channel & (filters.document | filters.video)

@Client.on_message(media_filter, group=-1)
@Client.on_edited_message(media_filter, group=-1)
async def handle_auto_edit(client: Client, message: Message) -> None:
    """Auto-edits new channel posts."""
    if Config.ALLOWED_CHANNELS and message.chat.id not in Config.ALLOWED_CHANNELS:
        return

    original_text = message.caption if message.caption else ""
    media = message.document or message.video
    
    if not original_text:
        file_name = getattr(media, 'file_name', None)
        if file_name:
            original_text = file_name
        else:
            return

    cleaned_text = clean_caption_text(original_text)

    is_already_bold = False
    if message.caption_entities:
        for entity in message.caption_entities:
            if entity.type == enums.MessageEntityType.BOLD:
                is_already_bold = True
                break

    if html.unescape(cleaned_text) == original_text.strip() and is_already_bold:
        return

    while True:
        try:
            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption=f"<b>{cleaned_text}</b>", 
                parse_mode=enums.ParseMode.HTML 
            )
            # logger.info(f"Edited caption for message ID {message.id} in chat {message.chat.id}")
            break 
            
        except FloodWait as e:
            logger.warning(f"FloodWait: Sleeping for {e.value}s")
            await asyncio.sleep(e.value)
            
        except Exception as e:
            logger.error(f"Error editing message ID {message.id}: {e}")
            break
