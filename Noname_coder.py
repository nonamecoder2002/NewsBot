import bs4
import requests
import re
import telebot

bot = telebot.TeleBot('925440483:AAHrvCoN89-Norr7LPjCs1xxflrs1oU604o')


@bot.message_handler(commands=['news'])
def get_news(message):
    global gap
    gap = 3
    site = requests.get('https://www.pravda.com.ua/news/')
    site_script = bs4.BeautifulSoup(site.text, features="html.parser")
    tag_a = site_script.select('.news_all .article')
    storage = {}
    count = 0
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
            mes_content = get_content[x].getText()
            storage.setdefault(count, mes_time + '\n' + '!' + mes_title + '!' '\n\n' + mes_content + '\n\n' + get_link
                               )
        count += 1

    def output(y: int):
        i = 0
        for v in storage.values():
            if y <= i < y + 2:
                bot.send_message(message.chat.id, v, disable_web_page_preview=True)
            elif i == y + 2:
                markup = telebot.types.InlineKeyboardMarkup()
                expand_but = telebot.types.InlineKeyboardButton('Показати Ще', callback_data='expand')
                markup.add(expand_but)
                bot.send_message(message.chat.id, v, reply_markup=markup, disable_web_page_preview=True)
            i = i + 1

    output(0)

    @bot.callback_query_handler(lambda query: query.data == 'expand')
    def expand(query):
        global gap
        output(gap)
        gap = gap + 3


gap = 0
bot.polling(none_stop=True)
