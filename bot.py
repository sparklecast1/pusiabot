#!/usr/bin/python
# -*- coding: utf-8 -*-
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import apiai, json
from modules.fir import *
import random
#from modules.yandere import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("telegram.utils.promise").propagate = False

start = False

updater = Updater(token='717149910:AAE6DKzpY48z-rqWbC155N8r4I7lPJSRRms') # Токен API к Telegram
dispatcher = updater.dispatcher



# Обработка команд
def stopCommand(bot, update):
    print ('бот выключен')
    global start
    start = False
    bot.send_message(chat_id=update.message.chat_id, text='Пуся спит. Z-z...')

def startCommand(bot, update):
    print ('Бот включен')
    global start
    start = True
    personname = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text='Привет, '+str(personname)+'?')


def biteinfoCommand(bot, update):
    print ('укусить')
    global username
    bot.send_message(chat_id=update.message.chat_id, text='Вводите bite и имя пользователя без @')
    message = u"Получил сообщение: {}".format(unicode(update.message.text))

def jokeinfoCommand(bot, update):
    print ('шутка')
    global username
    bot.send_message(chat_id=update.message.chat_id, text='Вводите joke и имя пользователя без @')
    message = u"Получил сообщение: {}".format(unicode(update.message.text))


def textMessage(bot, update):

    request = apiai.ApiAI('dbf368ec6b8f4ef091b25376a8d4a7ff').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'cute_pusia_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял


    user = update.message.text.split( )
    if "bite" in update.message.text:
        message = u"Получил сообщение: {}".format(unicode(update.message.text))
        print message
        #user = update.message.text.split( )
        bot.send_message(chat_id=update.message.chat_id, text='Кусь @' + str(user[1]) + ' !! :333')
        
    if "joke" in update.message.text:
        message = u"Получил сообщение: {}".format(unicode(update.message.text))
        print message
        roll = random.randrange(1,4)
        print roll
        if roll == 1:
           bot.send_message(chat_id=update.message.chat_id, text='Братан, @' + str(user[1]) + ', ну ты в натуре лох')

        if roll == 2:
           bot.send_message(chat_id=update.message.chat_id, text='Я видела много тупых, но настолько тупых как @' + str(user[1]) + ', еще ни разу')

        if roll == 3:
           bot.send_message(chat_id=update.message.chat_id, text='Нахуй пошел отсюда, @' + str(user[1]) + ' !')

        if roll == 4:
           bot.send_message(chat_id=update.message.chat_id, text='Ебать ты тупой, @' + str(user[1]) + ' , просто эталонный дебил')


    if start:
        print('вхождение в условие старта')
        if response:
    	    print('вхождение в апи')
            bot.send_message(chat_id=update.message.chat_id, text=response)
        #если не понимает то отвечает подобное
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

    #roll = random.randrange(50)
    #print(number)

    #был функционал когда она случайно фыркала в чатике
    #if number == 25:
    #    bot.send_message(chat_id=update.message.chat_id, text='Фыр!')
    #else:
    #    bot.send_message(chat_id=update.message.chat_id, text='Фыр!')
    
    
    
    #debug 
    #print update.message.text
    message = u"Получил сообщение: {}".format(unicode(update.message.text))
    print message
    #debug




# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
stop_command_handler = CommandHandler('stop', stopCommand)
cute_command_handler = CommandHandler('cute', cuteCommand)
biteinfo_command_handler = CommandHandler('bite', biteinfoCommand)
#bite_command_handler = CommandHandler('bite', biteCommand)
#joke_command_handler = CommandHandler('joke', jokeCommand)
jokeinfo_command_handler = CommandHandler('joke', jokeinfoCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(stop_command_handler)
dispatcher.add_handler(cute_command_handler)
#dispatcher.add_handler(bite_command_handler)
dispatcher.add_handler(biteinfo_command_handler)
#dispatcher.add_handler(joke_command_handler)
dispatcher.add_handler(jokeinfo_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
