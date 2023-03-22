import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
import re
import time

logging.basicConfig(level=logging.INFO, filename='get_images.log',
                    format='%(funcName)20s() %(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


base_url = 'https://www.goodreads.com'
url = 'https://www.goodreads.com/quotes/tag/cyberpunk'

def get_page(url, seq):
    page = requests.get(url+f'?page={seq}')
    file_name = f'data/pages/{seq}_quote_page.html'
    data_store = open(file_name, 'w')
    data_store.write(page.text)
    data_store.close()
    logger.info('Page saved')



def read_data(seq):
    file_name = f'data/pages/{seq}_quote_page.html'
    page = open(file_name)
    read_data = page.read()
    soup = BeautifulSoup(read_data, 'html.parser')
    return soup

def parse_data(soup):
    all_qoute_data_list = []
    quotes_details = soup.find_all('div', attrs={'class':'quoteDetails'})
    # print(quotes_text)
    for el in quotes_details:
        quote_data_list = []
        quote_text = el.find('div', attrs={'class':'quoteText'})
        quote_text_ = quote_text.text
        quote_text_clean = quote_text_.replace('\n','')
        quote_text_clean = quote_text_.replace('\'','"')
        text_author_list = quote_text_clean.split('―')
        text = text_author_list[0].strip()
        author = text_author_list[1].strip()
        author = author.replace('\n','')
        # print(text_author_list)
        quote_footer = el.find('div', attrs={'class':'quoteFooter'})
        tags = quote_footer.find_all('a')
        tags_list = []
        for el in tags:
            tags_list.append(el.text)
        # print(tags_list[:-1])
        tags_list_str = ' #'.join(tags_list[:-1]) # Last value is count of likes, we don't need it.
        tags_list_str = '#'+tags_list_str
        quote_link = quote_footer.find('a', attrs={'class':'smallText'}, href=True)
        # print(quote_link)
        quote_data_list.append(text)
        quote_data_list.append('― '+ author)
        quote_data_list.append(base_url+quote_link['href'])
        # print(text, '―',author, base_url+quote_link['href'])
        all_qoute_data_list.append(quote_data_list)
    return all_qoute_data_list


def write_to_db(all_qoute_data_list):
    conn = sqlite3.connect('data/cyberpunk_quotes.db')
    cursor = conn.cursor()
    for item in all_qoute_data_list:
        sql = f"INSERT INTO cyber_punk_quotes (text, author, link) VALUES ('{item[0]}', '{item[1]}', '{item[2]}')"
        conn.execute(sql)
        conn.commit()


for el in range(12):
    el += 1
    # get_page(url, el)
    # time.sleep(2)
    soup = read_data(el)
    all_qoute_data_list = parse_data(soup)
    # print(all_qoute_data_list)
    write_to_db(all_qoute_data_list)