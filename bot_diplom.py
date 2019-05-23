from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters,\
    RegexHandler
from emoji import emojize
from telegram.ext import messagequeue as mq

import logging
import telegramcalendar
import mysql.connector
import datetime
from datetime import timedelta

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

TOKEN = "728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo"

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

logger = logging.getLogger(__name__)

FIRST, SECOND, THIRD, FOURTH, FIVE = range(5)

conn = mysql.connector.connect(host='mysql.j949396.myjino.ru',
                               database='j949396',
                               user='046976902_1',
                               password='qwerty')

cursor = conn.cursor()

smile = emojize(':heavy_plus_sign:', use_aliases=True)
smile_2 = emojize(':ledger:', use_aliases=True)
smile_3 = emojize(':information_source:', use_aliases=True)
smile_4 = emojize(':x:', use_aliases=True)
smile_5 = emojize(':calendar:', use_aliases=True)
smile_6 = emojize(':man:', use_aliases=True)
smile_7 = emojize(':scissors:', use_aliases=True)
smile_8 = emojize(':clock230:', use_aliases=True)
smile_9 = emojize(':white_check_mark:', use_aliases=True)
smile_10 = emojize(':no_entry_sign:', use_aliases=True)
smile_11 = emojize(':telephone_receiver:', use_aliases=True)
smile_12 = emojize(':barber:', use_aliases=True)
smile_13 = emojize(':leftwards_arrow_with_hook:', use_aliases=True)


start_keyboard = ReplyKeyboardMarkup([['Добавить запись {}'.format(smile)],
                                      ['Мои записи {}'.format(smile_2),
                                       'О нас {}'.format(smile_3)]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True)


menu_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню {}'.format(smile_13)]],
                                    resize_keyboard=True)


def talk_to_me(bot, update):
    update.message.reply_text('Нажмите /start для запуска бота')


def greet_user(bot, update, user_data):
    # функция - /start
    text = 'Вас приветствует salon_service_bot! {}'.format(smile_12)
    update.message.reply_text(text, reply_markup=start_keyboard)


def choose_service(bot, update, user_data):
    # функция вызова инлайн клавиатуры с мастерами
    sql = "SELECT * FROM services"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    all_masters = []
    all_prices = []

    for masters in data_base:
        all_masters.append(masters[2])
    for prices in data_base:
        all_prices.append(prices[3])

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
    update.message.reply_text('Выберите услугу: {}'.format(smile_7) + '\n'
                              + all_masters[0] + ' - ' + str(all_prices[0]) + ' рублей' + '\n'
                              + all_masters[1] + ' - ' + str(all_prices[1]) + ' рублей' + '\n'
                              + all_masters[2] + ' - ' + str(all_prices[2]) + ' рублей' + '\n'
                              + all_masters[3] + ' - ' + str(all_prices[3]) + ' рублей' + '\n',
                              reply_markup=reply_markup)

    return FIRST


def choose_master(bot, update, user_data):
    # функция вызова инлайн клавиатуры с услугами
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

    # from_services = [masters[0] for masters in data_base if name in masters]
    # a = ''.join(from_services)

    counter = []
    for masters in data_base:
        if name in masters:
            a = masters[0]
            for master_id in data_base_1:
                if a in master_id:
                    b = master_id[1]
                    for service_id in data_base_2:
                        if b in service_id:
                            all_services = [service_id[1]]
                            row = []
                            for i in all_services:
                                row.append(InlineKeyboardButton(i, callback_data=str(i)))
                            counter = row + counter
    list_1 = [counter]
    reply_markup = InlineKeyboardMarkup(list_1)

    bot.edit_message_text(text='Выберите мастера: {}'.format(smile_6),
                          chat_id=update.callback_query.from_user.id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)

    # Запись данных в user_data
    user_data['service'] = query.data

    return SECOND


def calendar(bot, update, user_data):
    # функция вызова календаря
    query = update.callback_query
    name = query.data
    if name == 'Вова':
        bot.edit_message_text(text='Выберите дату: {}'.format(smile_5),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=telegramcalendar.create_calendar_vova())
    else:
        bot.edit_message_text(text='Выберите дату: {}'.format(smile_5),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=telegramcalendar.create_calendar())

    user_data['name'] = query.data

    return THIRD


