import logging
import asyncio
from aiohttp import web
from pyrogram import Client, enums, idle
from config import Config
from Plugins import web_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
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
            parse_mode=enums.ParseMode.HTML
        )

async def start():
    """Starts both the aiohttp web server and the Pyrogram client."""
    try:
        # 1. Start Web Server from Plugins/__init__.py
        app = await web_server()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", Config.PORT)
        await site.start()
        logger.info(f"🌐 Web Server Started on Port: {Config.PORT}")

        # 2. Start Telegram Bot
        bot = AutoCaptionBot()
        await bot.start()
        logger.info("⚡ Bot Started Successfully 🚀")
        
        # Keep the services running
        await idle()
        
    except Exception as e:
        logger.error(f"❌ Error occurred: {e}", exc_info=True)
    finally:
        # Graceful shutdown
        await bot.stop()
        await runner.cleanup()
        logger.info("🤖 Bot have been shut down securely.")

if __name__ == "__main__":
    # Start the async event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
