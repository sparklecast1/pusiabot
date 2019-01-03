#!/usr/bin/python
# -*- coding: utf-8 -*-
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
from modules.fir import *
#from modules.yandere import *

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
    bot.send_message(chat_id=update.message.chat_id, text='Привет?')


def textMessage(bot, update):

    request = apiai.ApiAI('dbf368ec6b8f4ef091b25376a8d4a7ff').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'cute_pusia_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if start:
        print('вхождение в условие старта')
        if response:
    	    print('вхождение в апи')
            bot.send_message(chat_id=update.message.chat_id, text=response)
        #если не понимает то отвечает подобное
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

    #number = random.randrange(50)
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
#pic_command_handler = CommandHandler('pic', picCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(stop_command_handler)
dispatcher.add_handler(cute_command_handler)
#dispatcher.add_handler(pic_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
