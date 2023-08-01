# Fel Argailo, multifunctional telegram bot for streamer, with minor but usable functions

## Currently, can:

- ### Welcome new subscribers on your channel, by post random gif or media
- ### Allow via command as reply on message, send message as post to channel

## In progress
- ### Send message to Telegram AND\OR Discord when stream is started - *WIP*
- ### Unpin channel posts in your connected chat - *WIP*
- ### All users whose media you "stole" will be placed in the local chat leaderboard - *WIP*
- ### Has some moderation features to save some time and clicks without opening the chat settings - *WIP*
- ### Allows you to store a variety of text, media or other types of data and send them by keyword or phrase - *WIP*

## Installation

### 1. Clone this repository to your computer.
### 2. Install the necessary dependencies by running the command `pip install -r requirements.txt` in the terminal.
### 3. Rename the `local.env` file to `.env` and fill it with the data specified there. Below is an explanation:
### `.env` Structure
#### Base bot settings
- **POLLING='True'** Responsible for the aiogram part of the bot mode. Set False to switch to Webhook mode
- **LOCAL_SERVER_URL=''** For using your own API server. Left blank if not necessary

#### Telegram configs
- **BOT_TOKEN=''** # Set here your bot token, received from @BotFather
- **ADMIN=''**  # Global admin ID, who can use bot functionality
- **CHANNEL=''**  # Target channel, need for some functions, which interract with channel

#### Webhook example configs, for bot in Webhook mode
- **WEBHOOK_HOST='https://webhook.webhookapp.com'**
- **WEBHOOK_PATH='/webhook/${BOT_TOKEN}'**
- **WEBHOOK_URL='${WEBHOOK_HOST}${WEBHOOK_PATH}'**
- **WEBAPP_HOST='0.0.0.0'**
- **WEBAPP_PORT='8005'**

#### Redis configs, for availability use local storage instead MemoryStorage
- **REDIS_HOST='localhost'** # Set your db host, or leave for local db
- **REDIS_PORT='6379'** #  Set db host port, or leave default
- **REDIS_DB='0'** # Set number of redis db (Redis allow use up to 16 db via db number 0-16)
- **REDIS_DB_NAME='FelArgailoDB'** # Set db name for your bot, or leave default

#### Telethon configs, for telethon side
- **API_ID=''** Specifies the ID obtained when creating a web application at https://my.telegram.org/apps
- **API_HASH=''** Specifies the hash obtained when creating a web application at https://my.telegram.org/apps**

#### Twitch configs
- **CLIENT_ID=''** Your Twitch client id. More on https://dev.twitch.tv/console/apps/ or google how to get it
- **CLIENT_SECRET=''** Your client secret key. How to is same as above
### 4. Run the bot by running the `run.py` file. At first launch, you will need to authorize the account, which will be used by telethon as a bot, by specifying a phone number and entering a confirmation code that will come

## Project Structure

- `media/`: folder with media files used by the bot. By default, checks for changes in files every 10 minutes.
- `plugins/`: folder with various plugins and basic bot functions.
- `support/`: folder with system files of the bot.
- `utils/`: folder with utilities and helper functions.
- `.gitignore`: file with settings for ignoring files and folders in Git.
- `config.py`: file with basic bot configuration.
- `requirements.txt`: file with a list of necessary dependencies.
- `local.env`: file with settings for your local environment.

## Support

If you have any problems or questions, please create an issue in this repository. 😊