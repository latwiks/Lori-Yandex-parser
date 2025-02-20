import requests
from bs4 import BeautifulSoup
import sqlite3


async def yandexparser(url, times, url1, db='db.db'):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    s = soup.findAll('li', {'class': 'CbirSites-Item'})

    s0 = [i.find('div', {'class': 'CbirSites-ItemInfo'}) for i in s]
    s1 = [i.find('div', {'class': 'CbirSites-ItemTitle'}) for i in s0]
    s2 = [i.find('a') for i in s1]
    links = [j['href'] for j in s2]
    titles = [j.contents for j in s2]

    conn = sqlite3.connect(f'databases/{db}')
    c = conn.cursor()
    c.execute('insert into criminals (criminal_links, criminal_descriptions) values (?, ?)', (f'{[[links]]}', f'{[[titles]]}'))
    criminal_id = c.lastrowid
    conn.commit()
    c.execute('insert into user (photo_vis, link, times, pages) values (?, ?, ?, ?)', (f'{[[url]]}', f'{[[url1]]}', f'{[[times]]}', f'[{[str(1) for i in range(len(links))]}]'))
    uid = c.lastrowid
    conn.commit()
    conn.close()
    return [uid, criminal_id]

