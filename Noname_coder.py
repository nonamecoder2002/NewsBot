import bs4
import requests
import re
import telebot

bot = telebot.TeleBot('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o')

gap = 3
storage = []


@bot.message_handler(commands=['news'])
def get_news(message):
    site = requests.get('https://www.pravda.com.ua/news/')
    site_script = bs4.BeautifulSoup(site.text, features="html.parser")
    tag_a = site_script.select('.news_all .article')
    global storage
    storage = []
    for line in tag_a:
        get_time = line.select('.article__time')
        get_title = line.select('.article__title')
        get_content = line.select('.article__subtitle')
        for x in range(len(get_time)):
            raw_line = str(line)
            get_link = ''.join(re.findall(r'"\S+/"', raw_line)).replace('"', '')
            if 'https:' not in get_link:
                get_link = 'https://www.pravda.com.ua' + get_link
            mes_time = get_time[x].getText()
            mes_title = get_title[x].getText()
            mes_title = str(mes_title)
            mes_title = ''.join(re.findall(r'\S+|\s\S+', mes_title))
            mes_content = get_content[x].getText()
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
