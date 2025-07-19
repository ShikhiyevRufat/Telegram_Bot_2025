import os
from io import BytesIO
from pyrogram import Client, filters
from telegram.ext import ContextTypes
from utilities.inline_keyboard_button import InlineKeyboard
from utilities.context_helper import UserContext
from utilities.language_func import user_language
from lib.extra_features.main_font import Main_Font
from lib.extra_features.qr_generate import qr_generate
from lib.extra_features.bg_remover import process_image
from utilities.language_func import language as lang_func
from lib.file_functions.image_convertor import convert_image
from lib.social_functions.tiktok_downloander import download_tiktok
from utilities.start_func import start as start_func, success_start
from lib.file_functions.document_convertor import document_convertor
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

user_state = {}
user_images = {}
user_youtube_urls = {}
user_documents = {}
user_credits = {}
INITIAL_CREDITS = 30

main_font = Main_Font()


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)
    await ctx.query.answer()

    if ctx.query.data == 'file_functions':
        user_state[ctx.query.from_user.id] = 'file_functions'

        keyboard = InlineKeyboard.file_functions()
        markup = InlineKeyboardMarkup(keyboard)

        await ctx.query.edit_message_text(
            text="Choose file function",
            reply_markup=markup
        )

    elif ctx.query.data == 'convert_image':
        user_state[ctx.query.from_user.id] = 'awaiting_image_upload'
        await ctx.query.edit_message_text(f"{ctx.menu["please_image_upload"]}")

    elif ctx.query.data == 'bg_remove':
        user_state[ctx.query.from_user.id] = 'bg_remove'
        await ctx.query.edit_message_text(f"{ctx.menu["please_image_upload"]}") 

    elif ctx.query.data == 'convert_document':
        user_state[ctx.query.from_user.id] = 'awaiting_document_upload'
        await ctx.query.edit_message_text(f"{ctx.menu["please_document_upload"]}")

    elif ctx.query.data == 'start':
        user_state[ctx.query.from_user.id] = 'starts'
        await start_func(update, context) 

    elif ctx.query.data == 'language':
        await lang_func(update, context)

    elif ctx.query.data == 'generate_qr':
        user_state[ctx.query.from_user.id] = 'awaiting_qr_input'
        await ctx.query.edit_message_text(f"{ctx.menu["please_enter_qr"]}")

    elif ctx.query.data == 'tiktok_download':
        user_state[ctx.query.from_user.id] = 'awaiting_tiktok_url'
        await ctx.query.edit_message_text(f"{ctx.menu["please_send_tiktok"]}")

    elif ctx.query.data == 'font_style':
        user_state[ctx.query.from_user.id] = 'font_style'
        await ctx.query.edit_message_text(f"{ctx.menu["pls_write_message"]}")    
    
    elif ctx.query.data.startswith('format_'):
        await handle_format_selection(update, context)

    elif ctx.query.data.startswith('lang_'):
        lang_code = ctx.query.data.split('_')[1]
        user_language[ctx.query.from_user.id] = lang_code

        await start_func(update, context)

    elif ctx.query.data.startswith('style+'):
        _, style = ctx.query.data.split('+')
        original_message = user_state.get(ctx.query.from_user.id)

        if original_message:
            styled_message = main_font.handle_style(style, original_message)
            await ctx.query.edit_message_text(styled_message)
            await ctx.query.message.reply_text(f"{ctx.menu["font_success"]}", reply_markup=success_start(update, context))
            del user_state[ctx.query.from_user.id]
        else:
            await ctx.query.edit_message_text("Please write a message first!",)

    else:
        await ctx.query.edit_message_text("This function is not available.")


