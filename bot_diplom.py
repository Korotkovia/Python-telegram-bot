from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters,\
    RegexHandler

import logging
import telegramcalendar
import mysql.connector

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH = range(4)

conn = mysql.connector.connect(host='mysql.j949396.myjino.ru',
                               database='j949396',
                               user='046976902_1',
                               password='qwerty')

# cursor = conn.cursor()


def talk_to_me(bot, update):
    update.message.reply_text('Нажмите /start для запуска бота')


def greet_user(bot, update, user_data):
    # функция - /start

    if user_data == {}:
        text = 'Вас приветствует salon_service_bot!'
        my_keyboard = ReplyKeyboardMarkup([['Запись'],
                                           ['Мои записи', 'О нас', 'Отменить запись']],
                                          resize_keyboard=True,
                                          one_time_keyboard=True)
        update.message.reply_text(text, reply_markup=my_keyboard)
    else:
        text_2 = 'Выберите дальнейшее действие:'
        my_keyboard_2 = ReplyKeyboardMarkup([['Добавить запись'],
                                             ['Мои записи', 'О нас', 'Отменить запись']],
                                            resize_keyboard=True,
                                            one_time_keyboard=True)
        update.message.reply_text(text_2, reply_markup=my_keyboard_2)


def cancel_record(bot, update, user_data):
    cursor = conn.cursor()
    sql = "SELECT number FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    if user_data == {}:
        update.message.reply_text('У вас нет записей')
    else:
        for record in data_base:
            a = user_data.get('number')
            cursor.execute("DELETE FROM record_info WHERE number = %s" % a)
            user_data.clear()
            print(user_data)
            conn.commit()
            update.message.reply_text('Вы отменили запись')

    greet_user(bot, update, user_data)


def choose_service(bot, update, user_data):
    # функция вызова инлайн клавиатуры с мастерами
    cursor = conn.cursor()
    sql = "SELECT service_name FROM services"
    cursor.execute(sql)
    data_base = cursor.fetchall()
    all_masters = []
    for masters in data_base:
        all_masters.append(masters[0])
    keyboard = []
    row = []
    rows = []
    for i in all_masters[0:2]:
        row.append(InlineKeyboardButton(i, callback_data=str(i)))
    for i in all_masters[2:4]:
        rows.append(InlineKeyboardButton(i, callback_data=str(i)))

    keyboard.append(row)
    keyboard.append(rows)

    reply_markup = InlineKeyboardMarkup(keyboard)
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\BRB 666.jpg', 'rb'))
    update.message.reply_text('Выберите услугу:', reply_markup=reply_markup)
    return FIRST


def choose_master(bot, update, user_data):
    # функция вызова инлайн клавиатуры с услугами

    cursor = conn.cursor()

    sql = "SELECT * FROM services"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_1 = "SELECT * FROM barbers_to_services"
    cursor.execute(sql_1)
    data_base_1 = cursor.fetchall()

    sql_2 = "SELECT * FROM barbers"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    query = update.callback_query
    name = query.data
    # Клавиатура с услугами
    counter = []
    for masters in data_base:
        if name in masters:
            a = masters[0]
            for master_id in data_base_1:
                if a in master_id:
                    b = master_id[1]
                    for service_id in data_base_2:
                        if b in service_id:
                            all_services = []
                            all_services.append(service_id[1])
                            row = []
                            for i in all_services:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            counter = row + counter
    list_1 = []
    list_1.append(counter)
    reply_markup = InlineKeyboardMarkup(list_1)

    bot.edit_message_text(text='Выберите мастера:',
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)
    # Запись данных в user_data
    user_data['service'] = query.data
    return SECOND


def calendar(bot, update, user_data):
    # функция вызова календаря
    query = update.callback_query
    bot.edit_message_text(text='Выберите дату:',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=telegramcalendar.create_calendar())
    user_data['name'] = query.data
    return THIRD


