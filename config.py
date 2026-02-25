import os

class Config:
    # Fetching secrets from environment variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8591161370:AAEhWSq_SA-eApXE1UC03TCdVaVzle4POYI")
    API_ID = int(os.environ.get("API_ID", "25465082"))
    API_HASH = os.environ.get("API_HASH", "4a6b5e40c8bc08c8af09add6cca23b18")
    
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "HIT_Sir") # without @

    # Parses comma-separated channel IDs. Example: "-1001234567890, -1009876543210"
    allowed_channels = os.environ.get("ALLOWED_CHANNELS", "")
    ALLOWED_CHANNELS = [
        int(ch.strip()) for ch in allowed_channels.split(",") if ch.strip()
    ] if allowed_channels else []
