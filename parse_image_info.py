from bs4 import BeautifulSoup
import requests
import logging
import sqlite3
import time


logging.basicConfig(level=logging.INFO, filename='get_images.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

data_base_dict = {}
seq = 379
class ParseSource:
    def __init__(self, seq):
        self.seq = str(seq)
        self.page_source = open(f'data/pages/{str(self.seq)}_page.html')
        data = self.page_source.read()
        self.soup = BeautifulSoup(data, 'html.parser')


    def get_image_link(self):
        title_button = self.soup.find('section', attrs={'id': 'title-button'})
        # print(title_button)
        source_link = title_button.find('a', href=True)
        return source_link


    def get_image(self):
        image_link = self.soup.find('img')
        # download the image contents in binary format
        url = image_link['src']
        image = requests.get(url).content
        sequence = str(self.seq)
        # # open method to open a file on your system and write the contents
        file_name = f'data/images/{sequence}_image.webp'
        with open(file_name, 'wb') as f:
            f.write(image)
        logger.info('Image saved')
        return file_name

    def image_info(self):
        image_info = self.soup.find('div', attrs={'id':'panel-slot-plain'})
        return image_info.text

    def get_tags(self):
        tags_list = self.soup.find('section', attrs={'class':'w-full'})
        tags_list = tags_list.find_all('li')
        tags_list_clean = []
        for el in tags_list:
            tags_list_clean.append(el.text)
        return tags_list_clean


conn = sqlite3.connect('data/cyberpunk_quotes.db')
cursor = conn.cursor()

for el in range(seq):
    print(el)
    el +=1
    el = str(el)
    process_page = ParseSource(el)
    href = process_page.get_image_link()
    source_link = href['href']
    file_name = process_page.get_image()
    time.sleep(2)
    # print(img_src['src'])
    image_info = process_page.image_info()
    image_info = image_info.lstrip().replace('\'','\"')
    print(image_info)
    tags = process_page.get_tags()
    # print(tags)
    tags_str = tags[:6]
    tags_str = (' #').join(tags)
    tags_str = '#'+tags_str
    print(tags_str)
    sql = f"INSERT INTO images (file_name, image_info, tags, source_link) VALUES ('{file_name}', '{image_info}', '{tags_str}', '{source_link}')"
    cursor.execute(sql)
    conn.commit()
    logger.info('Data stored in DB')