from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.translations import translations
from utilities.language_func import user_language


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    lang = user_language.get(user_id, "en")

    menu = translations[lang]
    
    keyboard = [
        [InlineKeyboardButton(menu["convert_image"], callback_data='convert_image')],
        [InlineKeyboardButton(menu["convert_document"], callback_data='convert_document')],
        [InlineKeyboardButton(menu["generate_qr"], callback_data='generate_qr')],
        [InlineKeyboardButton(menu["tiktok_download"], callback_data='tiktok_download')],
        [InlineKeyboardButton(menu["font_style"], callback_data='font_style')],
        [InlineKeyboardButton(menu["bg_remove"], callback_data='bg_remove')],
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{menu["welcome"]}",
        reply_markup=markup,
        parse_mode='Markdown',
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