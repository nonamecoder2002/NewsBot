from telegram import *
from telegram.ext import *
import logging


logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


print('[+]: SERVER STARTED')


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(text=f"{str(update)} ::::: {context.error}", chat_id=382182253)


def log(update, context):
    try:
        context.bot.send_document(chat_id=update.message.chat.id, document=open('log.txt', 'rb'))

    except TelegramError:
        update.message.reply_text("Файл пустой")


def start(update, context):
    context.bot.send_message(text="""HELLO""", chat_id=update.message.chat_id)


def main():
    updater = Updater('653357354:AAFtAd6zhj4aw6I7zdprQuewRv-tHd3egxk', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('log', log, filters=Filters.user(user_id=(399835396, 382182253))))
    # ERROR

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
