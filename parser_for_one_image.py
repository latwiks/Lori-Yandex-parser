import aiohttp
from bs4 import BeautifulSoup
import yaimparser_for_one_image


async def fetch_image(url, db):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()
            soup = BeautifulSoup(data, 'html.parser')
            image_tag = soup.find('img', {'class': 'pic-shield-image'})
            if image_tag is not None:
                image_url = image_tag['data-src']
                p = soup.find('time')
                p = p['datetime'] if p is not None else '-'
                return await yaimparser_for_one_image.yandexparser(
                    'https://yandex.ru/images/search?source=collections&cbir_page=sites&rpt=imageview&url=' + image_url,
                    p, url, db)
            else:
                return None
