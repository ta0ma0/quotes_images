from config import api_hash_conf, api_id_conf, bot_token_conf
import random
from telethon import TelegramClient, events
import asyncio
from asyncio import run
import sqlite3
import re

# Use your own values from my.telegram.org
api_id = api_id_conf
api_hash = api_hash_conf
bot_token = bot_token_conf
chat = '@tetus2_cbpnk1P0'
message = 'Say, hi!'



# Initialize bot and... just the bot!
bot = TelegramClient('bot', api_id_conf, api_hash_conf).start(bot_token=bot_token_conf)

@bot.on(events.NewMessage(pattern='/quote'))
async def quote_text(event):
    sequence = random.randint(402, 761)
    conn = sqlite3.connect('data/cyberpunk_quotes.db')
    cursor = conn.cursor()
    sql = f"SELECT text, author, link from cyber_punk_quotes where id='{sequence}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    try:
        text = rows[0][0]
        author = rows[0][1]
        link = rows[0][2]
    except IndexError as err:
        text = 'Void'
        author = 'Nothing'
        link = 'http://localhost'

    await event.respond(f'<i>{text}</i>\n <b>{author}</b>\n\n {link}\n', parse_mode='html')

@bot.on(events.NewMessage(pattern='/load'))
async def quote_image(event):
    sequence = random.randint(1, 379)
    sequence = str(sequence)
    file_name = f'data/images/{sequence}_image.webp'
    conn = sqlite3.connect('data/cyberpunk_quotes.db')
    cursor = conn.cursor()
    sql = f"SELECT image_info, tags, source_link from images where file_name='{file_name}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    try:
        image_info = rows[0][0]
        tags = rows[0][1]
        link = rows[0][2]
    except IndexError as err:
        tags = 'Void'
        image_info = 'Nothing'
        link = 'http://localhost'
#   
    if re.match(r'https://www.flickr.com', link):
        await event.respond(f'{tags}\n'+'\n\n'+f'**{image_info}**'+f'{link}', parse_mode='Markdown')
    else:
        await event.respond(file=file_name)
        await event.respond(f'{tags}\n'+'\n\n'+f'**{image_info}**'+f'{link}', parse_mode='Markdown')

# @bot.on(events.NewMessage)
# async def echo_all(event):
#     await event.reply(event.text)

if __name__ == '__main__':
    bot.run_until_disconnected()

