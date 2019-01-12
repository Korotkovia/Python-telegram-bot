from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler

import logging
import telegramcalendar
import sqlite3

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)

def talk_to_me(bot, update):
    update.message.reply_text('Приносим свои извинения! Бот находится в стадии разработки!')

def greet_user(bot, update):
    text = 'Приносим свои извинения! Бот находится в стадии разработки!'
    my_keyboard = ReplyKeyboardMarkup([['Записаться на услугу'],
                                       ['Мои записи', 'О нас']],
                                        resize_keyboard=True)
    update.message.reply_text(text, reply_markup=my_keyboard)

def services(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Услуга1', 'Выбор мастера'],
                                       ['Вернуться в главное меню']],
                                        resize_keyboard=True)
    update.message.reply_text("Здесь можно будет записаться на услугу", reply_markup=my_keyboard)

def date_select(bot, update):
    update.message.reply_text("Выберите дату:", reply_markup=telegramcalendar.create_calendar())

def time(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['10:00', '11:00', '12:00'],
                                       ['13:00', '14:00', '15:00']],
                                        resize_keyboard=True)
    update.message.reply_text("Выберите время:", reply_markup=my_keyboard)

def my_entry(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']], resize_keyboard=True)
    update.message.reply_text("Здесь появятся ваши записи", reply_markup=my_keyboard)
def info(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']], resize_keyboard=True)
    update.message.reply_text("Здесь можно будет узнать информацию о нас", reply_markup=my_keyboard)

def calendar_handler(bot, update):
    update.message.reply_text("Please select a date: ",
                        reply_markup=telegramcalendar.create_calendar())

def inline_handler(bot, update):
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text="You selected %s" % (date.strftime("%d/%m/%Y")),
                         reply_markup=ReplyKeyboardRemove())

if TOKEN == "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo":
    print("Please write TOKEN into file")
else:
    up = Updater("TOKEN")

def show_inline(bot, update):
    inlinekeyboard = [[InlineKeyboardButton("Выбрать мастера",
                                            callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(inlinekeyboard)
    bot.send_photo(chat_id=update.message.chat.id,
                   photo=open('C:\projects\diplom\photo\Lex.jpg', 'rb'))
    update.message.reply_text('Специалист Лекс', reply_markup=reply_markup)
def inline_button_pressed(bot, update):
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text="Лекс предлагает вам: %s" % result,
                     reply_markup=ReplyKeyboardRemove())

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()
sql = "SELECT * FROM barbershop"
cursor.execute(sql)
result = cursor.fetchall()

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(CommandHandler("Записаться на услугу", services))
    dp.add_handler(RegexHandler("Записаться на услугу", services))

    dp.add_handler(CommandHandler("Услуга1", date_select))
    dp.add_handler(RegexHandler("Услуга1", date_select))
    dp.add_handler(CommandHandler("Услуга1", time))
    dp.add_handler(RegexHandler("Услуга1", time))

    dp.add_handler(CommandHandler("Выбор мастера", show_inline))
    dp.add_handler(RegexHandler("Выбор мастера", show_inline))
    dp.add_handler(CallbackQueryHandler(inline_button_pressed))

    dp.add_handler(CommandHandler("Мои записи", my_entry))
    dp.add_handler(RegexHandler("Мои записи", my_entry))
    dp.add_handler(CommandHandler("О нас", info))
    dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user))

    dp.add_handler(CommandHandler("calendar", calendar_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
