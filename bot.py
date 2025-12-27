import logging

logging.basicConfig(level = logging.INFO)

import asyncio
from vkbottle.bot import Bot, Message
from voice_whisper import download, transcribe, close_session
import os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token = os.getenv("TOKEN"))


@bot.on.chat_message(attachment = "audio_message")
async def voice_message_handler(message: Message):
    voice_message = message.attachments[0].audio_message

    if getattr(voice_message, "transcript", None): # При использвоании встроенного транскрипат в интерфейсе вк, хэндлер тоже это ловит. Поэтому, елси у сообщения уже есть транскрипт, бот его не обработает.
        return

    url = voice_message.link_ogg
    bot_msg = await message.reply("Принято в обработку...")

    audio_path = await download(url, message.from_id, message.id)
    if not audio_path:
        await bot.api.messages.edit(
            text = "Не удалось скачать голосовое сообщение.",
            peer_id = message.from_id,
            conversation_id = bot_msg.conversation.id)
        return

    loop = asyncio.get_running_loop()
    voice_message_text = await loop.run_in_executor(None, transcribe, audio_path) # (Whisper + Perplexity) выносим в executor, чтобы не блокировать event loop
    if os.path.exists(audio_path):
        os.remove(audio_path)

    if not voice_message_text:
        await bot.api.messages.edit(
            peer_id = message.peer_id,
            conversation_id = bot_msg.conversation.id,
            text = "Не удалось распознать голосовое.")
        return

    await bot.api.messages.delete(
        peer_id = message.peer_id,
        cmids = [bot_msg.conversation_message_id],
        delete_for_all = True
    )

    await message.reply(voice_message_text)


if __name__ == "__main__":
    try:
        bot.run_forever()
    finally:
        asyncio.run(close_session())
