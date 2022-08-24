from ntpath import join
import os
import os.path
from pyclbr import Function
import sys
from typing import List
from uuid import uuid4
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.filters import Filters
from telegram.ext import CallbackQueryHandler
from telegram.parsemode import ParseMode
from config import HEROKU_APP, LOCAL, TOKEN
from giveaway import Giveaway
from log import Log
from userInfo import UserInfo
import pickle
from chatFunc import ChatFunc
from locals import get_line

PORT = os.getenv('PORT', default=8443)

SUBSCRIBE_KEYWORD = 'subscribe_'
UNSUBSCRIBE_KEYWORD = 'unsubscribe_'
GIVEAWAYS_PATH = './giveaways'
WEBHOOK_URL = "https://{0}.herokuapp.com/{1}".format(HEROKU_APP, TOKEN) 
langId = 1

updater = Updater(TOKEN, use_context=True)
bot = telegram.Bot(token=TOKEN)
chatFunc = ChatFunc(bot)
log = Log()

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def loadGiveaway(giveawayId:str) -> Giveaway:
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveawayId), 'rb') as giveaway_file:
        giveaway :Giveaway = pickle.load(giveaway_file)
        return giveaway

def saveGiveaway(giveaway :Giveaway):
    if not os.path.exists(GIVEAWAYS_PATH):
        os.mkdir(GIVEAWAYS_PATH)
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveaway.id), 'wb') as giveaway_file:
        pickle.dump(giveaway, giveaway_file)

def checkIfAuthor(giveaway :Giveaway, update :Update, doStuff: Function):
    if giveaway.is_Author(update.effective_user.id):
        doStuff(giveaway, update)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)

def makeGiveawayPost(giveaway:Giveaway, update:Update):
    button_s = [telegram.InlineKeyboardButton(
        text= get_line(langId, 'btn_sub_txt'), callback_data=SUBSCRIBE_KEYWORD + str(giveaway.id))]
    button_u = [telegram.InlineKeyboardButton(
        text= get_line(langId, 'btn_unsub_txt'), callback_data=UNSUBSCRIBE_KEYWORD + str(giveaway.id))]
    keyboard = telegram.InlineKeyboardMarkup([button_s, button_u])
    text = '<strong>{0}</strong>\n{1}'.format(giveaway.name, giveaway.description)
    if giveaway.photoId:
        bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = giveaway.photoId,
            caption = text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
    else:
        bot.send_message(
            chat_id = update.effective_chat.id,
            text = text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

def makeGiveawayEndPost(giveaway:Giveaway, update:Update, winners :str):
    text = get_line(langId, 'post_g_finished').format(giveaway.name, winners )
    if giveaway.photoId:
        bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = giveaway.photoId,
            caption = text,
            parse_mode=ParseMode.HTML,
        )
    else:
        bot.send_message(
            chat_id = update.effective_chat.id,
            text = text,
            parse_mode=ParseMode.HTML,
        )

def checkGiveawayId(update :Update,giveawayId :str):
    # check params are correct
    if not giveawayId:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_id'))
        return False
    if not giveawayExists(giveawayId):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_exists') % giveawayId)
        return False
    return True

def giveawayExists(guid :str):
    return os.path.exists(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % guid))

# /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(get_line(langId, 'cmd_start'))

# /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text(get_line(langId, 'cmd_help'))

# /restart
def restart(update: Update, context: CallbackContext):
    if not LOCAL: 
        return
    bot.sendMessage(chat_id=update.effective_chat.id,
                    text= get_line(langId, 'cmd_restart'))
    chatFunc.deleteOriginalMessage(update) 
    restart_program()

# /gc
def giveaway_createHandler(update: Update, cb: CallbackContext):
    log.info('processing command "{0}"'.format(update.message.text))
    giveaway_create(update, update.effective_message.text)

