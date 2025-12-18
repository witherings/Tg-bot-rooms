# Brawl Stars Code Generator Bot

## Overview

Telegram бот для генерации последовательных кодов команд Brawl Stars с настраиваемым смещением. Бот требует подписку на канал для использования.

## Recent Changes

- 2024-12-18: Создан проект с поддержкой деплоя на Railway
- Добавлен health check сервер для поддержания работы на Railway
- Настроена PostgreSQL база данных для логирования сообщений
- Добавлена обработка ошибок конфликта при работе нескольких инстансов
- Бот готов к деплою на Railway (используется режим Polling для локального тестирования)

## Project Architecture

### Файлы проекта

```
├── bot.py                      # Основной файл Telegram бота
├── requirements.txt            # Python зависимости для Railway
├── Procfile                    # Команда запуска для Railway (web dyno)
├── runtime.txt                 # Версия Python (3.11.13)
├── railway.json                # Конфигурация Railway
├── RAILWAY_DEPLOY.md           # Базовая инструкция по деплою
├── RAILWAY_DEPLOY_SETUP.md     # Подробная инструкция по деплою
└── .gitignore                  # Игнорируемые файлы Git
```

### Функции бота

- ✅ Генерация последовательных кодов команд с настраиваемым смещением
- ✅ Проверка подписки на канал @neighty_bs
- ✅ Выбор смещения (5, 10, 20, 50, 100 или произвольное значение)
- ✅ Поддержка прямых кодов (XWADUQNY) и ссылок-приглашений
- ✅ Логирование всех сообщений пользователей в PostgreSQL
- ✅ Временный доступ для пользователей без подписки
- ✅ Health check endpoints для Railway

### База данных

**Таблица message_logs:**
- id (SERIAL PRIMARY KEY)
- user_id (BIGINT) - ID пользователя Telegram
- username (VARCHAR) - Имя пользователя в Telegram
- first_name (VARCHAR) - Имя пользователя
- message_text (TEXT) - Текст сообщения
- code_input (VARCHAR) - Введенный код команды
- created_at (TIMESTAMP) - Время создания записи

## Deployment

### Для Railway

1. Загрузите код в GitHub
2. Создайте новый проект на railway.app
3. Подключите GitHub репозиторий
4. Добавьте PostgreSQL базу данных
5. Установите `TELEGRAM_BOT_TOKEN` переменную
6. **Важно:** Установите replicas = 1 (один инстанс) чтобы избежать конфликтов

Полную инструкцию см. в `RAILWAY_DEPLOY_SETUP.md`

## Environment Variables

| Переменная | Описание | Обязательна |
|------------|----------|-----------|
| TELEGRAM_BOT_TOKEN | Токен бота от @BotFather | Да |
| DATABASE_URL | URL подключения к PostgreSQL (Railway) | Да (Railway) |
| PORT | Порт для Flask сервера | Нет (по умолчанию 8080) |

## User Preferences

- Язык интерфейса: Русский
- Канал для подписки: @neighty_bs
- Деплой: Railway

## Bot Commands

- `/start` - Начать работу с ботом, показать приветственное сообщение
- `/generate` - Начать генерацию кодов (запросить ввод кода)
- `/offset` - Изменить смещение для генерации
- `/help` - Показать справку по использованию
- `/cancel` - Отменить текущую операцию

## Troubleshooting

### Ошибка "Conflict: terminated by other getUpdates request"

**Причина:** На Railway запущено несколько инстансов бота с одним токеном

**Решение:** 
- В Railway Dashboard установите replicas = 1
- Убедитесь что только один worker процесс запущен
- Перезапустите deploy

### Бот не отвечает на сообщения

**Проверьте:**
1. Установлен ли TELEGRAM_BOT_TOKEN правильно (без пробелов)
2. Подписаны ли вы на канал @neighty_bs
3. Логи бота в Railway Dashboard на наличие ошибок

### Ошибка подключения к базе данных

**Решение:**
1. Убедитесь что PostgreSQL база данных создана в Railway
2. DATABASE_URL переменная установлена правильно
3. Перезапустите deploy

## Development

### Локальный запуск

1. Установите зависимости: `pip install -r requirements.txt`
2. Установите TELEGRAM_BOT_TOKEN: `export TELEGRAM_BOT_TOKEN="ваш_токен"`
3. Запустите бота: `python bot.py`

### Тестирование

Откройте Telegram и найдите вашего бота по username (указали при создании в @BotFather)

## Code Structure

- **Код конвертации:** Функции `code_to_id()`, `id_to_code()`, `generate_hash_code()` для преобразования кодов Brawl Stars
- **Проверка подписки:** Функция `check_subscription()` проверяет наличие пользователя в канале
- **Логирование:** Функция `log_message()` сохраняет информацию в PostgreSQL
- **Обработчики:** ConversationHandler для управления многошаговыми диалогами с пользователем
