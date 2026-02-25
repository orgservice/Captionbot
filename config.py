import os

class Config:
    # Fetching secrets from environment variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8591161370:AAHVltcHDBLMtDq4DFsxg2mQEsdn4zMZJP0")
    API_ID = int(os.environ.get("API_ID", "25465082"))
    API_HASH = os.environ.get("API_HASH", "4a6b5e40c8bc08c8af09add6cca23b18")
    
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "HIT_Sir") # without @

    # Parses comma-separated channel IDs. Example: "-1001234567890, -1009876543210"
    allowed_channels = os.environ.get("ALLOWED_CHANNELS", "")
    ALLOWED_CHANNELS = [
        int(ch.strip()) for ch in allowed_channels.split(",") if ch.strip()
    ] if allowed_channels else []

    # Web Server configuration for Koyeb deployment
    PORT = int(os.environ.get("PORT", "8080"))
    WEB_RESPONSE = {"status": "Auto Caption Remover Bot is Running Successfully!"}
