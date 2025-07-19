from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.translations import translations
from utilities.language_func import user_language



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    lang = user_language.get(user_id, "en")

    menu = translations[lang]
    
    keyboard = [
        [InlineKeyboardButton(menu["ai_tools"], callback_data='ai_tools')],
        [InlineKeyboardButton(menu["file_functions"], callback_data='file_functions')],
        [InlineKeyboardButton(menu["extra_features"], callback_data='extra_features')],
        [InlineKeyboardButton(menu["games"], callback_data='games')],
        [InlineKeyboardButton(menu["social_media"], callback_data='social_media')],
        [InlineKeyboardButton(menu["subscriptions"], callback_data='subscriptions')],
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{menu["welcome"]}",
        reply_markup=markup,
        parse_mode='HTML',
        disable_web_page_preview=True  
    )
    

def success_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    user_id = None
    
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id

    if user_id is None:
        raise ValueError("Unable to determine user ID")

    lang = user_language.get(user_id, "en")
    menu = translations[lang]

    keyboard = [
        [
            InlineKeyboardButton(f"{menu['start']}", callback_data='start'),
            InlineKeyboardButton(f"{menu['language']}", callback_data='language'),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    return markup