import codecs
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import logging


"""
For work telegram-bot need minumum 365 images one image per day. After year bot is stop
and offer start again with repeat content. This script will get 365 first searching  results
CC license imges from https://openverse.org
"""

logging.basicConfig(level=logging.DEBUG, filename='get_images.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


url = 'https://openverse.org/search/image?q=cyberpunk&license_type=commercial,modification'
base_url = 'https://openverse.org'


Options = Options()
Options.headless = True

def get_page():
    driver = webdriver.Firefox(options=Options, executable_path='/home/ruslan/opt/geckodriver')
    driver.maximize_window()
    driver.get(url)
    weather_file = codecs.open('data/openverse.org.html', 'w', 'utf-8')
    data = driver.page_source
    weather_file.write(data)
    driver.quit()
    logging.info('Page is saved')

# page = get_page()

def get_thumbls_links():
    source_code = open('data/openverse.org.html')
    page_thumbls = source_code.read()
    soup = BeautifulSoup(page_thumbls, "html.parser")
    block_thumbls = soup.select('section[data-testid=search-results]')
    return block_thumbls


result = get_thumbls_links()
print(result)