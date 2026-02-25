import logging
from pyrogram import filters, Client
from pyrogram.types import Message

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

    await message.reply_text(
        text=welcome_text,
        disable_web_page_preview=True,
        quote=True
    )