def time_check(bot, update, user_data):
    # функция вызова инлайн клавиатуры с временем
    query = update.callback_query
    selected, date = telegramcalendar.process_calendar_selection(bot, update)

    sql = "SELECT * FROM time_to_barbers"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_2 = "SELECT * FROM record_info"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    if selected:
        all_time = []
        for name_list in data_base:
            if user_data.get('name') in name_list[0]:
                all_time.append(name_list[1])
        for time_info in data_base_2:
            if user_data.get('name') in time_info[1]:
                if date.strftime("%Y-%m-%d") in time_info[2]:
                    if time_info[3] in all_time:
                        all_time.remove(time_info[3])
                        if len(all_time) < 6:
                            all_time.append('Нет записи')
        keyboard = []
        row = []
        row_2 = []
        row_3 = [InlineKeyboardButton('Выбрать другой день', callback_data='Выбрать другой день')]

        for i in all_time[0:3]:
            row.append(InlineKeyboardButton(i, callback_data=str(i)))
        for i in all_time[3:6]:
            row_2.append(InlineKeyboardButton(i, callback_data=str(i)))

        keyboard.append(row)
        keyboard.append(row_2)
        keyboard.append(row_3)

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(text='Выберите время: {}'.format(smile_8),
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
    if query.data == "Нет записи":
        bot.answer_callback_query(callback_query_id=query.id)
    elif query.data == 'Выбрать другой день':
        bot.edit_message_text(text='Выберите дату: {}'.format(smile_5),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=telegramcalendar.create_calendar())
        return THIRD
    else:
        contact_button = KeyboardButton('Контактные данные {}'.format(smile_11), request_contact=True)
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
    print(update.message.contact)
    user_data['number'] = update.message.contact.phone_number
    user_data['first_name'] = update.message.contact.first_name
    user_data['last_name'] = update.message.contact.last_name

    my_keyboard = ReplyKeyboardMarkup([['Вернуться в главное меню {}'.format(smile_13)],
                                      ['Отправить напоминание']],
                                      resize_keyboard=True)

    update.message.reply_text("Спасибо! \n "
                              "Вы можете посмотреть информацию о своих записях в главном меню",
                              reply_markup=my_keyboard)

    """Запись всех данных в БД"""
    record = (user_data.get('service'),
              user_data.get('name'),
              user_data.get('date'),
              user_data.get('time'),
              user_data.get('number'),
              user_data.get('first_name'),
              user_data.get('last_name'),
              )

    record_insert = "INSERT INTO record_info (service, name, date, time, number, first_name, last_name)" \
                    " VALUES (%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(record_insert, record)
    conn.commit()

    """Создание переменной для напоминания"""
    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    zapis_1 = []

    for z in data_base:
        if user_data.get('number') == z[4]:
            zapis_1.extend((z[2:4]))

    top_zapis = (' '.join(zapis_1[0:2]))
    dates = datetime.datetime.strptime(top_zapis, "%Y-%m-%d %H:%M")
    lolkin = timedelta(hours=6, minutes=5)
    global topcheg
    topcheg = dates + lolkin
    print(topcheg)

    top_zapis_2 = (' '.join(zapis_1[2:4]))
    dates_2 = datetime.datetime.strptime(top_zapis_2, "%Y-%m-%d %H:%M")
    lolkin_2 = timedelta(hours=6, minutes=6)
    global topcheg_2
    topcheg_2 = dates_2 + lolkin_2
    print(topcheg_2)

    top_zapis_3 = (' '.join(zapis_1[4:6]))
    dates_3 = datetime.datetime.strptime(top_zapis_3, "%Y-%m-%d %H:%M")
    lolkin_3 = timedelta(hours=6, minutes=7)
    global topcheg_3
    topcheg_3 = dates_3 + lolkin_3
    print(topcheg_3)

    # cursor.close()
    # conn.close()


def my_entry(bot, update, user_data):
    """ Вывод информации о записях """

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    sql_2 = "SELECT * FROM services"
    cursor.execute(sql_2)
    data_base_2 = cursor.fetchall()

    if user_data == {}:
        update.message.reply_text('У вас нет записей {}'.format(smile_10),
                                  reply_markup=start_keyboard)
    else:
        check_price = []

        info_10 = []

        for z in data_base:
            if user_data.get('number') == z[4]:
                info_10.extend((z[0:4]))
                for m in data_base_2:
                    if z[0] in m[2]:
                        check_price.append(m[3])
        total_sum = sum(check_price[0:])

        row = []
        row_1 = []
        row_2 = []
        all_entries = []
        main_menu = []

        keyboard = []

        if len(info_10) == 4:
            row.append(InlineKeyboardButton((', '.join(info_10[0:4])), callback_data='1'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, main_menu))
        elif len(info_10) == 8:
            row.append(InlineKeyboardButton((', '.join(info_10[0:4])), callback_data='1'))
            row_1.append(InlineKeyboardButton((', '.join(info_10[4:8])), callback_data='2'))
            all_entries.append(InlineKeyboardButton('Отменить все записи {}'.format(smile_4), callback_data='Отмена'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, row_1, all_entries, main_menu))
        elif len(info_10) > 8:
            row.append(InlineKeyboardButton((', '.join(info_10[0:4])), callback_data='1'))
            row_1.append(InlineKeyboardButton((', '.join(info_10[4:8])), callback_data='2'))
            row_2.append(InlineKeyboardButton((', '.join(info_10[8:12])), callback_data='3'))
            all_entries.append(InlineKeyboardButton('Отменить все записи {}'.format(smile_4), callback_data='Отмена'))
            main_menu.append(InlineKeyboardButton('Вернуться в главное меню {}'.format(smile_13), callback_data='0'))
            keyboard.extend((row, row_1, row_2, all_entries, main_menu))

        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            update.message.reply_text('Клиент: ' + user_data.get('first_name') + '\n'
                                      + '\n'
                                      'Итоговая сумма: ' + str(total_sum) + '\n'
                                      + '\n'
                                      'Ниже представлена краткая информация о ваших записях.' + '\n'
                                      'Чтобы отменить запись -  просто нажмите на нее!',
                                      reply_markup=reply_markup)
        except AttributeError:
            bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=reply_markup)

        return FIVE


