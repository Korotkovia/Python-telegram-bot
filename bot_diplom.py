from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

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
    text = 'Вас приветствует salon_bot!'
    my_keyboard = ReplyKeyboardMarkup([['Запись'],
                                       ['Мои записи', 'О нас']],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
    update.message.reply_text(text,
                              reply_markup=my_keyboard)


def choose_master(bot, update, user_data):
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

    update.message.reply_text(text='Выберите мастера:',
                              reply_markup=reply_markup)


def inline_button_pressed(bot, update, user_data):
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

    query = update.callback_query
    name = query.data

    counter = []
    if name == query.data:
        global c
        c = query.data
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
                                keyboard = []
                                row = []
                                for i in all_services:
                                    row.append(InlineKeyboardButton(i, callback_data=str(i)))
                                counter = row + counter
                                list_1 = []
                                list_1.append(counter)
                                reply_markup = InlineKeyboardMarkup(list_1)

                            # bot.send_message(chat_id=update.callback_query.from_user.id,
                            #                  text="Выберите услугу:",
                            #                  reply_markup=reply_markup)

                                bot.edit_message_text(text='Выберите услугу:',
                                                      chat_id=update.callback_query.from_user.id,
                                                      message_id=query.message.message_id,
                                                      reply_markup=reply_markup)

    sql_3 = "SELECT service_name FROM services"
    cursor.execute(sql_3)
    data_base_3 = cursor.fetchall()
    for z in data_base_3:
        if query.data == z[0]:
            bot.edit_message_text(text='Выберите дату:',
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  reply_markup=telegramcalendar.create_calendar())
            global e
            e = query.data
            print(e)

    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        bot.edit_message_text(text="Вы выбрали дату: %s" % (date.strftime("%d/%m/%Y")),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,)
                              # reply_markup=telegramcalendar.create_calendar())


        # bot.send_message(chat_id=update.callback_query.from_user.id,
        #                  text="Вы выбрали дату: %s" % (date.strftime("%d/%m/%Y")),)
        #                  # reply_markup=reply_markup)
        global f
        f = query.data
        print(f)

    if len(query.data) == 13:
        inline_keyboard = [[InlineKeyboardButton('10:00', callback_data='10:00'),
                            InlineKeyboardButton('11:00', callback_data='11:00')],
                           [InlineKeyboardButton('12:00', callback_data='12:00'),
                            InlineKeyboardButton('13:00', callback_data='13:00')],
                           [InlineKeyboardButton('14:00', callback_data='14:00'),
                            InlineKeyboardButton('15:00', callback_data='15:00')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # bot.send_message(chat_id=update.callback_query.from_user.id,
        #                  text="Выберите время:",
        #                  reply_markup=reply_markup)
        bot.edit_message_text(text='Выберите время:',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)

    print(c, e, f)


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


# if TOKEN == "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo":
#     print("Please write TOKEN into file")
# else:
#     up = Updater("TOKEN")


def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(CommandHandler("Запись", choose_master, pass_user_data=True))
    dp.add_handler(RegexHandler("Запись", choose_master, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(inline_button_pressed, pass_user_data=True))

    dp.add_handler(CommandHandler("Мои записи", my_entry))
    dp.add_handler(RegexHandler("Мои записи", my_entry))
    dp.add_handler(CommandHandler("О нас", info))
    dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()
