from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters,\
    RegexHandler

import logging
import telegramcalendar
import sqlite3

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"


FIRST, SECOND, THIRD, FOUR = range(4)

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)


def greet_user(bot, update):
    # функция - /start
    text = 'Вас приветствует salon_service_bot!'
    my_keyboard = ReplyKeyboardMarkup([['Запись'],
                                       ['Мои записи', 'О нас']],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=my_keyboard)


def choose_master(bot, update):
    # функция вызова инлайн клавиатуры с мастерами
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
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\BRB 666.jpg', 'rb'))
    update.message.reply_text('Выберите мастера:', reply_markup=reply_markup)
    return FIRST


def choose_service(bot, update):
    # функция вызова инлайн клавиатуры с услугами
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
    # Клавиатура с услугами
    counter = []
    for masters in data_base:
        if name in masters:
            global c
            c = query.data
            a = masters[0]
            for master_id in data_base_1:
                if a in master_id:
                    b = master_id[2]
                    for service_id in data_base_2:
                        if b in service_id:
                            all_services = []
                            all_services.append(service_id[2])
                            row = []
                            for i in all_services:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            counter = row + counter
    list_1 = []
    list_1.append(counter)
    reply_markup = InlineKeyboardMarkup(list_1)

    bot.edit_message_text(text='Выберите услугу:',
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    return SECOND


def calendar(bot, update):
    # функция вызова календаря
    query = update.callback_query
    bot.edit_message_text(text='Выберите дату:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=telegramcalendar.create_calendar())
    return THIRD


def time(bot, update):
    # функция вызова инлайн клавиатуры с временем
    query = update.callback_query
    selected, date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        inline_keyboard = [[InlineKeyboardButton('10:00', callback_data='10:00'),
                            InlineKeyboardButton('11:00', callback_data='11:00')],
                           [InlineKeyboardButton('12:00', callback_data='12:00'),
                            InlineKeyboardButton('13:00', callback_data='13:00')],
                           [InlineKeyboardButton('14:00', callback_data='14:00'),
                            InlineKeyboardButton('15:00', callback_data='15:00')]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        bot.edit_message_text(text='Выберите время:',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)
    return FOUR


def contact(bot, update):
    # функция вызова запроса контактов
    query = update.callback_query
    print(query.data)
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    my_keyboard = ReplyKeyboardMarkup([[contact_button]],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text="Отправьте Ваши контактные данные для уточнения заказа:",
                     reply_markup=my_keyboard)
    bot.delete_message(chat_id=update.callback_query.from_user.id,
                       message_id=query.message.message_id)


def get_contact(bot, update, user_data):
    # функция обработчик контактов
    a = str(update.message.contact)
    phone = a[18:30]
    user_data['phone'] = phone
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']],
                                      resize_keyboard=True)
    update.message.reply_text("Спасибо! \n "
                              "Вы можете посмотреть информацию о своих записях в \n"
                              " главном меню",
                              reply_markup=my_keyboard)


def info(bot, update, user_data):
    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']],
                                      resize_keyboard=True)
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\mapbrb.jpg', 'rb'))
    update.message.reply_text("Наши контакты: \n "
                              "Адрес: г.Москва, ул.Большая Ордынка 17 стр.1 \n "
                              "Телефон: +74951234567 \n "
                              "Часы работы: \n "
                              "Будни: с 10:00 до 22:00 \n "
                              "Выходные: c 12:00 до 22:00",
                              reply_markup=my_keyboard)


def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("О нас", info, pass_user_data=True))
    dp.add_handler(RegexHandler("О нас", info, pass_user_data=True))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user))

    dp.add_handler(CommandHandler("Вернуться в главное меню", get_contact))
    dp.add_handler(RegexHandler("Вернуться в главное меню", get_contact))

    dp.add_handler(CommandHandler("start", greet_user))
    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Запись', choose_master)],
        states={
            FIRST: [CallbackQueryHandler(choose_service)],
            SECOND: [CallbackQueryHandler(calendar)],
            THIRD: [CallbackQueryHandler(time)],
            FOUR: [CallbackQueryHandler(contact)]
        },
        fallbacks=[MessageHandler(Filters.contact, get_contact, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
