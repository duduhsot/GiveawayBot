import re
from flask import Flask, request
import telegram

bot_token = "5726668567:AAEnt_hRMirItfq2Jrn-srH8OGRz_oVjNOI"
bot_user_name = "@omlenastrik_bot"
URL = "the heroku app link that we will create later"

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)

   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       response = """Welcome to RipYourAss bot!"""
       bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
   # displays commands
   if text == "/start":
       response = """I won't tell you anything!"""
       bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)