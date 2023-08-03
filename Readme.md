# Fel Argailo, multifunctional telegram bot for streamer, with minor but usable functions

## Currently, can:

- ### Welcome new subscribers on your channel, by post random gif or media
- ### Allow via command as reply on message, send message as post to channel
- ### All users whose media you "stole" will be placed in the local chat leaderboard

## In progress
- ### Send message to Telegram AND\OR Discord when stream is started - *IN PROCESS*
- ### Unpin channel posts in your connected chat - *WIP*
- ### Has some moderation features to save some time and clicks without opening the chat settings - *WIP*
- ### Allows you to store a variety of text, media or other types of data and send them by keyword or phrase - *WIP*

## Installation

### 1. Clone this repository to your computer.
### 2. Install the necessary dependencies by running the command `pip install -r requirements.txt` in the terminal.
### 3. Rename the `local.env` file to `.env` and fill it with the data specified.
### 4. After .env filled, and project is running, add bot(s) to channel and chat, and give admin rights
## *Important notes:* 
### The bot is developed using two libraries, aiogram and telethon, so for full functionality you need to have a classic bot with a token, and a Telegram account that will be used as a telethon user bot. Without the use of telethons, some functions, such as receiving the admin log of the channel, will not work
### More details about the difference between see there: https://docs.telethon.dev/en/stable/concepts/botapi-vs-mtproto.html and there: https://github.com/LonamiWebs/Telethon/wiki/MTProto-vs-HTTP-Bot-API

## Usage

### 1. When a new user subscribes to the channel, the bot will automatically send random media, which will be signed in the new_follower_ format and located in sub-folders of the main media folder. Currently, correctly supports gif, video, picture formats
### 2. Through the `!steal` command as a response to a user's message, the bot forwards the message on its behalf to the channel
#### `!steal patterns`
```
!steal - default pattern, post message to channel with default caption "Вкрадено у @username" and #meme tag.
!steal Some text - post message with "Some text" caption.
!steal #tag - post message with caption "Вкрадено у @username" and #tag tag.
!steal Some text #tag - combine previous patterns. Message with "Some text" caption and #tag tag.
```
### 3. Throught `!leaderboard`, you can display local leaderboard, with users and the number of messages "stolen" from them
### 4. *IN PROGRESS*

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