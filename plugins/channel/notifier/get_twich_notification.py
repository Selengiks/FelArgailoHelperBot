import asyncio
import requests
from loguru import logger


async def twitch_stream_handler(client_id, access_token, channel):
    """Check target user on Twitch and handle if stream on channel is started. By default, check every 5 minutes."""
    while True:
        streams_url = "https://api.twitch.tv/helix/streams"
        streams_params = {"user_login": channel}
        streams_headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}",
        }
        streams_response = requests.get(
            streams_url, params=streams_params, headers=streams_headers
        )
        stream_data = streams_response.json()["data"]

        if stream_data:
            logger.info(f"Handled Twitch event.{channel} is live!")
            # Do something
        else:
            logger.trace(f"No stream events for [{channel}] channel.")

        await asyncio.sleep(
            900
        )  # Set update interval in seconds (3600 = 1 hour, 900 = 15 minutes)


async def on_startup(client_id, client_secret, channel):
    auth_url = "https://id.twitch.tv/oauth2/token"
    auth_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    auth_response = requests.post(auth_url, params=auth_params)
    access_token = auth_response.json()["access_token"]

    asyncio.create_task(twitch_stream_handler(client_id, access_token, channel))
    logger.trace("twitch_notifier loaded")
