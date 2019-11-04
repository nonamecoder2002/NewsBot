import bs4
import telebot
from urllib.request import urlopen
bot = telebot.TeleBot('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o')

gap = 3
storage = []


@bot.message_handler(commands=['news'])
def get_news(message):
    site = urlopen('https://www.pravda.com.ua/news/')
    site_script = bs4.BeautifulSoup(site, features="html.parser")
    news_raw = site_script.find_all('div', {'class': 'news_all'})
    global storage
    storage = []
    news_raw = news_raw[0]
    get_time = news_raw.find_all('div', {'class': 'article__time'})
    get_title = news_raw.find_all('div', {'class': 'article__title'})
    get_content = news_raw.find_all('div', {'class': 'article__subtitle'})
    for x in range(len(get_title)):
        get_link = get_title[x].a.attrs['href']
        if 'https:' not in get_link:
            get_link = 'https://www.pravda.com.ua' + get_link
        mes_time = get_time[x].getText()
        mes_title = get_title[x].get_text()
        mes_content = get_content[x].getText()
        try:
            junk = get_title[x].em.get_text()
            mes_title = mes_title.replace(junk, '')
            storage.append(f'🕒 {mes_time}\n\n📍 {mes_title}  \n\n📰 {mes_content}\n\n 🖥 {get_link}')
        except AttributeError:
            storage.append(f'🕒 {mes_time}\n\n📍 {mes_title}  \n\n📰 {mes_content}\n\n 🖥 {get_link}')

    def output(y, id_, arr):
        for i in range(y, y+3):
            if i != y+2:
                bot.send_message(id_, arr[i], disable_web_page_preview=True)
            elif i == y + 2:
                markup = telebot.types.InlineKeyboardMarkup()
                expand_but = telebot.types.InlineKeyboardButton('Показати Ще', callback_data='expand')
                markup.add(expand_but)
                bot.send_message(id_, arr[i], reply_markup=markup, disable_web_page_preview=True)
    output(0, message.chat.id, storage)

    @bot.callback_query_handler(lambda query: query.data == 'expand')
    def expand(query):
        bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id, reply_markup=None)
        global gap
        global storage
        output(gap, query.message.chat.id, storage)
        gap = gap + 3

    global gap
    gap = 3


bot.polling(none_stop=True)
