from telegram import *
from telegram.ext import *
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(handlers=[logging.FileHandler('log.txt', 'w', 'utf-8')],
                    level=logging.INFO,
                    format='[*] {%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

session_string = {}  # {user_id: [articles]}


def start(update, context):
    context.bot.send_message(text="Я бот", chat_id=update.message.chat_id)


def prepare_session_string(update, url):
    global session_string
    html_raw = requests.get(url=url).text
    html_bs4 = BeautifulSoup(html_raw, 'lxml')
    article_list = []

    for article in html_bs4.find_all('article'):
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
        article_list.append({'url': url, 'img_url': img_url, 'description': description})

    session_string.update({update.message.from_user.id: article_list})


def get_news(update, context):
    global session_string
    prepare_session_string(update, 'https://tsn.ua/ukrayina')
    url = session_string[update.message.from_user.id][0]['url']
    description = session_string[update.message.from_user.id][0]['description']
    img_url = session_string[update.message.from_user.id][0]['img_url']

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Посилання Тут', url=url)],
        [InlineKeyboardButton('Далі ⬇️', callback_data='down')]
    ])
    context.bot.send_photo(chat_id=update.message.chat.id, photo=img_url, caption=f"<b>{description}</b>",
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    session_string[update.message.from_user.id].pop(0)


def list_down(update, context):
    global session_string
    query = update.callback_query

    if len(session_string[query.from_user.id]) == 0:
        query.message.reply_text("Список новин закінчився.\nОновити список: /news")
        return

    url = session_string[query.from_user.id][0]['url']
    description = session_string[query.from_user.id][0]['description']
    img_url = session_string[query.from_user.id][0]['img_url']

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Посилання Тут', url=url)],
        [InlineKeyboardButton('Далі ⬇️', callback_data='down')]
    ])
    context.bot.send_photo(chat_id=query.message.chat.id, photo=img_url, caption=f"<b>{description}</b>",
                           reply_markup=keyboard, parse_mode=ParseMode.HTML, timeout=10)

    url_keyboard = InlineKeyboardMarkup([query.message.reply_markup.inline_keyboard[0]])
    context.bot.edit_message_caption(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                     parse_mode=ParseMode.HTML, caption=query.message.caption,
                                     reply_markup=url_keyboard, timeout=10)

    session_string[query.from_user.id].pop(0)


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
    html_global = BeautifulSoup(str(html_global).replace(str(article_raw), ''), 'html.parser')


def list_down(update, context):
    bot = context.bot
    query = update.callback_query
    global html_global
    article = html_global.article
    html_global = BeautifulSoup(str(html_global).replace(str(article), ''), 'html.parser')
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
