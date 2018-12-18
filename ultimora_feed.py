from conf import TOKEN, ALLOWED_CHAT_ID, NAME, LINK, SUBTITLE, FILE_NAME

import telebot 
from feedgen.feed import FeedGenerator

bot = telebot.TeleBot(TOKEN)
feed = FeedGenerator()
feed.title(NAME)
feed.link(href=LINK, rel="alternate")
feed.subtitle(SUBTITLE)


def _update_file():
    with open(FILE_NAME, r) as rss_file:
        rss_file.write(feed.rss_str(pretty=False))


@bot.channel_post_handler(func=lambda m: True, content_types=['text', 'photo'])
def on_new_channel_post(message):
    if message.chat.id == ALLOWED_CHAT_ID:
        text = message.text if message.text != None else message.caption
        if text != None:
            _f = feed.add_entry()
            _f.id(str(message.message_id))
            _f.title(text)
    
            _update_file()


bot.polling(none_stop=True)

