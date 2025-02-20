import ast
import asyncio
from bs4 import BeautifulSoup
import sqlite3

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


url = 'https://yandex.ru/images/search?source=collections&cbir_page=sites&rpt=imageview&url=https://prv2.lori-images.net/0002882066-larger.jpg'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Sec-Fetch-Dest': 'Document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-User': '?1',
           'TE': 'trailers',
           }

SCROLL_PAUSE_TIME = 0.5

async def scroll_to_bottom(driver):
    """
    Прокручивает страницу до конца, пока не будет загружен весь контент.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

async def parse_yandex_page(driver, url2, criminal_links_3, criminal_descriptions_3):
    """
    Парсит страницу Яндекс.Картинок и извлекает ссылки и описания найденных сайтов.
    """
    for i in range(len(url2)):
        driver.get(url + url2[i])
        await scroll_to_bottom(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        s = soup.findAll('li', {'class': 'CbirSites-Item'})
        s0 = [i.find('div', {'class': 'CbirSites-ItemInfo'}) for i in s]
        s1 = [i.find('div', {'class': 'CbirSites-ItemTitle'}) for i in s0]
        s2 = [i.find('a') for i in s1]
        criminal_links_3.append([j['href'] for j in s2])
        print([j['href'] for j in s2])
        print([j.contents for j in s2])
        criminal_descriptions_3.append([j.contents for j in s2])
    return criminal_links_3, criminal_descriptions_3

async def yandexparser(photo_vis, driver):
    """
    Асинхронно парсит страницы Яндекс.Картинок для каждой фотографии.
    """
    criminal_links = []
    criminal_descriptions = []
    tasks = []
    for url2 in photo_vis:
        tasks.append(asyncio.create_task(parse_yandex_page(driver, url2, criminal_links, criminal_descriptions)))
    await asyncio.gather(*tasks)
    return criminal_links, criminal_descriptions


async def main(db, identifier):
    """
    Основная функция, запускающая парсинг Яндекс.Картинок и сохраняющая результаты в базу данных.
    """
    criminal_links_2 = []
    criminal_descriptions_2 = []
    conn = sqlite3.connect(f'databases/{db}')
    c = conn.cursor()
    photo_vis = c.execute('select photo_vis from user where id=?', (identifier,)).fetchone()[0]
    photo_vis = ast.literal_eval(photo_vis)

    # Инициализация драйвера Selenium
    ua = UserAgent()
    userAgent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={userAgent}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(3)
    '''driver.execute_script("window.open('https://yandex.ru/', 'secondtab');")'''

    try:
        criminal_links, criminal_descriptions = await yandexparser(photo_vis, driver)
        criminal_links_2.append(criminal_links)
        criminal_descriptions_2.append(criminal_descriptions)
        c.execute('insert into criminals (criminal_links, criminal_descriptions) values (?, ?)',
                  (f'{criminal_links_2}', f'{criminal_descriptions_2}'))
        criminal_id = c.lastrowid
        conn.commit()
        conn.close()
        return [identifier, criminal_id]
    finally:
        # Закрытие драйвера Selenium
        driver.quit()