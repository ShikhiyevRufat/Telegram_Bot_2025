from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utilities.context_helper import UserContext

async def reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)

    keyboard = [
        ["📄 Botun funksiyaları", "💰 Premium necə alınır?"],
        ["🌐 Dili dəyişmək", "📞 Admin ilə əlaqə"]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=ctx.chat_id,
        text = "Alt düymələr özəlliyidə aktivləşdi",
        reply_markup=markup
    )
