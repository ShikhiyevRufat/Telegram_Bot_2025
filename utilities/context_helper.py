from utilities.translations import translations
from utilities.language_func import user_language


class UserContext:
    def __init__(self, update, context):
        self.update = update
        self.context = context

        self.query = getattr(update, 'callback_query', None)
        self.message = getattr(update, 'message', None)

        if update.callback_query:
            self.query = update.callback_query
            self.user_id = self.query.from_user.id
            self.chat_id = self.query.message.chat_id
        elif self.message:
            self.user_id = self.message.from_user.id
            self.chat_id = self.message.chat_id
        else:
            self.query = None
            self.user_id = update.effective_user.id
            self.chat_id = update.effective_chat.id

        self.lang = user_language.get(self.user_id, "en")
        self.menu = translations[self.lang]
