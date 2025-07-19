from telegram import InlineKeyboardButton
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

    def file_functions():
        keyboard = [
            [InlineKeyboardButton("Image format convertor", callback_data='convert_image')],
            [InlineKeyboardButton("Document format convertor", callback_data='convert_document')],
        ]

        return keyboard