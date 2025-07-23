from telegram import InlineKeyboardButton

def back_button(label: str = "🔙 Geri", callback_data: str = "start"):
    return [[InlineKeyboardButton(label, callback_data=callback_data)]]
