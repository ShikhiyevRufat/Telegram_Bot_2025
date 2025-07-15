from lib.font_functions.font_style import Fonts
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
class Main_Font:
    def generate_buttons(self):
        buttons = [[
            InlineKeyboardButton('𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛', callback_data='style+typewriter'),
            InlineKeyboardButton('𝕆𝕦𝕥𝕝𝕚𝕟𝕖', callback_data='style+outline'),
            InlineKeyboardButton('𝐒𝐞𝐫𝐢𝐟', callback_data='style+serif'),
            ],[
            InlineKeyboardButton('𝑺𝒆𝒓𝒊𝒇', callback_data='style+bold_cool'),
            InlineKeyboardButton('𝑆𝑒𝑟𝑖𝑓', callback_data='style+cool'),
            InlineKeyboardButton('Sᴍᴀʟʟ Cᴀᴘs', callback_data='style+small_cap'),
            ],[
            InlineKeyboardButton('𝓈𝒸𝓇𝒾𝓅𝓉', callback_data='style+script'),
            InlineKeyboardButton('𝓼𝓬𝓻𝓲𝓹𝓽', callback_data='style+script_bolt'),
            InlineKeyboardButton('ᵗⁱⁿʸ', callback_data='style+tiny'),
            ],[
            InlineKeyboardButton('ᑕOᗰIᑕ', callback_data='style+comic'),
            InlineKeyboardButton('𝗦𝗮𝗻𝘀', callback_data='style+sans'),
            InlineKeyboardButton('𝙎𝙖𝙣𝙨', callback_data='style+slant_sans'),
            ],[
            InlineKeyboardButton('𝘚𝘢𝘯𝘴', callback_data='style+slant'),
            InlineKeyboardButton('𝖲𝖺𝗇𝗌', callback_data='style+sim'),
            InlineKeyboardButton('Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎', callback_data='style+circles'),
            ],[
            InlineKeyboardButton('🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎', callback_data='style+circle_dark'),
            InlineKeyboardButton('𝔊𝔬𝔱𝔥𝔦𝔠', callback_data='style+gothic'),
            InlineKeyboardButton('𝕲𝖔𝖙𝖍𝖎𝖈', callback_data='style+gothic_bolt'),
            ],[
            InlineKeyboardButton('C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡', callback_data='style+cloud'),
            InlineKeyboardButton('H̆̈ă̈p̆̈p̆̈y̆̈', callback_data='style+happy'),
            InlineKeyboardButton('S̑̈ȃ̈d̑̈', callback_data='style+sad'),
            ],[
                InlineKeyboardButton('🇸 🇵 🇪 🇨 🇮 🇦 🇱 ', callback_data='style+special'),
                InlineKeyboardButton('🅂🅀🅄🄰🅁🄴🅂', callback_data='style+squares'),
                InlineKeyboardButton('🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎', callback_data='style+squares_bold'),
                ],[
                InlineKeyboardButton('ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ', callback_data='style+andalucia'),
                InlineKeyboardButton('爪卂几ᘜ卂', callback_data='style+manga'),
                InlineKeyboardButton('S̾t̾i̾n̾k̾y̾', callback_data='style+stinky'),
                ],[
                InlineKeyboardButton('B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ', callback_data='style+bubbles'),
                InlineKeyboardButton('U͟n͟d͟e͟r͟l͟i͟n͟e͟', callback_data='style+underline'),
                InlineKeyboardButton('꒒ꍏꀷꌩꌃꀎꁅ', callback_data='style+ladybug'),
                ],[
                InlineKeyboardButton('R҉a҉y҉s҉', callback_data='style+rays'),
                InlineKeyboardButton('B҈i҈r҈d҈s҈', callback_data='style+birds'),
                InlineKeyboardButton('S̸l̸a̸s̸h̸', callback_data='style+slash'),
                ],[
                InlineKeyboardButton('s⃠t⃠o⃠p⃠', callback_data='style+stop'),
                InlineKeyboardButton('S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆', callback_data='style+skyline'),
                InlineKeyboardButton('A͎r͎r͎o͎w͎s͎', callback_data='style+arrows'),
                ],[
                InlineKeyboardButton('ዪሀክቿነ', callback_data='style+qvnes'),
                InlineKeyboardButton('S̶t̶r̶i̶k̶e̶', callback_data='style+strike'),
                InlineKeyboardButton('F༙r༙o༙z༙e༙n༙', callback_data='style+frozen')
                ]]
        return InlineKeyboardMarkup(buttons)

    def handle_style(self, style, text):
        style_map = {
        'typewriter': Fonts.typewriter,
        'outline': Fonts.outline,
        'serif': Fonts.serief,
        'bold_cool': Fonts.bold_cool,
        'cool': Fonts.cool,
        'small_cap': Fonts.smallcap,
        'script': Fonts.script,
        'script_bolt': Fonts.bold_script,
        'tiny': Fonts.tiny,
        'comic': Fonts.comic,
        'sans': Fonts.san,
        'slant_sans': Fonts.slant_san,
        'slant': Fonts.slant,
        'sim': Fonts.sim,
        'circles': Fonts.circles,
        'circle_dark': Fonts.dark_circle,
        'gothic': Fonts.gothic,
        'gothic_bolt': Fonts.bold_gothic,
        'cloud': Fonts.cloud,
        'happy': Fonts.happy,
        'sad': Fonts.sad,
        'special': Fonts.special,
        'squares': Fonts.square,
        'squares_bold': Fonts.dark_square,
        'andalucia': Fonts.andalucia,
        'manga': Fonts.manga,
        'stinky': Fonts.stinky,
        'bubbles': Fonts.bubbles,
        'underline': Fonts.underline,
        'ladybug': Fonts.ladybug,
        'rays': Fonts.rays,
        'birds': Fonts.birds,
        'slash': Fonts.slash,
        'stop': Fonts.stop,
        'skyline': Fonts.skyline,
        'arrows': Fonts.arrows,
        'qvnes': Fonts.rvnes,
        'strike': Fonts.strike,
        'frozen': Fonts.frozen,
    }
        cls = style_map.get(style)
        return cls(text) if cls else text