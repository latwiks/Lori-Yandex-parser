import sqlite3
from openpyxl import Workbook
import ast


async def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


async def excel(db, limiter, uid, criminal_id, url, sortby, isphoto):
    conn = sqlite3.connect(f'databases/{db}')
    c = conn.cursor()
    link = ast.literal_eval(c.execute('select link from user where id=?', (uid,)).fetchone()[0])
    times = ast.literal_eval(c.execute('select times from user where id=?', (uid,)).fetchone()[0])
    criminal_links = ast.literal_eval(c.execute('select criminal_links from criminals where id=?', (criminal_id,)).fetchone()[0])
    criminal_descriptions = ast.literal_eval(c.execute('select criminal_descriptions from criminals where id=?', (criminal_id,)).fetchone()[0])
    conn.close()
    wb = Workbook()
    ws = wb.active
    for i in range(len(link)):
        for j in range(len(link[i])):
            ij = 1
            if len(criminal_links[j]) >= 20:
                if await isint(limiter) or limiter == '':
                    if limiter == '':
                        ws.append(
                            [link[i][j], times[i][j], 'Более 20 результатов', 'Точных совпадений не выявлено'])
                        continue
                    elif int(limiter) <= 0:
                        ws.append(
                            [link[i][j], times[i][j], 'Более 20 результатов', 'Точных совпадений не выявлено'])
                        continue
                    else:
                        for ii in range(len(criminal_links[i][j])):
                            if ij + 1 > int(limiter) + 1:
                                break
                            ws.append([ij, criminal_links[i][j][ii], criminal_descriptions[i][j][ii][0], '', '', ''])
                            ij += 1
                        continue
            else:
                data = [
                    ['', '', '', '', '', ''],
                    ['', '', '', '', '', ''],
                    ['Картинка', link[i][j], 'На странице:', str(i + 1), 'Дата съёмки:', times[i][j]],
                    ['Кол-во нарушений', 'Ссылки', 'Описание', 'Дата публикации', 'Ссылка на первоисточник',
                     'Нарушитель'],
                ]
                for ii in range(len(criminal_links[i][j])):
                    data.append([ij, criminal_links[i][j][ii], criminal_descriptions[i][j][ii][0], '', '', ''])
                    ij += 1
                for row in data:
                    ws.append(row)
    if isphoto:
        a = '_'
    elif sortby == '?':
        a = '_by_order_'
    elif sortby == '?sort=date':
        a = '_by_date_'
    elif sortby == '?sort=sales':
        a = '_by_sales_'
    elif sortby == '?sort=random':
        a = '_by_random_'
    wb.save(f"excel_files/{url}{a}{uid}_{criminal_id}.xlsx")
    return f'excel_files/{url}{a}{uid}_{criminal_id}.xlsx'
