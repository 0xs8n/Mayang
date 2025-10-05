# Twitter Follow Monitor Bot

A Python bot that monitors Twitter accounts and sends real-time Telegram notifications when they follow new accounts.

## Features

- Monitors multiple Twitter accounts simultaneously
- Sends instant Telegram notifications for new follows
- Uses authenticated Twitter session (no API rate limits)
- Persistent storage of following lists
- Automatic retry on errors
- Detailed logging for debugging

## Prerequisites

- Python 3.7 or higher
- Active Twitter account
- Telegram bot token
- Chrome or Firefox browser (for extracting cookies)

## Installation

1. Clone this repository or download the script

2. Install required dependencies:
```bash
pip install requests python-dotenv
```

3. Create a `.env` file in the same directory (optional):
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_CT0=your_ct0_cookie
TWITTER_AUTH_TOKEN=your_auth_token_cookie
```

## Configuration

### Getting Telegram Credentials

1. **Create a Telegram Bot:**
   - Open Telegram and message [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow the instructions
   - Save the bot token provided

2. **Get Your Chat ID:**
   - For personal notifications: Message [@userinfobot](https://t.me/userinfobot) to get your chat ID
   - For group notifications: Add your bot to a group, send a message, then visit:
     ```
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```
   - Look for `"chat":{"id":-1001234567890}` in the response

### Getting Twitter Cookies

1. **Login to Twitter:**
   - Open Chrome or Firefox
   - Go to [twitter.com](https://twitter.com) or [x.com](https://x.com)
   - Login to your account

2. **Extract Cookies:**
   - Press F12 to open Developer Tools
   - Go to Application/Storage tab
   - Click on Cookies → twitter.com or x.com
   - Find and copy these values:
     - `auth_token`
     - `ct0`

3. **Update the script:**
   - Either add them to `.env` file, or
   - Replace the default values in the script directly

### Setting Monitored Accounts

Edit the `MONITORED_USERNAMES` list in the script:

```python
MONITORED_USERNAMES = ["elonmusk", "jack", "vitalikbuterin"]
```

### Adjust Check Interval

Change `CHECK_INTERVAL` (in seconds) to control how often the bot checks:

```python
CHECK_INTERVAL = 300  # 5 minutes
```

## Usage

Run the bot:

```bash
python main.py
```

### First Run

On the first run, the bot will:
1. Initialize and fetch current following lists for monitored accounts
2. Save the data to `following_lists.json`
3. Start monitoring for new follows

### Subsequent Runs

The bot will:
1. Load previous following lists
2. Check for new follows every CHECK_INTERVAL seconds
3. Send Telegram notifications for any new follows detected
4. Update the saved following lists

## File Structure

```
.
├── main.py                    # Main bot script
├── following_lists.json       # Saved following lists (auto-generated)
├── .env                       # Environment variables (optional)
└── README.md                  # This file
```

## Output Format

When a new follow is detected, you'll receive a Telegram message like:

```
New Follow Alert

@elonmusk is now following:
Mark Zuckerberg (@zuck)
https://x.com/zuck
```

## Troubleshooting

### Bot not detecting follows

- Make sure your Twitter cookies are valid
- Check if you're logged into Twitter in your browser
- Try refreshing your cookies

### Telegram notifications not working

- Verify your bot token is correct
- Ensure the chat ID is correct (negative for groups)
- Check if the bot has permission to send messages in the group

### Rate limiting or errors

- Increase `CHECK_INTERVAL` to reduce request frequency
- Wait a few minutes if you hit rate limits
- Check the console output for specific error messages

## Security Notes

- **Never share your `.env` file or cookies publicly**
- Cookies expire after some time - you'll need to refresh them
- Keep your bot token secure
- Consider using environment variables for production

## Advanced Usage

### Running in Background

Using `screen` or `tmux`:
```bash
screen -S twitter-bot
python main.py
# Press Ctrl+A then D to detach
```

Using `nohup`:
```bash
nohup python main.py > bot.log 2>&1 &
```

### Multiple Bots

To monitor different accounts separately:
1. Create separate directories for each bot
2. Use different `.env` files
3. Run each instance independently

## Limitations

- Cookies expire periodically (usually after a few weeks)
- Twitter may detect automated behavior if checking too frequently
- Large following lists (10k+) may take longer to fetch initially

## License

This project is provided as-is for educational purposes.

## Disclaimer

This bot uses Twitter's internal API through authenticated sessions. Use responsibly and in accordance with Twitter's Terms of Service. The author is not responsible for any account restrictions or bans resulting from the use of this bot.