import aiohttp
import os
import aiofiles
import whisper
import torch
import logging
from contextual_corrections import ai_rewrite

session: aiohttp.ClientSession | None = None

device = "cuda" if torch.cuda.is_available() else "cpu" # Если GPU недоступен, Whisper будет запущен на CPU
# Модель можно менять в зависимости от железа.
# "medium" — хороший баланс качества и скорости (на RTX 2060 Super работает без проблем).
model_name = 'medium'
model = whisper.load_model(model_name, device = device)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info(f"Model loaded: {device}")


async def download(url, user_id, message_id):
    folder = os.path.join("AM", f"voice{user_id}")
    os.makedirs(folder, exist_ok = True)

    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession()

    try:
        async with session.get(url) as response:
            content = await response.read()
        path = os.path.join(folder, f"audio{message_id}.ogg")
        async with aiofiles.open(path, "wb") as f:
            await f.write(content)
        return path

    except Exception as e:
        logger.exception(f"Не удалось скачать файл:{e}")
        return None


def transcribe(path):
    try:
        result = model.transcribe(audio = path, language = "ru")
        return ai_rewrite(result.get("text", "").strip())
    except Exception as e:
        logger.exception(f"Ошибка при транскрипции:{e}")
        return None

async def close_session():
    global session
    if session and not session.closed:
        await session.close()
        session = None
