import codecs
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import logging
import time


"""
For work telegram-bot need minumum 365 images one image per day. After year bot is stop
and offer start again with repeat content. This script will get 365 first searching  results
CC license imges from https://openverse.org
"""

logging.basicConfig(level=logging.INFO, filename='get_images.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


url = 'https://openverse.org/search/image?q=cyberpunk&license_type=commercial,modification'
base_url = 'https://openverse.org'


Options = Options()
Options.headless = True

def get_page(base_url=base_url, url=url):
    driver = webdriver.Firefox(options=Options, executable_path='/home/ruslan/opt/geckodriver')
    driver.maximize_window()
    driver.get(url)
    count=20 #20 images per page we need load 18 pages for 365 images, + 2 for redudancy
    while count>1:
        button=driver.find_element_by_css_selector('[data-testid="load-more"]')
        button.click()
        count-=1
        time.sleep(2)
    weather_file = codecs.open('data/openverse.org.html', 'w', 'utf-8')
    data = driver.page_source
    weather_file.write(data)
    driver.quit()
    logging.info('Page is saved')


def get_thumbls_links():
    source_code = open('data/openverse.org.html')
    page_thumbls = source_code.read()
    soup = BeautifulSoup(page_thumbls, "html.parser")
    block_thumbls = soup.find('section', attrs={'data-testid':'search-results'})
    return block_thumbls

def get_hrefs(source):
    hrefs_links = []
    hrefs = source.find_all('a', attrs={'itemprop':'contentUrl'}, href=True)
    for el in hrefs:
        hrefs_links.append(el['href'])
    return hrefs_links


def get_image_page(base_url, url, sequences):
    """
    Get image with image info store to dictionary with
    {'name':'file.jpg','credit_the_creator':'','tags':['1','2',3','...'],'source_link':'flicr.com/link'
    """
    page = requests.get(base_url+url)
    data_store = open(f'data/pages/{sequences}_page.html', 'w')
    data_store.write(page.text)
    data_store.close()
    time.sleep(2)
    logger.info('Writing on disk')

# get_page()
thumbls = get_thumbls_links()
count_links = get_hrefs(thumbls)
# print(count_links)

sequeces = 0

for el in count_links:
    sequeces += 1
    get_image_page(base_url, el, sequeces)