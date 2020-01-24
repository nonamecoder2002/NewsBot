from telegram import *
from telegram.ext import *
import requests
from bs4 import BeautifulSoup


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
    article_img_url = article_raw.img['data-src']
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


def main():
    updater = Updater('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
