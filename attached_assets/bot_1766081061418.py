#!/usr/bin/env python3
"""
Brawl Stars Код-Генератор - Telegram бот
Требуется подписка на канал @neighty_bs
"""

import logging
import os
import signal
import sys
import re
import psycopg2
from datetime import datetime

# Константы для конвертации
TEAM_CONVERSION_CHARS = "QWERTYUPASDFGHJKLZCVBNM23456789"
TEAM_TAG = "X"
CONVERSION_CHARS = "0289PYLQGRJCUV"
HASH_TAG = "#"

# Конфигурация канала для подписки
CHANNEL_USERNAME = "@neighty_bs"  # обязательно с @
CHANNEL_LINK = "https://t.me/neighty_bs"  # ссылка на канал для подписки

# Стандартные смещения для быстрого выбора
PREDEFINED_OFFSETS = [5, 10, 20, 50, 100]

def to_long(hi_int, lo_int):
    """Вспомогательная функция для конвертации двух целых чисел в long"""
    return (hi_int << 32) | (lo_int & 0xFFFFFFFF)

def to_long_s(hi_int, lo_int):
    """Вспомогательная функция для конвертации со знаком"""
    return (hi_int << 32) | lo_int

def convert(id_num, chars):
    """Преобразование числового ID в строку с использованием заданного набора символов"""
    result = ''
    length = len(chars)
    
    while id_num > 0:
        char_index = id_num % length
        result = chars[char_index] + result
        id_num -= char_index
        id_num //= length
    
    return result

def code_to_id(code):
    """Преобразование кода команды в числовой ID"""
    if not code or not code.startswith(TEAM_TAG):
        return -1
    
    code_substring = code[1:]
    if len(code_substring) < 1:
        return 0
    
    unk6 = 0
    unk7 = 0
    
    for char in code_substring:
        sub_str_idx = TEAM_CONVERSION_CHARS.find(char)
        
        if sub_str_idx <= -1:
            return -1
        
        unk12 = unk6 * len(TEAM_CONVERSION_CHARS) + sub_str_idx
        unk7 = (to_long(unk7, unk6) * len(TEAM_CONVERSION_CHARS) + sub_str_idx) >> 32
        unk6 = unk12
    
    if (unk6 & unk7) != -1:
        v13 = to_long_s(unk7, unk6) >> 8
        lo_int = v13 & 0x7FFFFFFF
        hi_int = unk6 & 0xFF
        return to_long(hi_int, lo_int)
    
    return -1

def id_to_code(id_num):
    """Преобразование числового ID в код команды"""
    hi_int = (id_num >> 32) & 0xFFFFFFFF
    lo_int = id_num & 0xFFFFFFFF
    
    if hi_int < 256:
        l = to_long((lo_int >> 24), hi_int | (lo_int << 8))
        res = convert(l, TEAM_CONVERSION_CHARS)
        return TEAM_TAG + res
    
    return None

def generate_hash_code(id_num):
    """Преобразование числового ID в хеш-код"""
    hi_int = id_num >> 32
    lo_int = id_num & 0xFFFFFFFF
    
    if hi_int < 256:
        l = to_long((lo_int >> 24), hi_int | (lo_int << 8))
        res = convert(l, CONVERSION_CHARS)
        return HASH_TAG + res
    
    return None

def is_valid_team_code(code):
    """Проверка валидности кода команды"""
    if not code:
        return False
    
    code = code.strip().upper()
    
    return (
        code.startswith(TEAM_TAG) and 
        len(code) >= 2 and 
        len(code) <= 9 and
        all(char in TEAM_CONVERSION_CHARS for char in code[1:])
    )

def extract_team_code_from_link(text):
    """
    Извлекает код команды из ссылки-приглашения Brawl Stars
    Поддерживает формат: https://link.brawlstars.com/invite/gameroom/en?tag=XWADUQNY
    """
    pattern = r'tag=([A-Za-z0-9]+)'
    match = re.search(pattern, text)
    if match:
        code = match.group(1).upper()
        if is_valid_team_code(code):
            return code
    return None

def generate_sequential_codes(base_code, offset=0, count=10):
    """Генерация последовательных кодов команд с настраиваемым смещением"""
    numeric_id = code_to_id(base_code)
    if numeric_id == -1:
        raise ValueError("Неверный код команды")
    
    # Добавляем смещение к базовому ID
    base_id_with_offset = numeric_id + offset
    
    codes = []
    for i in range(count):
        # Затем добавляем последовательные числа к этому смещенному ID
        current_id = base_id_with_offset + i
        new_team_code = id_to_code(current_id)
        hash_code = generate_hash_code(current_id)
        
        if new_team_code and hash_code:
            codes.append({
                'team_code': new_team_code,
                'hash_code': hash_code
            })
    
    return codes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Подключение к базе данных для логирования сообщений
