import logging
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message) -> None:
    """Handles the /start command to welcome users using HTML formatting."""
    user_name = message.from_user.first_name if message.from_user else "User"
    
    welcome_text = (
        f"👋 Hi <b>{user_name}</b>,\n\n"
        "<b>I am the Auto Caption Remover Bot!</b> 🤖\n\n"
        "💡 <u><b>How to use:</b></u>\n"
        "<i>Just add me as an Admin in your channel with Edit Messages permission, and I will handle the rest automatically!</i>"
    )

    # Define the inline keyboard with the new Update Channel button styling
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📢 Update Channel", 
                    url="https://t.me/YourUpdateChannel", # Replace with your actual channel link
                    # Note: These parameters require a library version that supports the latest Bot API
                    style="primary", 
                    icon_custom_emoji_id="5373303496357388091" # Replace with your custom emoji ID, or remove if not needed
                ) 
            ]
        ]
    )

    await message.reply_text(
        text=welcome_text,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=reply_markup
    )
