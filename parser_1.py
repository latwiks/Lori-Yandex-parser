import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
import yandeximagesparser

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


async def f(url, m='', n='', db='db.db'):
    async with aiohttp.ClientSession() as session:
        session.headers.update(headers)
        tasks = []
        response = await session.get(url)
        data = await response.text()
        soup = BeautifulSoup(data, 'html.parser')
        a = soup.findAll()
        s = [int(i['data-page']) for i in a if i.has_attr('data-page')]
        maxnum = max(s)
        for i in range(1 if m == '' else int(m), maxnum if n == '' else int(n) + 1):
            tasks.append(asyncio.create_task(session.get(f'{url}&page={i}')))

        responses = await asyncio.gather(*tasks)
        print(responses)
        return await process_responses(responses, db)


async def process_responses(responses, db):
    times = []
    photo_vis = []
    links_of_pictures_2 = []
    pagestodb = []
    tasks = []
    for response in responses:
        tasks.append(asyncio.create_task(async_process(response, photo_vis, links_of_pictures_2, times, pagestodb)))
    await asyncio.gather(*tasks)
    conn = sqlite3.connect(f'databases/{db}')
    c = conn.cursor()
    c.execute('insert into user (photo_vis, link, times, pages) values (?, ?, ?, ?)',
              (f'{photo_vis}', f'{links_of_pictures_2}', f'{times}', f'{pagestodb}'))
    identifier = c.lastrowid
    conn.commit()
    conn.close()
    return await yandeximagesparser.main(db, identifier)


async def async_process(response, photo_vis, links_of_pictures_2, times, pagestodb):
    page = str(response.url)[-1]
    data = await response.text()
    soup = BeautifulSoup(data, 'html.parser')
    a = soup.findAll('a', {'class': 'img-title'})
    links_of_pictures = []
    s2, s4, pages = [], [], []
    async with aiohttp.ClientSession() as session1:
        session1.headers.update(headers)
        for j in a:
            retry = 3
            while retry > 0:
                try:
                    resp1 = await session1.get('https://lori.ru' + j['href'])
                    if resp1.status == 200 or resp1.status == 404:
                        break
                except:
                    print("error....")
            if resp1.status == 404:
                continue

            data1 = await resp1.text()
            bs = BeautifulSoup(data1, 'lxml')
            if bs.find('div', {'class': 'video-div'}):
                continue
            if bs.find('img', {'class': 'pic-shield-image'}) is None:
                continue
            links_of_pictures.append('https://lori.ru' + j['href'])

    async with aiohttp.ClientSession() as session2:
        session2.headers.update(headers)
        for i in links_of_pictures:
            retry = 3
            while retry > 0:
                try:
                    resp2 = await session2.get(i)
                    if resp2.status == 200 or resp2.status == 404:
                        break
                except:
                    print('error')
            if resp2.status == 404:
                continue

            data2 = await resp2.text()
            soup1 = BeautifulSoup(data2, 'lxml')
            l1 = soup1.find('img', {'class': 'pic-shield-image'})
            s2.append(l1['data-src'])
            p = soup1.find('time')
            pages.append(str(page))
            s4.append(p['datetime'] if p is not None else '-')

    photo_vis.append(s2)
    links_of_pictures_2.append(links_of_pictures)
    times.append(s4)
    pagestodb.append(pages)
    print(pagestodb)
