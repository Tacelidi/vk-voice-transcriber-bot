# VK Voice Transcriber Bot

VK-бот, который автоматически расшифровывает голосовые сообщения через Whisper, корректирует расшифровку по конетксту через Perplexity API

## Возможности

- Принимает голосовые сообщения в беседах ВКонтакте.
- Скачивает аудио и распознаёт речь через Whisper (GPU, CUDA).
- Дополнительно исправляет орфографию и артефакты распознавания с помощью Perplexity.

## Технологии

- [vkbottle](https://github.com/vkbottle/vkbottle) — VK Bot API
- [OpenAI Whisper](https://github.com/openai/whisper) — распознавание речи
- [Perplexity API](https://docs.perplexity.ai) — корректировка текста

## Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение и установить зависимости
3. Создать файл `.env` в корне проекта:
  TOKEN=vk_group_token_here
  PERPLEXITY_API_KEY=your_perplexity_key_here





