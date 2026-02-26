import logging
import aiohttp
from pyrogram import filters, Client, enums
from pyrogram.types import (
    Message, 
    CallbackQuery, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message) -> None:
    """Handles the /start command to welcome users using HTML formatting."""
    user_name = message.from_user.first_name if message.from_user else "User"
    
    welcome_text = (
        f"👋 Hi <b>{user_name}</b>,\n\n"
        "<b>I am the Auto Caption Cleaner Bot!</b> 🤖\n\n"
        "💡 <u><b>How to use:</b></u>\n"
        "<i>Just add me as an Admin in your channel with Edit Messages permission, and I will handle the rest automatically!</i>"
    )

    # 1. Build the raw JSON payload for Telegram's HTTP API with all 3 colored buttons
    payload = {
        "chat_id": message.chat.id,
        "text": welcome_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_to_message_id": message.id,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📢 Update Channel",
                        "url": "https://t.me/imaxprime", # Replace with your actual channel link
                        "style": "primary", # Blue background
                        "icon_custom_emoji_id": "5373303496357388091" # Replace or remove if not needed
                    }
                ],
                [
                    {
                        "text": "ℹ️ About",
                        "callback_data": "about_cb",
                        "style": "success" # Green background
                    },
                    {
                        "text": "❌ Close",
                        "callback_data": "close_cb",
                        "style": "danger" # Red background
                    }
                ]
            ]
        }
    }

    # 2. Send the message directly using aiohttp to support the new colors
    bot_token = client.bot_token
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status != 200:
                    error_data = await response.text()
                    logger.error(f"Failed to send styled start message: {error_data}")
    except Exception as e:
        logger.error(f"Error making HTTP request: {e}")

@Client.on_callback_query(filters.regex("^(about_cb|close_cb)$"))
async def handle_callbacks(client: Client, query: CallbackQuery):
    """Handles clicks for the About and Close buttons."""
    
    if query.data == "close_cb":
        # Delete the message when "Close" is clicked
        await query.message.delete()
        
    elif query.data == "about_cb":
        # Show an About message formatted with HTML
        about_text = (
            "🤖 <b>Auto Caption Cleaner Bot</b>\n\n"
            "This bot automatically removes unwanted links, tags, and text from media "
            "uploaded to your channels, keeping only the clean file name.\n\n"
            "👨‍💻 <b>Developer:</b> <a href='https://t.me/ZeroCivicSense'>@ZeroCivicSense</a>"
        )
        
        await query.answer("Fetching About Info...", show_alert=False)
        
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])
        
        # Use standard Pyrogram edit_text since we don't need colors here
        await query.message.edit_text(
            text=about_text,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

@Client.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start_callback(client: Client, query: CallbackQuery):
    """Restores the original start message by editing the current message."""
    await query.answer()
    
    # Get the user's name for the welcome text
    user_name = query.from_user.first_name if query.from_user else "User"
    
    welcome_text = (
        f"👋 Hi <b>{user_name}</b>,\n\n"
        "<b>I am the Auto Caption Cleaner Bot!</b> 🤖\n\n"
        "💡 <u><b>How to use:</b></u>\n"
        "<i>Just add me as an Admin in your channel with Edit Messages permission, and I will handle the rest automatically!</i>"
    )

    # 1. Build the raw JSON payload for editing the message
    payload = {
        "chat_id": query.message.chat.id,
        "message_id": query.message.id, # We specify the message_id to EDIT it
        "text": welcome_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📢 Update Channel",
                        "url": "https://t.me/imaxprime", # Replace with your actual channel link
                        "style": "primary", # Blue background
                        "icon_custom_emoji_id": "5373303496357388091" # Replace or remove if not needed
                    }
                ],
                [
                    {
                        "text": "ℹ️ About",
                        "callback_data": "about_cb",
                        "style": "success" # Green background
                    },
                    {
                        "text": "❌ Close",
                        "callback_data": "close_cb",
                        "style": "danger" # Red background
                    }
                ]
            ]
        }
    }

    # 2. Call the editMessageText endpoint directly to restore the colors
    bot_token = client.bot_token
    api_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status != 200:
                    error_data = await response.text()
                    logger.error(f"Failed to edit styled start message: {error_data}")
    except Exception as e:
        logger.error(f"Error making HTTP request for edit: {e}")
