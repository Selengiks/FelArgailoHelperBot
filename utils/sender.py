import typing
from aiogram import md, types


async def send_data(
    message: types.Message,
    chat_id: typing.Union[str, int],
    disable_notification: typing.Optional[bool] = None,
    disable_web_page_preview: typing.Optional[bool] = None,
    reply_to_message_id: typing.Optional[int] = None,
    reply_markup: typing.Union[
        types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, None
    ] = None,
    caption: str = None,
) -> types.Message:
    """Allow to send different types of media and make some additional configurations"""
    kwargs = {
        "chat_id": chat_id,
        "allow_sending_without_reply": True,
        "reply_markup": reply_markup or message.reply_markup,
        "parse_mode": types.ParseMode.HTML,
        "disable_notification": disable_notification,
        "reply_to_message_id": reply_to_message_id,
    }
    text = formatter_text(message)

    if message.text:
        kwargs["disable_web_page_preview"] = disable_web_page_preview
        return await message.bot.send_message(text=text, **kwargs)
    elif message.audio:
        return await message.bot.send_audio(
            audio=message.audio.file_id,
            caption=caption or text,
            title=message.audio.title,
            performer=message.audio.performer,
            duration=message.audio.duration,
            **kwargs,
        )
    elif message.animation:
        return await message.bot.send_animation(
            animation=message.animation.file_id, caption=caption or text, **kwargs
        )
    elif message.document:
        return await message.bot.send_document(
            document=message.document.file_id, caption=caption or text, **kwargs
        )
    elif message.photo:
        return await message.bot.send_photo(
            photo=message.photo[-1].file_id, caption=caption or text, **kwargs
        )
    elif message.sticker:
        kwargs.pop("parse_mode")
        return await message.bot.send_sticker(sticker=message.sticker.file_id, **kwargs)
    elif message.video:
        return await message.bot.send_video(
            video=message.video.file_id, caption=caption or text, **kwargs
        )
    elif message.video_note:
        kwargs.pop("parse_mode")
        return await message.bot.send_video_note(
            video_note=message.video_note.file_id, **kwargs
        )
    elif message.voice:
        return await message.bot.send_voice(voice=message.voice.file_id, **kwargs)
    elif message.contact:
        kwargs.pop("parse_mode")
        return await message.bot.send_contact(
            phone_number=message.contact.phone_number,
            first_name=message.contact.first_name,
            last_name=message.contact.last_name,
            vcard=message.contact.vcard,
            **kwargs,
        )
    elif message.venue:
        kwargs.pop("parse_mode")
        return await message.bot.send_venue(
            latitude=message.venue.location.latitude,
            longitude=message.venue.location.longitude,
            title=message.venue.title,
            address=message.venue.address,
            foursquare_id=message.venue.foursquare_id,
            foursquare_type=message.venue.foursquare_type,
            **kwargs,
        )
    elif message.location:
        kwargs.pop("parse_mode")
        return await message.bot.send_location(
            latitude=message.location.latitude,
            longitude=message.location.longitude,
            **kwargs,
        )
    elif message.poll:
        kwargs.pop("parse_mode")
        return await message.bot.send_poll(
            question=message.poll.question,
            options=[option.text for option in message.poll.options],
            **kwargs,
        )
    else:
        raise TypeError("This type of message can't be copied.")


def formatter_text(message: types.Message):
    html_text = message.html_text if (message.text or message.caption) else None
    if not html_text:
        return html_text
    formatter = {
        "user": md.quote_html(message.from_user.full_name),
        "id": message.from_user.id,
        "username": message.from_user.username,
        "text": md.quote_html(message.text),
    }
    return html_text.format(**formatter)
