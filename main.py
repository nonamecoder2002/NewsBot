from telegram import *
from telegram.ext import *
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

html_global = None

# FIXME:
#  1. Fix len() error


def start(update, context):
    context.bot.send_message(text="Я бот", chat_id=update.message.chat_id)


def parse(bs4_obj):
    article_raw = bs4_obj.a
    article_link = article_raw['href']
    article_img_url = article_raw.img['src']
    article_desc = article_raw.img['alt']
    return [article_img_url, article_desc, article_link]


def req_obj_to_bs4(url_):
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
    global html_global
    html_global = req_obj_to_bs4('https://tsn.ua/ukrayina')
    article_raw = html_global.article
    article = parse(article_raw)
    keyboard = [
        [InlineKeyboardButton(text='Посидання Тут', url=article[2]), ],
        [InlineKeyboardButton('Далі ⬇️', callback_data='down')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption_ = '*' + article[1] + '*'
    context.bot.send_photo(chat_id=update.message.chat.id, photo=article[0], caption=caption_,
                           reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    html_global = str(html_global).replace(str(article_raw), '')


def list_down(update, context):
    bot = context.bot
    query = update.callback_query
    global html_global
    article = BeautifulSoup(html_global, 'html.parser').article
    html_global = str(html_global).replace(str(article), '')
    article = parse(article)
    url_keyboard = InlineKeyboardMarkup([query.message.reply_markup.inline_keyboard[0]])
    bot.edit_message_caption(chat_id=query.message.chat_id, message_id=query.message.message_id,
                             parse_mode=ParseMode.MARKDOWN, caption=query.message.caption, reply_markup=url_keyboard)
    keyboard = [
        [InlineKeyboardButton(text='Посидання Тут', url=article[2])],
        [InlineKeyboardButton('Далі  ⬇️', callback_data='down')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    caption_ = '*' + article[1] + '*'
    bot.send_photo(chat_id=query.message.chat.id, photo=article[0], caption=caption_,
                   reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


def main():
    updater = Updater('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('log', log, filters=Filters.user(user_id=(399835396, 382182253))))
    dp.add_handler(CommandHandler('news', get_news))
    dp.add_handler(CallbackQueryHandler(callback=list_down, pattern='^down$'))
    # ERROR

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
