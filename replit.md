# Brawl Stars Code Generator Bot

## Overview

Telegram бот для генерации последовательных кодов команд Brawl Stars с настраиваемым смещением. Бот требует подписку на канал для использования.

## Recent Changes

- 2024-12-18: Создан проект с поддержкой деплоя на Railway
- Добавлен health check сервер для поддержания работы на Railway
- Настроена PostgreSQL база данных для логирования сообщений

## Project Architecture

### Файлы проекта

```
├── bot.py              # Основной файл Telegram бота
├── requirements.txt    # Python зависимости для Railway
├── Procfile            # Команда запуска для Railway
├── runtime.txt         # Версия Python
├── railway.json        # Конфигурация Railway
├── RAILWAY_DEPLOY.md   # Инструкция по деплою
└── .gitignore          # Игнорируемые файлы Git
```

### Функции бота

- Генерация последовательных кодов команд
- Проверка подписки на канал
- Выбор смещения (5, 10, 20, 50, 100 или произвольное)
- Поддержка прямых кодов и ссылок-приглашений
- Логирование сообщений в PostgreSQL

### База данных

**Таблица message_logs:**
- id (SERIAL PRIMARY KEY)
- user_id (BIGINT)
- username (VARCHAR)
- first_name (VARCHAR)
- message_text (TEXT)
- code_input (VARCHAR)
- created_at (TIMESTAMP)

## Environment Variables

| Переменная | Описание |
|------------|----------|
| TELEGRAM_BOT_TOKEN | Токен бота от @BotFather |
| DATABASE_URL | URL подключения к PostgreSQL |

## User Preferences

- Язык интерфейса: Русский
- Деплой: Railway

## Commands

- `/start` - Начать работу с ботом
- `/generate` - Сгенерировать коды
- `/offset` - Изменить смещение
- `/help` - Показать справку
- `/cancel` - Отменить операцию