def time(bot, update, user_data):
    # функция вызова инлайн клавиатуры с временем
    cursor = conn.cursor()

    query = update.callback_query
    selected, date = telegramcalendar.process_calendar_selection(bot, update)

    sql = "SELECT * FROM time_to_barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    if selected:
        all_time = []
        for name_list in data_base:
            if user_data.get('name') in name_list:
                all_time.append(name_list[1])
        keyboard = []
        row = []
        row_2 = []

        for i in all_time[0:3]:
            row.append(InlineKeyboardButton(i, callback_data=str(i)))
        for i in all_time[3:9]:
            row_2.append(InlineKeyboardButton(i, callback_data=str(i)))

        keyboard.append(row)
        keyboard.append(row_2)
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text='Выберите время:',
                              chat_id=update.callback_query.from_user.id,
                              message_id=query.message.message_id)
        bot.edit_message_reply_markup(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=reply_markup)
    user_data['date'] = date.strftime("%Y-%m-%d")
    return FOURTH


def contact(bot, update, user_data):
    # функция вызова запроса контактов
    query = update.callback_query
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    my_keyboard = ReplyKeyboardMarkup([[contact_button]],
                                      resize_keyboard=True,
                                      one_time_keyboard=True)
    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text="Отправьте Ваши контактные данные для уточнения заказа:",
                     reply_markup=my_keyboard)
    bot.delete_message(chat_id=update.callback_query.from_user.id,
                       message_id=query.message.message_id)
    user_data['time'] = query.data


def get_contact(bot, update, user_data):
    # функция обработчик контактов
    cursor = conn.cursor()
    print(update.message.contact)
    user_data['number'] = update.message.contact.phone_number
    user_data['first_name'] = update.message.contact.first_name
    user_data['last_name'] = update.message.contact.last_name

    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню']],
                                      resize_keyboard=True)
    update.message.reply_text("Спасибо! \n "
                              "Вы можете посмотреть информацию о своих записях в \n"
                              " главном меню",
                              reply_markup=my_keyboard)
    # Запись всех данных в БД
    record = (user_data.get('service'),
              user_data.get('name'),
              user_data.get('date'),
              user_data.get('time'),
              user_data.get('number'),
              user_data.get('first_name'),
              user_data.get('last_name'),
              )
    data = []
    data.append(record)
    record_insert = "INSERT INTO record_info (service, name, date, time, number, first_name, last_name)" \
                    " VALUES (%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(record_insert, record)
    conn.commit()
    # cursor.close()
    # conn.close()


def info(bot, update):
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


def my_entry(bot, update, user_data):
    # функция вывод информации о записях
    if user_data == {}:
        update.message.reply_text('У вас нет записей')
    else:
        my_keyboard = ReplyKeyboardMarkup([["Вернуться в главное меню"]],
                                          resize_keyboard=True)
        update.message.reply_text("Услуга: " + user_data.get('service') + "\n"
                                  "Имя мастера: " + user_data.get('name') + "\n"
                                  "Дата: " + user_data.get('date') + "\n"
                                  "Время: " + user_data.get('time') + "\n"
                                  "Клиент: " + user_data.get('first_name') + ' ' + user_data.get('last_name'),
                                  reply_markup=my_keyboard)


def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)
    dp = mybot.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Запись', choose_service, pass_user_data=True),
                      RegexHandler('Добавить запись', choose_service, pass_user_data=True)],
        states={
            FIRST: [CallbackQueryHandler(choose_master, pass_user_data=True)],
            SECOND: [CallbackQueryHandler(calendar, pass_user_data=True)],
            THIRD: [CallbackQueryHandler(time, pass_user_data=True)],
            FOURTH: [CallbackQueryHandler(contact, pass_user_data=True)]
        },
        fallbacks=[MessageHandler(Filters.contact, get_contact, pass_user_data=True)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler("О нас", info))
    dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(CommandHandler("Отменить запись", cancel_record, pass_user_data=True))
    dp.add_handler(RegexHandler("Отменить запись", cancel_record, pass_user_data=True))

    dp.add_handler(CommandHandler("Мои записи", my_entry, pass_user_data=True))
    dp.add_handler(RegexHandler("Мои записи", my_entry, pass_user_data=True))

    dp.add_handler(CommandHandler("Вернуться в главное меню", greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler("Вернуться в главное меню", greet_user, pass_user_data=True))

    # dp.add_handler(CommandHandler("Вернуться в главное меню", get_contact, pass_user_data=True))
    # dp.add_handler(RegexHandler("Вернуться в главное меню", get_contact, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