def get_db_connection():
    """Создает подключение к базе данных PostgreSQL"""
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None

def log_message(user_id, username, first_name, message_text, code_input=None):
    """Записывает сообщение пользователя в базу данных"""
    try:
        conn = get_db_connection()
        if not conn:
            logger.error("Не удалось подключиться к базе данных для логирования")
            return False
        
        cursor = conn.cursor()
        query = """
            INSERT INTO message_logs (user_id, username, first_name, message_text, code_input)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, username, first_name, message_text, code_input))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Сообщение от пользователя {user_id} успешно записано в лог")
        return True
    except Exception as e:
        logger.error(f"Ошибка при логировании сообщения: {e}")
        return False

# Обработчики сигналов для корректного завершения
def signal_handler(sig, frame):
    print('\n💡 Бот остановлен (Ctrl+C)')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Основной код бота
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler
except ImportError:
    print("\n⚠️ Библиотека python-telegram-bot не установлена!")
    print("\nУстановите её командой:")
    print("pip install python-telegram-bot\n")
    sys.exit(1)

# Состояния для ConversationHandler
CHOOSE_OFFSET, ENTER_CODE = range(2)

# Проверка подписки на канал
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверяет, подписан ли пользователь на канал или имеет временный доступ"""
    # Проверяем флаг временного доступа
    if context.user_data.get('temp_access', False):
        logger.info(f"Пользователь {update.effective_user.id} имеет временный доступ")
        return True
        
    user_id = update.effective_user.id
    try:
        # Пытаемся получить информацию о пользователе в канале
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        
        # Получаем статус пользователя (с учетом разных версий API)
        if hasattr(chat_member, 'status'):
            # Старый формат API
            status = chat_member.status
        else:
            # Новый формат API (v20+)
            status = chat_member.status.value if hasattr(chat_member.status, 'value') else str(chat_member.status)
        
        # Подробное логирование для отладки
        logger.info(f"Статус пользователя {user_id} в канале {CHANNEL_USERNAME}: {status}")
        
        # Проверяем статус пользователя (с учетом разных форматов статусов)
        valid_statuses = ["member", "administrator", "creator", "MEMBER", "ADMINISTRATOR", "CREATOR"]
        is_member = status in valid_statuses
        
        return is_member
    except Exception as e:
        # Подробное логирование ошибки
        logger.error(f"Ошибка при проверке подписки для пользователя {user_id}: {e}")
        logger.error(f"Тип ошибки: {type(e).__name__}")
        
        # На всякий случай проверяем, не связана ли ошибка с отсутствием прав
        if "Chat not found" in str(e):
            logger.error(f"Ошибка: Канал {CHANNEL_USERNAME} не найден. Проверьте имя канала.")
        elif "bot is not a member" in str(e):
            logger.error(f"Ошибка: Бот не добавлен в канал {CHANNEL_USERNAME} как администратор.")
        
        return False