def cancel_entries(bot, update, user_data, job_queue):
    """ Удаление записей из базы данных """

    query = update.callback_query
    service = query.data

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    info_list = []
    for data_list in data_base:
        if user_data.get('number') in data_list[4]:
            info_list.extend((data_list[0:4]))

    if service == '1' and len(info_list) == 4:
        info_tuple = tuple(info_list[0:4])
        new_tuple = info_tuple + (user_data.get('number'),)
        cursor.execute("DELETE FROM record_info WHERE"
                       " service = %s"
                       " and name = %s"
                       " and date = %s"
                       " and time = %s"
                       " and number = %s",
                       new_tuple)
        user_data.clear()
        conn.commit()

        """ Удаление напоминания """
        job_queue.stop()

        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='У вас нет записей {}'.format(smile_10),
                         reply_markup=start_keyboard)
    elif service == '1':
        info_tuple = tuple(info_list[0:4])
        new_tuple = info_tuple + (user_data.get('number'),)
        cursor.execute("DELETE FROM record_info WHERE"
                       " service = %s"
                       " and name = %s"
                       " and date = %s"
                       " and time = %s"
                       " and number = %s",
                       new_tuple)
        conn.commit()

        if len(info_list) == 12:
            spisok[0].schedule_removal()
        elif len(info_list) == 8:
            spisok[1].schedule_removal()

    elif service == '2':
        info_tuple = tuple(info_list[4:8])
        new_tuple = info_tuple + (user_data.get('number'),)
        cursor.execute("DELETE FROM record_info WHERE"
                       " service = %s"
                       " and name = %s"
                       " and date = %s"
                       " and time = %s"
                       " and number = %s",
                       new_tuple)
        conn.commit()

        if len(info_list) == 12:
            spisok[1].schedule_removal()
        elif len(info_list) == 8:
            spisok[2].schedule_removal()

    elif service == '3':
        info_tuple = tuple(info_list[8:12])
        new_tuple = info_tuple + (user_data.get('number'),)
        cursor.execute("DELETE FROM record_info WHERE"
                       " service = %s"
                       " and name = %s"
                       " and date = %s"
                       " and time = %s"
                       " and number = %s",
                       new_tuple)
        conn.commit()
        spisok[2].schedule_removal()
    elif service == 'Отмена':
        info_tuple = user_data.get('number')
        cursor.execute("DELETE FROM record_info WHERE number = %s" % info_tuple)
        user_data.clear()
        conn.commit()
        job_queue.stop()
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='У вас нет записей {}'.format(smile_10),
                         reply_markup=start_keyboard)
    elif service == '0':
        bot.delete_message(chat_id=update.callback_query.from_user.id,
                           message_id=query.message.message_id)
        bot.send_message(chat_id=update.callback_query.from_user.id,
                         text='Вы вернулись в главное меню',
                         reply_markup=start_keyboard)

    bot.send_message(chat_id=update.callback_query.from_user.id,
                     text='Есть!',
                     reply_markup=my_entry(bot, update, user_data))


