from telegram import *
from telegram.ext import *
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

news_container = []

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Посилання Тут', url='')],
    [InlineKeyboardButton('Далі ⬇️', callback_data='down')]
])


def start(update, context):
    context.bot.send_message(text="Найновіші новини тут!", chat_id=update.message.chat_id)


def load_news():
    article_container = []
    site_html = BeautifulSoup(requests.get(url='https://tsn.ua/ukrayina').text, 'lxml')
    for article in site_html.find_all('article'):
        article_dict = dict(zip(['article_img', 'article_title', 'article_url'],
                            [article.img['data-src'], article.img['alt'], article.a['href']]))
        article_container.append(article_dict)

        """    
        url = article.div.a['href']
        img_url = None
        description = None

        for img in article.find_all('img'):
            try:
                if img['class'][0] == 'c-post-img':
                    img_url = img['src']
                    description = img['alt']
                    break

                elif img['class'][0] == 'lazyload c-post-img' or \
                        img['class'][0] == 'lazyload':
                    img_url = img['data-src']
                    description = img['alt']
                    break
            except Exception as err:
                if err == 'class':
                    img_url = img['src']
                    description = img['alt']
                    break

        if img_url is None or description is None:
            continue

        print(f"| {url}\n|\n| {img_url}\n|\n| {description}\n\n\n")
        """
    return article_container


print(load_news()[-1])


def show_news(update, context):
    context.bot.send_photo(chat_id=update.message.chat.id, photo='', caption='',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)


def show_next(update, context):
    query = update.callback_query
    context.bot.send_photo(chat_id='', photo='___url_for_photo___', caption='___text___',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML, timeout='__int_val__')

    url_keyboard = InlineKeyboardMarkup([query.message.reply_markup.inline_keyboard[0]])
    context.bot.edit_message_caption(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                     parse_mode=ParseMode.HTML, caption=query.message.caption,
                                     reply_markup=url_keyboard, timeout='__int_val__')


def error(update, context):
    print('Update "%s" caused error "%s"', update, context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def log(update, context):
    try:
        context.bot.send_document(chat_id=update.message.chat.id, document=open('log.txt', 'rb'))

    except TelegramError:
        update.message.reply_text("Файл пустой")


def main():
    updater = Updater('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('log', log, filters=Filters.user(user_id=(399835396, 382182253))))
    dp.add_handler(CommandHandler('news', show_news))
    dp.add_handler(CallbackQueryHandler(callback=show_next, pattern='^down$'))
    # ERROR

    dp.add_error_handler(error)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