# creates a new giveaway and a post about it
def giveaway_create(update :Update,command: str, photo_id :str = None):
    log.info('processing command "{0}"'.format(command))
    giveawayInfo = command.replace('/g_create', '').strip().split("''")
    # check params are correct
    if len(giveawayInfo) != 3:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_wr_create_params') % len(giveawayInfo))
        return
    if not giveawayInfo[1]:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_name'))
        return
    if not giveawayInfo[2]:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_descr'))
        return
    if (not giveawayInfo[0]) | (not giveawayInfo[0].isdigit()):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_NoW'))
        return
    if int(giveawayInfo[0]) < 1:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_wr_g_NoW'))
        return


    newGiveaway = Giveaway(
        author = update.effective_user.id,
        authorNick = update.effective_user.name,
        name = giveawayInfo[1],
        description = giveawayInfo[2],
        NumberOfWinners = int(giveawayInfo[0]),
        id = uuid4(),
        subscribers = [],
        ended = False,
        winners = [],
        photoId = photo_id
    )
    saveGiveaway(newGiveaway)

    makeGiveawayPost(newGiveaway, update)
    bot.sendMessage(chat_id=newGiveaway.author,
                    text= get_line(langId, 'msg_g_created').
                    format(newGiveaway.id, update.effective_chat.id,newGiveaway.numberOfWinners,newGiveaway.name,newGiveaway.description))
    chatFunc.deleteOriginalMessage(update) 

# /gp
def giveaway_post(update: Update, cb : CallbackContext):
    log.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_post', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    checkIfAuthor(giveaway, update, makeGiveawayPost)
    bot.sendMessage(chat_id= giveaway.author,
                    text= get_line(langId, 'msg_g_post_created').
                    format(giveaway.id, update.effective_chat.id))
    chatFunc.deleteOriginalMessage(update) 

# /gs
def giveaway_subs(update: Update, cb : CallbackContext):
    log.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_subs', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    if update.effective_user.id == giveaway.author:
        subs = [sub.name for sub in giveaway.subscribers]
        subsDsc = get_line(langId, 'cmd_giveaway_subs').format(str(len(subs)), '\n'.join(subs))
        bot.send_message(chat_id = update.effective_chat.id,
                        text = subsDsc)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)
    chatFunc.deleteOriginalMessage(update) 

# /gf
def giveaway_finish(update :Update, cb :CallbackContext):
    log.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_finish', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    if update.effective_user.id == giveaway.author:
        winners = giveaway.getWinners()
        makeGiveawayEndPost(giveaway, update, winners)
        saveGiveaway(giveaway)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)
    chatFunc.deleteOriginalMessage(update) 

# /ge
def giveaway_editHandler(update :Update, cb :CallbackContext):
    log.info('processing command "{0}"'.format(update.message.text))
    giveaway_edit(update, update.effective_message.text)

def giveaway_edit(update :Update, command :str, photo_id :str = None):
    log.info('processing command "{0}"'.format(command))
    giveawayInfo = command.replace('/g_edit', '').strip().split("''")
    # check params are correct
    if len(giveawayInfo) != 4:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_wr_edit_params') % len(giveawayInfo))
        return
    giveawayId = giveawayInfo[0]
    newNoW = giveawayInfo[1]
    newName = giveawayInfo[2]
    newDescription = giveawayInfo[3]
    if not checkGiveawayId(update, giveawayId): 
        return
    if not newName:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_name'))
        return
    if not newDescription:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_descr'))
        return
    if (not newNoW) | (not newNoW.isdigit()):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_no_g_NoW'))
        return
    if int(newNoW) < 1:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text= get_line(langId, 'err_wr_g_NoW'))
        return

    giveaway = loadGiveaway(giveawayId)
    giveaway.name = newName
    giveaway.description = newDescription
    giveaway.numberOfWinners = int(newNoW)
    giveaway.photoId = photo_id
    saveGiveaway(giveaway)
    makeGiveawayPost(giveaway, update)

# handles messages with photos
def photoHandler(update: Update, cb: CallbackContext):
    log.info('processing photo with caption "{0}"'.format(update.effective_message.caption))
    message = update.effective_message
    text = message.caption
    photoId = message.photo[0].file_id
    print(str(len(message.photo)))
    print([x.file_id for x in message.photo])
    print([x.file_size for x in message.photo])
    if (bool(text)) and (text.startswith('/g_create')):
        giveaway_create(update, message.caption, photoId)
    if (bool(text)) and (text.startswith('/g_edit')):
        giveaway_edit(update, message.caption, photoId)

