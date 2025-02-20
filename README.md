# Парсер для https://lori.ru
***
## Примеры реализации:
* #### Для ссылки на профиль в excel формате первой формы, когда не нужно удалять строки с повторяющимеся ссылками

```python
from excel import excel
from excel_2 import excel_2, excel_to_csv_2, remove_duplicates_csv, remove_duplicates_xlsx
from create_db import create_database
import parser
import parser_for_one_image


async def lori(sort_by: str, start_page: str, end_page: str,
               limiter: str):  # limiter, start_page, end_page - числа в строке (типа '5')
    db = await create_database('db', 'databases')
    await parser.main(
        'https://lori.ru/user' + sort_by,  # sort_by = '?' or '?sort=date' or '?sort=sales' or '?sort=random'
        start_page,
        end_page, db)
    a = await excel(db, limiter)
    return a  # a - строка (путь до файла)
```
* #### Для ссылки в формате excel второй формы, когда нужно удалить строки с повторяющимеся ссылками
```python
from excel import excel
from excel_2 import excel_2, excel_to_csv_2, remove_duplicates_csv, remove_duplicates_xlsx
from create_db import create_database
import parser
import parser_for_one_image
async def lori(sort_by: str, start_page: str, end_page: str,
               limiter: str):
    db = await create_database('db', 'databases')
    await parser.main('https://lori.ru/user' + sort_by,
                      start_page,
                      end_page, db)
    a = await excel_2(db, 'https://lori.ru/user', limiter)
    b = await remove_duplicates_xlsx(db)
    return b # b - строка (путь до файла)
```
#### Остальные примеры использования можно посмотреть в файле main.py
* ###### *****p.s. повторяющиеся ссылки - ссылки на тех, кто использовал ту или иную картинку, сортировка - картинок по лори.*****