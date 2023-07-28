# Fel Argailo

## Installation

1. Clone this repository to your computer.
2. Install the necessary dependencies by running the command `pip install -r requirements.txt` in the terminal.
3. Rename the `local.env` file to `.env` and fill it with the data specified there. Below is an explanation:
## `.env` Structure
### Base bot settings
- **POLLING='True'** Responsible for the aiogram part of the bot mode. Set to False to switch to Webhook mode
- **LOCAL_SERVER_URL=''** For using your own API server. Left blank if not necessary

### Telegram configs
- **BOT_TOKEN=''** Actually, the token of your bot itself, necessary for aiogram

### Webhook example configs, for bot in Webhook mode
- **WEBHOOK_HOST='https://webhook.webhookapp.com'**
- **WEBHOOK_PATH='/webhook/${BOT_TOKEN}'**
- **WEBHOOK_URL='${WEBHOOK_HOST}${WEBHOOK_PATH}'**
- **WEBAPP_HOST='0.0.0.0'**
- **WEBAPP_PORT='8005'**

### Telethon configs, for telethon side
- **API_ID=''** Specifies the ID obtained when creating a web application at https://my.telegram.org/apps
- **API_HASH=''** Specifies the hash obtained when creating a web application at https://my.telegram.org/apps**
4. Run the bot by running the `run.py` file. At first launch, you will need to authorize the account,
which will be used by telethon as a bot, by specifying a phone number and entering a confirmation code that will come

## Project Structure

- `media/`: folder with media files used by the bot. By default, checks for changes in files every 10 minutes.
- `plugins/`: folder with various plugins and basic bot functions.
- `support/`: folder with system files of the bot.
- `utils/`: folder with utilities and helper functions.
- `.gitignore`: file with settings for ignoring files in Git.
- `config.py`: file with basic bot configuration.
- `requirements.txt`: file with a list of necessary dependencies.
- `local.env`: file with settings for your local environment.
- `README.md`: this file with information about the project.

## Support

If you have any problems or questions, please create an issue in this repository or contact the project author.

I hope this helps! If you have any further questions or need additional explanations, please let me know. I'm always here to help! 😊