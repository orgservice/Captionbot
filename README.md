<h1 align='center'>🖊️ TG AutoCaption Remover Bot </h1>

<h4 align='center'>
    Telegram Bot for Automatically Cleaning and Formatting Media Captions<br><br>
    <i>(Exclusive to public or private Telegram channels)</i> 
</h4><br>

## Overview

TG AutoCaption Remover Bot is a Telegram bot designed to automatically clean up files and videos posted in your channels. Instead of adding custom text, it strips away unwanted clutter (like URLs and Telegram handles) and isolates the pure file name, formatting it neatly in bold.

## Features

- **Filename Extraction:** Strictly extracts the media title up to its extension (e.g., .mkv, .mp4, .zip, .pdf).
- **Link & Tag Removal:** Automatically removes HTTP/HTTPS links and stray `@usernames` from the caption.
- **HTML Formatting:** Formats the cleaned filename in bold HTML (`<b>filename</b>`) for a cleaner look.
- **Channel Restriction:** Can be configured to work globally or restricted to specific allowed channels.

## Configuration

1. **Create a Bot on Telegram:**
   - Start by creating a new bot on Telegram using [@BotFather](https://t.me/BotFather).
   - After creating the bot, add it to your channel and grant it "Edit Messages" admin rights.

2. **Environment Variables (`config.py`):**
   - Customize the bot behavior by setting the following environment variables:
     - `BOT_TOKEN`: Your Telegram Bot Token from @BotFather.
     - `API_ID`: Your Telegram API ID (from my.telegram.org).
     - `API_HASH`: Your Telegram API Hash (from my.telegram.org).
     - `ADMIN_USERNAME`: Username to display for the admin (without "@").
     - `ALLOWED_CHANNELS`: Comma-separated list of channel IDs where the bot is allowed to work. Leave empty to allow in all channels.

## Deployment

### Local Deployment

1. **Download this repository:**
   - Clone or download this repository to your local machine.

2. **Install required packages:**
   - Open a terminal and run the following command:
     ```bash
     pip3 install -r requirements.txt
     ```

3. **Configure variables:**
   - Set up your environment variables or edit the `config.py` file.

4. **Run the bot:**
   - Start the bot by running the following command in your terminal:
     ```bash
     python3 bot.py
     ```

### Heroku Deployment
The repository includes an `app.json` and `Procfile`, making it ready for 1-click deployment on Heroku. Ensure you fill in the required `BOT_TOKEN`, `API_ID`, and `API_HASH` in the Heroku dashboard.

## Commands

- `/start`: Starts the bot and displays the welcome message with usage instructions.

## Credits

This repository is a modification of Caption Bot by avipatilpro. Special thanks for the original implementation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
