from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler, ConversationHandler

import logging
import telegramcalendar
import sqlite3

#FIRST, SECOND = range(2)

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
    text = 'Вас приветствует salon_bot!'
    my_keyboard = ReplyKeyboardMarkup([['Записаться на услугу'],
                                       ['Мои записи', 'О нас']],
                                        resize_keyboard=True)
    update.message.reply_text(text, reply_markup=my_keyboard)

# Функция choose_master для вывода инлайн клавы с мастерами

def choose_master(bot, update):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    sql = "SELECT barber_name FROM barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()
    all_masters = []
    for masters in data_base:
        all_masters.append(masters[0])
    keyboard = []
    row = []
    for i in all_masters:
        row.append(InlineKeyboardButton(i, callback_data=str(i)))
    keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)

#    bot.send_photo(chat_id=update.message.chat.id,
#                   photo=open('C:\projects\diplom\photo\Lex.jpg', 'rb'))

    update.message.reply_text(text='Выберите мастера:', reply_markup=reply_markup)


#inline_button_pressed - функция для вызова клавиатуры с услугами

def inline_button_pressed(bot, update):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    sql = "SELECT * FROM barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_1 = "SELECT * FROM barbers_to_services"
    cursor.execute(sql_1)
    data_base_1 = cursor.fetchall()

    sql_2 = "SELECT * FROM services"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    counter = []
    query = update.callback_query
    name = query.data
    for masters in data_base:
        if name in masters:
            a = masters[0]
            for master_id in data_base_1:
                if a in master_id:
                    b = master_id[2]
                    for service_id in data_base_2:
                        if b in service_id:
                            all_services = []
                            all_services.append(service_id[2])
                            counter = counter + all_services

    my_keyboard_1 = ReplyKeyboardMarkup([counter,
                                        ["Вернуться в меню"]],
                                        resize_keyboard=True)
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text="Please select a service: ",
                     reply_markup=my_keyboard_1)
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text="You selected %s" % (date.strftime("%d/%m/%Y")),
                         reply_markup=ReplyKeyboardMarkup([['10:00', '11:00'],
                                                           ['12:00', '13:00']],
                                                          resize_keyboard=True))

def date_select(bot, update):
    update.message.reply_text(text="Please select a date: ",
                              reply_markup=telegramcalendar.create_calendar())

def my_entry(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']],
                                      resize_keyboard=True)
    update.message.reply_text("Здесь появятся ваши записи",
                              reply_markup=my_keyboard)
def info(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']],
                                      resize_keyboard=True)
    update.message.reply_text("Здесь можно будет узнать информацию о нас",
                              reply_markup=my_keyboard)

if TOKEN == "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo":
    print("Please write TOKEN into file")
else:
    up = Updater("TOKEN")

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(CommandHandler("Записаться на услугу", choose_master))
    dp.add_handler(RegexHandler("Записаться на услугу", choose_master))

    dp.add_handler(CommandHandler("Стрижка машинкой", date_select))
    dp.add_handler(RegexHandler("Стрижка машинкой", date_select))
    dp.add_handler(CommandHandler("Стрижка модельная", date_select))
    dp.add_handler(RegexHandler("Стрижка модельная", date_select))
    dp.add_handler(CommandHandler("Стрижка бороды", date_select))
    dp.add_handler(RegexHandler("Стрижка бороды", date_select))
    dp.add_handler(CommandHandler("Опасное бритье", date_select))
    dp.add_handler(RegexHandler("Опасное бритье", date_select))
    dp.add_handler(CommandHandler("Стрижка усов", date_select))
    dp.add_handler(RegexHandler("Стрижка усов", date_select))
    dp.add_handler(CommandHandler("Моделирование бороды и усов", date_select))
    dp.add_handler(RegexHandler("Моделирование бороды и усов", date_select))
    dp.add_handler(CommandHandler("Укладка", date_select))
    dp.add_handler(RegexHandler("Укладка", date_select))
    dp.add_handler(CommandHandler("Маска для лица", date_select))
    dp.add_handler(RegexHandler("Маска для лица", date_select))

    dp.add_handler(CallbackQueryHandler(inline_button_pressed))

    dp.add_handler(CommandHandler("Мои записи", my_entry))
    dp.add_handler(RegexHandler("Мои записи", my_entry))
    dp.add_handler(CommandHandler("О нас", info))
    dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user))

#    dp.add_handler(ConversationHandler(
#            entry_points=[CommandHandler('start', greet_user)],
#            states={
#                FIRST: [CallbackQueryHandler(choose_master)],
#                SECOND: [CallbackQueryHandler(date_select)]
#            },
#            fallbacks=[CommandHandler('start', greet_user)]
#        ))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()
