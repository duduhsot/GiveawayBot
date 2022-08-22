from telegram.bot import Bot
from telegram.update import Update
from giveaway import Giveaway

class ChatFunc(object):

    def __init__(self, bot :Bot):
        self.bot = bot

    def sendMessage(self, update :Update, message :str):
        self.bot.send_message(chat_id = update.effective_chat.id,
                        text = message)
                        
    def deleteOriginalMessage(self, update :Update):
        self.bot.deleteMessage(chat_id = update.message.chat_id,
                        message_id = update.message.message_id
                ) 

    def sendDontHavePermission(self, update :Update, giveaway :Giveaway):
        self.bot.sendMessage(chat_id= update.effective_chat.id,
            text="You do not have permission for this command!\nPlease contact %s." % giveaway.authorNick)