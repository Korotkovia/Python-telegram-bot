#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
import datetime
import calendar


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = []
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),
                                    callback_data=data_ignore))
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day,
                                        callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)

    # Remove the days that have passed
    past_days = datetime.datetime.today()
    active_days = int(past_days.strftime("%d"))
    #list for master
    # Sergey = [9, 10, 11]

    for week in my_calendar:
        row = []
        for day in week:
            if month == now.month:
                # for current month
                if day < active_days:
                    # output days starting from the current
                    row.append(InlineKeyboardButton(" ",
                                                    callback_data=data_ignore))
                #days for master Sergey
                # elif day in Sergey:
                #     row.append(InlineKeyboardButton(" ",
                #                                     callback_data=data_ignore))
                else:
                    row.append(InlineKeyboardButton(str(day),
                                                    callback_data=create_callback_data("DAY", year, month, day)))
            else:
                # for previous and next month
                if day == 0:
                    row.append(InlineKeyboardButton(" ",
                                                    callback_data=data_ignore))
                else:
                    row.append(InlineKeyboardButton(str(day),
                                                    callback_data=create_callback_data("DAY", year, month, day)))

        keyboard.append(row)
    # Last row - Buttons
    row = []
    row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def create_calendar_vova(year=None, month=None):
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    row = []
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),
                                    callback_data=data_ignore))
    keyboard.append(row)
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day,
                                        callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)

    active_days = int(now.strftime("%d"))

    vova_list = [5, 7, 10, 12, 16, 17, 18, 25, 26, 30, 31]

    for week in my_calendar:
        row = []
        for day in week:
            if month == now.month:
                if day < active_days:
                    row.append(InlineKeyboardButton(" ",
                                                    callback_data=data_ignore))
                    # для вовы
                elif day > active_days and day in vova_list:
                    row.append(InlineKeyboardButton(str(day),
                                                    callback_data=create_callback_data("DAY", year, month, day)))
                else:
                    row.append(InlineKeyboardButton(" ",
                                                    callback_data=data_ignore))
            elif month < now.month:
                row.append(InlineKeyboardButton(" ",
                                                callback_data=data_ignore))
            else:
                if day in vova_list:
                    row.append(InlineKeyboardButton(str(day),
                                                    callback_data=create_callback_data("DAY", year, month, day)))
                else:
                    row.append(InlineKeyboardButton(" ",
                                                    callback_data=data_ignore))

        keyboard.append(row)
    row = []
    row.append(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False, None)
    query = update.callback_query
    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar_vova(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar_vova(int(ne.year), int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id=query.id,
                                  text="Something went wrong!")
        # UNKNOWN
    return ret_data


'''сделать 4 функции telegramm create calendar, в кажджой будет лежать свой список'''