async def subscription_required(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение о необходимости подписки"""
    keyboard = [
        [InlineKeyboardButton("Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Я подписался ✅", callback_data="check_subscription")],
        [InlineKeyboardButton("Временный доступ", callback_data="temp_access")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ Для использования бота необходимо подписаться на наш канал!\n\n"
        f"Канал: {CHANNEL_LINK}\n\n"
        "После подписки нажмите кнопку «Я подписался ✅»\n\n"
        "Если возникают проблемы с проверкой подписки, можете использовать временный доступ.",
        reply_markup=reply_markup
    )

async def temporary_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Предоставляет временный доступ к боту"""
    query = update.callback_query
    await query.answer("Временный доступ предоставлен")
    
    # Устанавливаем флаг временного доступа
    context.user_data['temp_access'] = True
    
    await query.edit_message_text(
        "✅ Временный доступ предоставлен!\n\n"
        "Вы можете пользоваться всеми функциями бота, но рекомендуем подписаться на канал.\n\n"
        "Используйте /generate чтобы сгенерировать коды или просто отправьте код команды."
    )

async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие на кнопку проверки подписки"""
    query = update.callback_query
    await query.answer()
    
    is_subscribed = await check_subscription(update, context)
    
    if is_subscribed:
        await query.edit_message_text(
            "✅ Спасибо за подписку!\n\n"
            "Теперь вы можете пользоваться всеми функциями бота.\n\n"
            "Используйте /generate чтобы сгенерировать коды или просто отправьте код команды."
        )
    else:
        keyboard = [
            [InlineKeyboardButton("Подписаться на канал", url=CHANNEL_LINK)],
            [InlineKeyboardButton("Проверить снова", callback_data="check_subscription")],
            [InlineKeyboardButton("Временный доступ", callback_data="temp_access")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "❌ Вы не подписаны на наш канал!\n\n"
            f"Пожалуйста, подпишитесь: {CHANNEL_LINK}\n\n"
            "После подписки нажмите кнопку «Проверить снова»\n\n"
            "Если возникают проблемы с проверкой подписки, можете использовать временный доступ.",
            reply_markup=reply_markup
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start"""
    # Логируем команду start
    user = update.effective_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    log_message(user_id, username, first_name, "/start")
    
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    # Сохраняем временный доступ если он был предоставлен ранее
    temp_access = context.user_data.get('temp_access', False)
    
    # Сбрасываем данные пользователя при новом старте но сохраняем флаг временного доступа
    if context.user_data:
        context.user_data.clear()
    
    # Восстанавливаем флаг временного доступа
    if temp_access:
        context.user_data['temp_access'] = True
    
    # Устанавливаем смещение по умолчанию
    context.user_data['offset'] = 50
    
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n\n"
        f"Это бот для генерации кодов команд Brawl Stars с настраиваемым смещением.\n\n"
        f"Используйте /generate чтобы сгенерировать коды с выбранным смещением.\n"
        f"Используйте /offset чтобы изменить смещение (текущее: {context.user_data['offset']}).\n\n"
        f"/help - показать справку"
    )
    
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет справочное сообщение при команде /help"""
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    current_offset = context.user_data.get('offset', 50)
    
    await update.message.reply_text(
        "📌 *Как пользоваться ботом*\n\n"
        "1️⃣ Используйте /offset чтобы выбрать смещение для генерации\n"
        "2️⃣ Используйте /generate чтобы ввести код команды и сгенерировать новые коды\n"
        "3️⃣ Отправьте код прямо боту для быстрой генерации\n\n"
        "🔗 Поддерживаются прямые коды (XWADUQNY) и ссылки-приглашения\n"
        "   (https://link.brawlstars.com/invite/gameroom/en?tag=XWPVMTYM)\n\n"
        f"🔢 Текущее смещение: *{current_offset}*\n\n"
        "⚠️ Код должен быть валидным и начинаться с буквы X",
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

async def select_offset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /offset для выбора смещения"""
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    current_offset = context.user_data.get('offset', 50)
    
    # Создаем клавиатуру с предустановленными смещениями
    keyboard = []
    row = []
    
    for i, offset in enumerate(PREDEFINED_OFFSETS):
        row.append(InlineKeyboardButton(f"+{offset}", callback_data=f"offset:{offset}"))
        
        # По 3 кнопки в ряд
        if (i + 1) % 3 == 0 or i == len(PREDEFINED_OFFSETS) - 1:
            keyboard.append(row)
            row = []
    
    # Добавляем кнопку для ввода произвольного смещения
    keyboard.append([InlineKeyboardButton("Другое значение", callback_data="offset:custom")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔢 Выберите смещение для генерации кодов:\n\n"
        f"Текущее смещение: *{current_offset}*\n\n"
        "Выберите один из вариантов или введите своё значение:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return CHOOSE_OFFSET

async def process_offset_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает выбор смещения из меню"""
    query = update.callback_query
    await query.answer()
    
    choice = query.data.split(":", 1)[1]
    
    if choice == "custom":
        await query.edit_message_text(
            "🔢 Введите произвольное смещение (целое число):\n\n"
            "Например: 42"
        )
        return CHOOSE_OFFSET
    else:
        # Сохраняем выбранное смещение
        offset = int(choice)
        context.user_data['offset'] = offset
        
        await query.edit_message_text(
            f"✅ Установлено новое смещение: *{offset}*\n\n"
            f"Теперь используйте /generate чтобы ввести код команды или просто отправьте код боту.",
            parse_mode="Markdown"
        )
        
        return ConversationHandler.END

async def process_custom_offset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ввод произвольного смещения"""
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    try:
        offset = int(update.message.text.strip())
        
        # Проверяем, что смещение в разумных пределах
        if offset < 0 or offset > 10000:
            await update.message.reply_text(
                "⚠️ Смещение должно быть положительным числом не больше 10000.\n"
                "Введите другое значение или нажмите /cancel"
            )
            return CHOOSE_OFFSET
        
        # Сохраняем выбранное смещение
        context.user_data['offset'] = offset
        
        await update.message.reply_text(
            f"✅ Установлено новое смещение: *{offset}*\n\n"
            f"Теперь используйте /generate чтобы ввести код команды или просто отправьте код боту.",
            parse_mode="Markdown"
        )
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "⚠️ Пожалуйста, введите целое число.\n"
            "Например: 42\n\n"
            "Или нажмите /cancel чтобы отменить."
        )
        return CHOOSE_OFFSET

async def request_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрашивает код команды у пользователя"""
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    current_offset = context.user_data.get('offset', 50)
    
    await update.message.reply_text(
        f"📝 Введите код команды Brawl Stars\n\n"
        f"Текущее смещение: *{current_offset}*\n\n"
        "Принимаются:\n"
        "- Код команды (например, XWADUQNY)\n"
        "- Ссылка-приглашение",
        parse_mode="Markdown"
    )
    
    return ENTER_CODE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет текущую операцию"""
    await update.message.reply_text(
        "❌ Операция отменена."
    )
    
    return ConversationHandler.END

async def generate_codes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает ввод кода и генерирует новые коды"""
    # Проверяем подписку пользователя
    is_subscribed = await check_subscription(update, context)
    
    if not is_subscribed:
        return await subscription_required(update, context)
    
    text = update.message.text.strip()
    user = update.effective_user
    
    # Логируем сообщение пользователя
    user_id = user.id
    username = user.username
    first_name = user.first_name
    
    # Логируем входящее сообщение в базу данных
    log_message(user_id, username, first_name, text)
    
    # Проверяем, есть ли в сообщении ссылка-приглашение
    team_code = extract_team_code_from_link(text)
    
    # Если не нашли ссылку, пробуем обработать как прямой код
    if not team_code:
        team_code = text.upper()
    
    # Проверяем валидность кода
    if not is_valid_team_code(team_code):
        await update.message.reply_text(
            "⚠️ Неверный формат кода команды!\n\n"
            "Код должен начинаться с X и содержать символы из набора:\n"
            f"{TEAM_CONVERSION_CHARS}\n\n"
            "Пример: XWADUQNY"
        )
        return ConversationHandler.END
    
    # Получаем текущее смещение
    offset = context.user_data.get('offset', 50)
    
    try:
        # Генерируем коды с выбранным смещением
        codes = generate_sequential_codes(team_code, offset, 10)
        
        # Формируем сообщение с результатами
        result_message = f"🎮 *Сгенерированные коды* (смещение: +{offset})\n\n"
        
        for i, code_data in enumerate(codes, 1):
            result_message += f"{i}. `{code_data['team_code']}` ({code_data['hash_code']})\n"
        
        result_message += "\nℹ️ Коды можно скопировать нажатием на них."
        
        # Отправляем результаты
        await update.message.reply_text(
            result_message,
            parse_mode="Markdown"
        )
        
        # Логируем обработанный код в базу данных
        log_message(user_id, username, first_name, f"Сгенерированы коды (смещение: +{offset})", team_code)
        
    except ValueError as e:
        await update.message.reply_text(
            f"⚠️ Ошибка: {str(e)}\n\n"
            "Пожалуйста, проверьте код и попробуйте снова."
        )
    
    return ConversationHandler.END

async def direct_code_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает прямую отправку кода боту"""
    # Перенаправляем в основной обработчик генерации
    await generate_codes(update, context)

def main() -> None:
    """Запускает бота"""
    # Получаем токен из переменной окружения или запрашиваем у пользователя
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        token = input("Введите токен вашего Telegram бота: ")
        if not token:
            print("❌ Токен не указан. Завершение работы.")
            sys.exit(1)
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Обработчик разговора для выбора смещения
    offset_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("offset", select_offset)],
        states={
            CHOOSE_OFFSET: [
                CallbackQueryHandler(process_offset_choice, pattern="^offset:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_custom_offset),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Обработчик разговора для ввода кода
    code_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generate", request_code)],
        states={
            ENTER_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, generate_codes),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(offset_conv_handler)
    application.add_handler(code_conv_handler)
    
    # Обработчики для проверки подписки и временного доступа
    application.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_subscription$"))
    application.add_handler(CallbackQueryHandler(temporary_access, pattern="^temp_access$"))
    
    # Обработчик для прямого ввода кода
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE, 
        direct_code_handler
    ))
    
    # Запускаем бота
    print("🚀 Бот запущен!")
    print(f"Канал для подписки: {CHANNEL_USERNAME}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()