def callback_query_handler(update: Update, context: CallbackContext):
    update.callback_query.answer()
    log.info('processing callback "{0}"'.format(update.callback_query.data))
    callbackData = update.callback_query.data
    if callbackData.startswith(SUBSCRIBE_KEYWORD):
        giveawayId = callbackData.replace(SUBSCRIBE_KEYWORD, '')
        giveaway = loadGiveaway(giveawayId)
        user = UserInfo(update)
        if not giveaway.containsUser(user):
            giveaway.subscribers.append(user)
            saveGiveaway(giveaway)
            # bot.sendMessage(chat_id=update.effective_chat.id,
            #                 text='%s has been added to the giveaway subscribers' % update.effective_user.name)
        # else:
            # bot.sendMessage(chat_id=update.effective_chat.id,
            #                 text='%s is already subscribed to the giveaway' % update.effective_user.name)
        return
    if callbackData.startswith(UNSUBSCRIBE_KEYWORD):
        giveawayId = callbackData.replace(UNSUBSCRIBE_KEYWORD, '')
        giveaway = loadGiveaway(giveawayId)
        user = UserInfo(update)
        sameUser = user.findSame(giveaway.subscribers)
        if sameUser:
            giveaway.subscribers.remove(sameUser)
            saveGiveaway(giveaway)
            # bot.sendMessage(chat_id=update.effective_chat.id,
            #                 text='%s has been unsubscribed from the giveaway' % update.effective_user.name)
        # else:
            # bot.sendMessage(chat_id=update.effective_chat.id,
            #                 text='%s is not in the giveaway' % update.effective_user.name)
        return
    if callbackData.startswith('EDIT '):
        giveawayId = callbackData.replace('EDIT ', '')
        giveaway = loadGiveaway(giveawayId)
        return

# inDev
def inDev(update: Update, context: CallbackContext):
    update.message.reply_text(
        "In development")

def tst(update: Update, context: CallbackContext):

    # get all giveaways names
    giveaway_files = [f for f in os.listdir(GIVEAWAYS_PATH) if os.path.isfile(
        os.path.join(GIVEAWAYS_PATH, f)) and f.startswith('g_') and f.endswith('.pkl')]
    
    user_giveaways :List[Giveaway] = [] 
    for f in giveaway_files:
        giveaway_id = f.replace('g_', '').replace('.pkl', '')
        giveaway = loadGiveaway(giveaway_id)
        if giveaway.is_Author(update.effective_user.id):
            user_giveaways.append(giveaway)
    
    message = "Твои конкурсы:\n{0}\n\nКакой конкурс ты хочешь изменить?".format(
        '\n'.join(map(lambda x: '    %s - %s' % (x.name, str(x.id)), user_giveaways))
    )
    keyboard = [['/g_edit %s' % str(x.id)] for x in user_giveaways]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    
    message = "Какой конкурс ты хочешь изменить?"
    buttons = [[telegram.InlineKeyboardButton(
        text= '%s' % x.name, callback_data= 'EDIT ' + str(x.id))] for x in user_giveaways ]
    reply_markup = telegram.InlineKeyboardMarkup(buttons)
    update.message.reply_text(message, reply_markup=reply_markup)


updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(callback_query_handler)],
        states={
            1: [MessageHandler(Filters.text, name_input_by_user)],
            2: [CallbackQueryHandler(button_click_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True
    ))
updater.dispatcher.add_handler(CommandHandler('tst', tst))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('restart', restart))
# create new giveaway with Description, Number of winners
# /g_create NoW''Name''Description
# /g_create 3''Annual Giveaway #3''This time we will giveaway 3 new skins to the members of community!\nAll you have to do is to press 'subscribe' button just below the post
updater.dispatcher.add_handler(CommandHandler('g_create', giveaway_createHandler)) 
# [author only] creates new giveaway post
# /g_post giveawayId
# /g_post 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_post', giveaway_post)) 
# [author only] shows number and nicknames of giveaway subs 
# /g_subs giveawayID
# /g_subs 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_subs', giveaway_subs))
# [author only] change Description, Number of winners
# /g_edit giveawayID''NoW''Name''Description   
# /g_edit 41cce09e-10b3-4cb2-9228-52d4d872eabc''3''Annual Giveaway #3''This time we will giveaway 3 new skins to the members of community!\nAll you have to do is to press 'subscribe' button just below the post
updater.dispatcher.add_handler(CommandHandler('g_edit', giveaway_editHandler))
# [author only] ends a giveaway if needed; sends a post about winners
# /g_finish giveawayID
# /g_finish 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_finish', giveaway_finish)) 
# /run_test
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photoHandler)) 
# processes buttons requests
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

if LOCAL:
    log.info('polling messages...')
    updater.start_polling()
else:
    log.info('setting webhook on "{0}" listening on address "{1}:{2}"...'.
                format(WEBHOOK_URL, "0.0.0.0", PORT))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=WEBHOOK_URL)
    updater.bot.set_webhook(WEBHOOK_URL)
    bot.set_webhook(WEBHOOK_URL)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