def info(bot, update):
    # bot.send_photo(chat_id=update.message.chat.id,
    #                photo=open('C:\projects\diplom\photo\mapbrb.jpg', 'rb'))
    update.message.reply_text("Наши контакты: \n "
                              "Адрес: г.Москва \n "
                              "Телефон: +74951234567 \n "
                              "Часы работы: \n "
                              "Будни: с 10:00 до 22:00 \n "
                              "Выходные: c 10:00 до 22:00",
                              reply_markup=menu_keyboard)


def set_alarm(bot, update, job_queue, user_data):

    sql = "SELECT * FROM record_info"
    cursor.execute(sql)
    data_base = cursor.fetchall()

    global vse_zapisi
    vse_zapisi = []
    global info_9
    info_9 = []

    for z in data_base:
        if user_data.get('number') == z[4]:
            vse_zapisi.append(z[4])
            info_9.extend((z[0:4]))

    print(vse_zapisi)

    if len(vse_zapisi) == 1:
        job_queue.run_once(alarm, when=topcheg, context=update.message.chat_id, name='lol')

    elif len(vse_zapisi) == 2:
        job_queue.run_once(alarm_1, when=topcheg_2, context=update.message.chat_id, name='lol')

    elif len(vse_zapisi) == 3:
        job_queue.run_once(alarm_2, when=topcheg_3, context=update.message.chat_id, name='lol')

    global spisok
    spisok = []

    for job in job_queue.get_jobs_by_name('lol'):
        spisok.append(job)
        print(job)
    print(spisok)

    update.message.reply_text("Напоминание создано!",
                              reply_markup=start_keyboard)


@mq.queuedmessage
def alarm(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 1' + ', '.join(info_9[0:4])))


@mq.queuedmessage
def alarm_1(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 2' + ', '.join(info_9[4:8])))


@mq.queuedmessage
def alarm_2(bot, job):
    bot.send_message(chat_id=job.context, text=('Запись 3' + ', '.join(info_9[8:12])))


def main():
    mybot = Updater('728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo', request_kwargs=PROXY)
    dp = mybot.dispatcher

    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default = True

    conv_handler = ConversationHandler(
        entry_points=[RegexHandler('Добавить запись', choose_service, pass_user_data=True),
                      RegexHandler('Мои записи', my_entry, pass_user_data=True),
                      ],
        states={
            FIRST: [CallbackQueryHandler(choose_master, pass_user_data=True)],
            SECOND: [CallbackQueryHandler(calendar, pass_user_data=True)],
            THIRD: [CallbackQueryHandler(time_check, pass_user_data=True)],
            FOURTH: [CallbackQueryHandler(contact, pass_user_data=True)],
            FIVE: [CallbackQueryHandler(cancel_entries, pass_user_data=True, pass_job_queue=True)],
        },
        fallbacks=[MessageHandler(Filters.contact, get_contact, pass_user_data=True)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler("О нас", info))
    dp.add_handler(RegexHandler("О нас", info))

    dp.add_handler(CommandHandler('Вернуться в главное меню', greet_user, pass_user_data=True))
    dp.add_handler(RegexHandler('Вернуться в главное меню', greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler('Отправить напоминание', set_alarm, pass_job_queue=True, pass_user_data=True))
    dp.add_handler(RegexHandler('Отправить напоминание', set_alarm, pass_job_queue=True, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

'''executemany (executescript) несколько обращений к базе данных ?'''
'''для базы данных сделать условие с отключением через определенное время'''