@Client.on_callback_query(filters.regex('^style'))
async def apply_style(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in user_state:
        await callback_query.answer("Please send a message first!", show_alert=True)
        return

    _, style = callback_query.data.split('+')
    original_message = user_state[user_id]

    styled_message = main_font.handle_style(style, original_message)

    await callback_query.message.edit_text(
        styled_message,
        reply_markup=callback_query.message.reply_markup
    )

    del user_state[user_id]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)

    if ctx.query:
        await ctx.query.answer()

    if user_state.get(ctx.user_id) == 'languages':
        await lang_func(update, context)

    if user_state.get(ctx.user_id) == 'starts':
        await start_func(update, context)

    if user_state.get(ctx.user_id) == 'font_style':
        if update.message:  
            user_state[ctx.user_id] = update.message.text  
            await update.message.reply_text(
                "Choose your style, please:",
                reply_markup=main_font.generate_buttons()
            )
        else:
            await update.message.reply_text("Please send a valid message first.")

    if user_state.get(ctx.user_id) == 'awaiting_tiktok_url':
        url = update.message.text
        await update.message.reply_text(f"{ctx.menu["tiktok_download_video"]}")

        output_filename = 'tiktok_video.mp4'
        target_resolution = '720p'  

        try:
            download_tiktok(url, output_filename, target_resolution)
            with open(output_filename, 'rb') as video_file:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
            os.remove(output_filename)  
            await update.message.reply_text(f"{ctx.menu["download_success"]}",reply_markup=success_start(update, context))
        except Exception as e:
            await update.message.reply_text(f"{ctx.menu["error_video"]}",reply_markup=success_start(update, context))
        user_state[ctx.user_id] = None

    if user_state.get(ctx.user_id) == 'awaiting_qr_input':
        text = update.message.text
        try:
            qr_code = qr_generate(text)
            await update.message.reply_photo(photo=qr_code, caption=f"{ctx.menu["download_success"]}",reply_markup=success_start(update, context)) 
        except Exception as e:
            await update.message.reply_text(f"{ctx.menu["error_qr"]}",reply_markup=success_start(update, context))

    elif user_state.get(ctx.user_id) == 'bg_remove':
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            photo = await photo_file.download_as_bytearray()

            try:
                output_buffer = process_image(photo)

                await update.message.reply_document(document=output_buffer, caption=f"{ctx.menu["download_success"]}", filename="output_image.png", reply_markup=success_start(update, context))

            except Exception as e:
                await update.message.reply_text(f"{ctx.menu["error_image"]}")
        else:
            await update.message.reply_text(f"{ctx.menu["error_upload_image"]}")

    elif user_state.get(ctx.user_id) == 'awaiting_image_upload':
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            photo = await photo_file.download_as_bytearray()

            user_images[ctx.user_id] = photo

            keyboard = InlineKeyboard.image_format()

            markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"{ctx.menu["choose_image_format"]}",
                reply_markup=markup
            )
            user_state[ctx.user_id] = 'awaiting_format_selection'
        else:
            await update.message.reply_text(f"{ctx.menu["error_upload_image"]}",reply_markup=success_start(update, context))

    if user_state.get(ctx.user_id) == 'awaiting_document_upload':
        if update.message.document:
            document_file = await update.message.document.get_file()
            document_bytes = await document_file.download_as_bytearray()

            user_documents[ctx.user_id] = document_bytes

            await update.message.reply_text(f"{ctx.menu['converting_document']}")

            try:
                input_file_path = 'uploaded_document' + os.path.splitext(update.message.document.file_name)[1]
                output_file_path = 'uploaded_document.pdf'

                with open(input_file_path, 'wb') as f:
                    f.write(user_documents[ctx.user_id])

                document_convertor(input_file_path, output_file_path)

                with open(output_file_path, 'rb') as pdf_file:
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf_file)

                os.remove(input_file_path)
                os.remove(output_file_path)
                await update.message.reply_text(f"{ctx.menu['download_success']}", reply_markup=success_start(update, context))
            except FileNotFoundError:
                await update.message.reply_text(
                    f"{ctx.menu['error_format_document']}", reply_markup=success_start(update, context)
                )
            except Exception as e:
                await update.message.reply_text(f"{ctx.menu['error_document']}",reply_markup=success_start(update, context))

            user_state[ctx.user_id] = None
            user_documents.pop(ctx.user_id, None)
        else:
            await update.message.reply_text(f"{ctx.menu['error_upload_document']}",reply_markup=success_start(update, context))

async def handle_format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ctx = UserContext(update, context)
    await ctx.query.answer()

    if user_state.get(ctx.user_id) == 'awaiting_format_selection' and ctx.user_id in user_images:
        await ctx.query.edit_message_text(f"{ctx.menu["please_wait_image"]}")

        input_image = BytesIO(user_images[ctx.user_id])
        output_format = ctx.query.data.split('_')[1]
        output_image = BytesIO()
        error_message = convert_image(input_image, output_image, output_format)

        if error_message:
            await ctx.query.edit_message_text(f"Error: {error_message}")
        else:
            output_image.seek(0)
            await context.bot.send_document(chat_id=ctx.query.message.chat_id, document=output_image,
                                            filename=f"converted.{output_format}")
        await ctx.query.edit_message_text(f"{ctx.menu["download_success"]}",reply_markup=success_start(update, context))

        user_state[ctx.user_id] = None
        user_images.pop(ctx.user_id, None)


