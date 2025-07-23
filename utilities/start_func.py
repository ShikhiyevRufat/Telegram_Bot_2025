from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utilities.context_helper import UserContext
from telegram.ext import ContextTypes
from utilities.translations import translations
from utilities.language_func import user_language


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)
    await ctx.query.answer()
    
    keyboard = [
        [InlineKeyboardButton(ctx.menu["ai_tools"], callback_data='ai_tools')],
        [InlineKeyboardButton(ctx.menu["file_functions"], callback_data='file_functions')],
        [InlineKeyboardButton(ctx.menu["extra_features"], callback_data='extra_features')],
        [InlineKeyboardButton(ctx.menu["games"], callback_data='games')],
        [InlineKeyboardButton(ctx.menu["social_media"], callback_data='social_media')],
        [InlineKeyboardButton(ctx.menu["subscriptions"], callback_data='subscriptions')],
    ]

    markup = InlineKeyboardMarkup(keyboard)
    user_first_name = update.effective_user.first_name

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ctx.menu["welcome"].format(name=user_first_name),
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