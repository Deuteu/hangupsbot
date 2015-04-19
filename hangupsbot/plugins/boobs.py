import asyncio
#for image
import aiohttp
import os
import io
#for test presence in text
import re

keyword = "boobs"

def _initialise(Handlers, bot=None):
    if "register_admin_command" in dir(Handlers) and "register_user_command" in dir(Handlers):
        Handlers.register_admin_command(["minor", "major"])
    _create_boobs_in_memory(bot)
    Handlers.register_handler(_handle_autoreply)
    return []

def _create_boobs_in_memory(bot):
    boobs = {}
    bot.memory.set_by_path([keyword], boobs)
    bot.memory.save()

@asyncio.coroutine
def _handle_autoreply(bot, event, command):
    """Handle autoreplies to boobs in messages"""
    if boobs_in_text(event.text):
        if is_major(bot, event.conv.id_):
            # TODO: Use local image
            link_image = "http://deberdt.fr/Ingress/Boobs.jpg"
            filename = os.path.basename(link_image)
            r = yield from aiohttp.request('get', link_image)
            raw = yield from r.read()
            image_data = io.BytesIO(raw)
            image_id = yield from bot._client.upload_image(image_data, filename=filename)
            bot.send_message_segments(event.conv.id_, None, image_id=image_id)

def boobs_in_text(text):
    """Return True if Boobs is in text"""
    regexword = "\\b" + "Boobs" + "\\b"
    return True if re.search(regexword, text, re.IGNORECASE) else False

def is_major(bot, conv_id):
    dict = bot.memory.get(keyword)
    if conv_id in dict:
        return dict[conv_id] == 1
    return False

def major(bot, event, *args):
    dict = bot.memory.get(keyword)
    dict[event.conv.id_] = 1
    bot.memory.set_by_path([keyword], dict)
    bot.memory.save()

def minor(bot, event, *args):
    dict = bot.memory.get(keyword)
    dict[event.conv.id_] = 0
    bot.memory.set_by_path([keyword], dict)
    bot.memory.save()