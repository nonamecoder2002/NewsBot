from telegram import *
from telegram.ext import *
import requests
from bs4 import BeautifulSoup
import logging


logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(text="Я бот", chat_id=update.message.chat_id)


def parse(bs4_obj):
    """

    :param bs4_obj: <article class = 'c-entry h-entry'>
    :return: list, [0] - img_url,
    [1] - desc for artic, [2] - link
    """
    article_raw = bs4_obj.a
    article_link = article_raw['href']
    article_img_url = article_raw.img['src']
    article_desc = article_raw.img['alt']
    return [article_img_url, article_desc, article_link]


def req_obj_to_bs4(url_):
    """

    :param url_: url
    :return: html ready to parse
    """
    html_raw = requests.get(url=url_).content
    html_bs4 = BeautifulSoup(html_raw, 'html.parser')
    return html_bs4


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def log(update, context):
    try:
        context.bot.send_document(chat_id=update.message.chat.id, document=open('log.txt', 'rb'))

    except TelegramError:
        update.message.reply_text("Файл пустой")


def get_news(update, context):
    html = req_obj_to_bs4('https://tsn.ua/ukrayina')
    article_raw = html.article
    i = 0
    while i < 4:
        article = parse(article_raw)
        context.bot.send_photo(chat_id=update.message.chat.id, photo=article[0], caption=article[1]+'\n'+article[2])
        article_raw = article_raw.find_next('article')
        i += 1


def main():
    updater = Updater('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('log', log, filters=Filters.user(user_id=(399835396, 382182253))))
    dp.add_handler(CommandHandler('news', get_news))
    # ERROR

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
