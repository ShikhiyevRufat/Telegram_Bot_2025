import os
from io import BytesIO
from pyrogram import Client, filters
from telegram.ext import ContextTypes
from utilities.translations import translations
from utilities.language_func import user_language
from lib.font_functions.main_font import Main_Font
from lib.file_functions.qr_generate import qr_generate
from lib.file_functions.bg_remover import process_image
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
    user_id = update.effective_chat.id
    lang = user_language.get(user_id, "en")

    menu = translations[lang]
    query = update.callback_query
    await query.answer()

    if query.data == 'convert_image':
        user_state[query.from_user.id] = 'awaiting_image_upload'
        await query.edit_message_text(f"{menu["please_image_upload"]}")
    
    elif query.data == 'bg_remove':
        user_state[query.from_user.id] = 'bg_remove'
        await query.edit_message_text(f"{menu["please_image_upload"]}") 

    elif query.data == 'convert_document':
        user_state[query.from_user.id] = 'awaiting_document_upload'
        await query.edit_message_text(f"{menu["please_document_upload"]}")

    elif query.data == 'start':
        user_state[query.from_user.id] = 'starts'
        await start_func(update, context) 

    elif query.data == 'language':
        await lang_func(update, context)

    elif query.data == 'generate_qr':
        user_state[query.from_user.id] = 'awaiting_qr_input'
        await query.edit_message_text(f"{menu["please_enter_qr"]}")

    elif query.data == 'tiktok_download':
        user_state[query.from_user.id] = 'awaiting_tiktok_url'
        await query.edit_message_text(f"{menu["please_send_tiktok"]}")

    elif query.data == 'font_style':
        user_state[query.from_user.id] = 'font_style'
        await query.edit_message_text(f"{menu["pls_write_message"]}")    
    
    elif query.data.startswith('format_'):
        await handle_format_selection(update, context)

    elif query.data.startswith('lang_'):
        lang_code = query.data.split('_')[1]
        user_language[query.from_user.id] = lang_code
        await start_func(update, context)

    elif query.data.startswith('style+'):
        _, style = query.data.split('+')
        original_message = user_state.get(query.from_user.id)

        if original_message:
            styled_message = main_font.handle_style(style, original_message)
            await query.edit_message_text(styled_message)
            await query.message.reply_text(f"{menu["font_success"]}", reply_markup=success_start(update, context))
            del user_state[query.from_user.id]
        else:
            await query.edit_message_text("Please write a message first!",)

    else:
        await query.edit_message_text("This function is not available.")


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
    user_id = update.message.from_user.id 
    lang = user_language.get(user_id, "en")
    query = update.callback_query

    menu = translations[lang]

    if user_state.get(user_id) == 'languages':
        await lang_func(update, context)

    if user_state.get(user_id) == 'starts':
        await start_func(update, context)
    
    if user_state.get(user_id) == 'font_style':
        if update.message:  
            user_state[user_id] = update.message.text  
            await update.message.reply_text(
                "Choose your style, please:",
                reply_markup=main_font.generate_buttons()
            )
        else:
            await update.message.reply_text("Please send a valid message first.")

    if user_state.get(user_id) == 'awaiting_tiktok_url':
        url = update.message.text
        await update.message.reply_text(f"{menu["tiktok_download_video"]}")

        output_filename = 'tiktok_video.mp4'
        target_resolution = '720p'  

        try:
            download_tiktok(url, output_filename, target_resolution)
            with open(output_filename, 'rb') as video_file:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
            os.remove(output_filename)  
            await update.message.reply_text(f"{menu["download_success"]}",reply_markup=success_start(update, context))
        except Exception as e:
            await update.message.reply_text(f"{menu["error_video"]}",reply_markup=success_start(update, context))
        user_state[user_id] = None

    if user_state.get(user_id) == 'awaiting_qr_input':
        text = update.message.text
        try:
            qr_code = qr_generate(text)
            await update.message.reply_photo(photo=qr_code, caption=f"{menu["download_success"]}",reply_markup=success_start(update, context)) 
        except Exception as e:
            await update.message.reply_text(f"{menu["error_qr"]}",reply_markup=success_start(update, context))

    elif user_state.get(user_id) == 'bg_remove':
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            photo = await photo_file.download_as_bytearray()

            try:
                output_buffer = process_image(photo)

                await update.message.reply_document(document=output_buffer, caption=f"{menu["download_success"]}", filename="output_image.png", reply_markup=success_start(update, context))

            except Exception as e:
                await update.message.reply_text(f"{menu["error_image"]}")
        else:
            await update.message.reply_text(f"{menu["error_upload_image"]}")

    elif user_state.get(user_id) == 'awaiting_image_upload':
        if update.message.photo:
            photo_file = await update.message.photo[-1].get_file()
            photo = await photo_file.download_as_bytearray()

            user_images[user_id] = photo

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

            markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"{menu["choose_image_format"]}",
                reply_markup=markup
            )
            user_state[user_id] = 'awaiting_format_selection'
        else:
            await update.message.reply_text(f"{menu["error_upload_image"]}",reply_markup=success_start(update, context))

    if user_state.get(user_id) == 'awaiting_document_upload':
        if update.message.document:
            document_file = await update.message.document.get_file()
            document_bytes = await document_file.download_as_bytearray()

            user_documents[user_id] = document_bytes

            await update.message.reply_text(f"{menu['converting_document']}")

            try:
                input_file_path = 'uploaded_document' + os.path.splitext(update.message.document.file_name)[1]
                output_file_path = 'uploaded_document.pdf'

                with open(input_file_path, 'wb') as f:
                    f.write(user_documents[user_id])

                document_convertor(input_file_path, output_file_path)

                with open(output_file_path, 'rb') as pdf_file:
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=pdf_file)

                os.remove(input_file_path)
                os.remove(output_file_path)
                await update.message.reply_text(f"{menu['download_success']}", reply_markup=success_start(update, context))
            except FileNotFoundError:
                await update.message.reply_text(
                    f"{menu['error_format_document']}", reply_markup=success_start(update, context)
                )
            except Exception as e:
                await update.message.reply_text(f"{menu['error_document']}",reply_markup=success_start(update, context))

            user_state[user_id] = None
            user_documents.pop(user_id, None)
        else:
            await update.message.reply_text(f"{menu['error_upload_document']}",reply_markup=success_start(update, context))

async def handle_format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = user_language.get(user_id, "en")

    menu = translations[lang]

    if user_state.get(user_id) == 'awaiting_format_selection' and user_id in user_images:
        await query.edit_message_text(f"{menu["please_wait_image"]}")

        input_image = BytesIO(user_images[user_id])
        output_format = query.data.split('_')[1]
        output_image = BytesIO()
        error_message = convert_image(input_image, output_image, output_format)

        if error_message:
            await query.edit_message_text(f"Error: {error_message}")
        else:
            output_image.seek(0)
            await context.bot.send_document(chat_id=query.message.chat_id, document=output_image,
                                            filename=f"converted.{output_format}")
        await query.edit_message_text(f"{menu["download_success"]}",reply_markup=success_start(update, context))

        user_state[user_id] = None
        user_images.pop(user_id, None)

