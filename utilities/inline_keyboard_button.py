from telegram import InlineKeyboardButton
from utilities.translations import translations
from utilities.context_helper import UserContext
from utilities.back_button import back_button
from telegram import Update
from telegram.ext import ContextTypes

class InlineKeyboard:

    def image_format():
        keyboard = [
            [
                InlineKeyboardButton("PNG", callback_data='format_png'),
                InlineKeyboardButton("JPEG", callback_data='format_jpeg'),
                InlineKeyboardButton("GIF", callback_data='format_gif')
            ],
            [
                InlineKeyboardButton("TIFF", callback_data='format_tiff'),
                InlineKeyboardButton("PDF", callback_data='format_pdf'),
                InlineKeyboardButton("AVIF", callback_data='format_avif')
            ],
            [
                InlineKeyboardButton("WEBP", callback_data='format_webp')
            ]
        ]
        return keyboard

    async def file_functions(update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = UserContext(update, context)
        await ctx.query.answer()

        keyboard = [
            [InlineKeyboardButton(ctx.menu['convert_image'], callback_data='convert_image')],
            [InlineKeyboardButton(ctx.menu['convert_document'], callback_data='convert_document')],
            *back_button(label=ctx.menu['back_to_menu'], callback_data="start")
        ]

        return keyboard
    
    async def extra_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = UserContext(update, context)
        await ctx.query.answer()

        keyboard = [
            [InlineKeyboardButton(ctx.menu['bg_remove'], callback_data='bg_remove')],
            [InlineKeyboardButton(ctx.menu['generate_qr'], callback_data='generate_qr')],
            [InlineKeyboardButton(ctx.menu['font_style'], callback_data='font_style')],
            *back_button(label=ctx.menu['back_to_menu'], callback_data="start")

        ]

        return keyboard