import logging
from pyrogram import Client, enums
from config import Config

# Configure application-wide logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Suppress overly verbose Pyrogram logs
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class AutoCaptionBot(Client):
    def __init__(self):
        super().__init__(
            name="Captioner",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=20,
            plugins=dict(root="Plugins"),
            parse_mode=enums.ParseMode.HTML # Global HTML support enabled
        )

    def run(self):
        """Starts the Pyrogram client safely."""
        try:
            logger.info("⚡ Caption Bot Started 🚀")
            super().run()
        except Exception as e:
            logger.error(f"❌ Bot Stoped: {e}", exc_info=True)
        finally:
            logger.info("Bot has been shut down securely.")

if __name__ == "__main__":
    app = AutoCaptionBot()
    app.run()
