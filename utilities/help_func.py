from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.start_func import start as start_func
from utilities.context_helper import UserContext

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)

    if ctx.query:
        await ctx.query.answer()

    text = ctx.menu["help_text"]

    keyboard = [[InlineKeyboardButton("🟢 Start", callback_data="start")]]
    markup = InlineKeyboardMarkup(keyboard)

    if ctx.message:
        await ctx.message.reply_text(text, reply_markup=markup, parse_mode='HTML')
    elif ctx.query:
        await ctx.query.edit_message_text(text=text, reply_markup=markup, parse_mode='HTML')
