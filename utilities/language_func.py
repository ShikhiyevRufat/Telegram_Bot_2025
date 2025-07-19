from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


user_language = {}

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🇦🇿 Azərbaycan dili", callback_data='lang_az')],
        [InlineKeyboardButton("🇬🇧 English language", callback_data='lang_en')],
        [InlineKeyboardButton("🇷🇺 Русский язык", callback_data='lang_ru')],
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🌐 Zəhmət olmasa dil seçin / Пожалуйста, выберите язык / Please choose your language:",
        reply_markup=markup,
        parse_mode='Markdown',
        disable_web_page_preview=True  
    )
