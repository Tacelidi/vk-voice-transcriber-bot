from perplexity import Perplexity
from dotenv import load_dotenv
import logging

load_dotenv()
client = Perplexity()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def ai_rewrite(text: str) -> str:
    try:
        request = client.chat.completions.create(
            model = "sonar-pro",
            messages = [{"role": "system",
                         "content":"Вы — специалист по точной корректировке текста.Исправляйте ошибки распознавания по контексту, сохраняя язык, стиль и смысл. Исправляй орфографию и пунктуацию.Можно чуть переформулировать, если это нужно для грамотности, но НЕЛЬЗЯ добавлять новые факты, числа, бренды или технические детали. Если текст уже выглядит нормально, верни его без изменений."},
                        {"role": "user", "content": f"{text}"}],

            disable_search = True,  # Отключаем веб-поиск, чтобы модель работала только с переданным текстом.
            temperature = 0.1

        )

        res = request.choices[0].message.content.strip()
        return res
    except Exception as e:
        logger.exception(e)
        return text
