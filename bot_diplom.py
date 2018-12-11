from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

def talk_to_me(bot, update):
    user_text = update.message.text 
    print('Приносим свои извинения! Бот находится в стадии разработки!')
    update.message.reply_text('Приносим свои извинения! Бот находится в стадии разработки!')

def greet_user(bot, update):
	text = 'Приносим свои извинения! Бот находится в стадии разработки!'
	print(text)
	update.message.reply_text(text)

def main():
    mybot = Updater("728852231:AAEZLnITK0BYNpAfQ4DCIC8CjpyiYLYUpIo", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()

main ()
