# Парсер Lori + Yandex Images

## Описание проекта
**Лори-проверяльщик** — это веб-приложение на базе Flask, предназначенное для автоматизированного анализа изображений с сайта lori.ru. Оно позволяет собирать данные, сортировать их, а также экспортировать в форматы Excel (.xlsx) и CSV (.csv).

## Функционал
- Парсинг изображений с сайта lori.ru.
- Проверка изображений на совпадения в Яндекс.Картинках.
- Сохранение результатов в базу данных SQLite.
- Экспорт данных в форматы Excel и CSV.
- Опциональное удаление дубликатов из полученных данных.
- Поддержка светлой и тёмной темы интерфейса.

## Используемые технологии
- **Backend:** Flask, SQLite, asyncio, aiohttp.
- **Парсинг:** BeautifulSoup, Selenium, requests.
- **Frontend:** HTML, CSS, JavaScript.
- **Форматы вывода:** OpenPyXL, CSV.

## Установка и запуск
### Клонирование репозитория и заход в папку:
```sh
git clone https://github.com/latwiks/Lori-Yandex-parser.git && cd Lori-Yandex-parser
```
### Создание виртуального окружения
Вы можете создать и использовать виртуальное окружение командой
```sh
python -m venv venv && .\venv\Scripts\activate
```
### Установка зависимостей
Перед запуском убедитесь, что у вас установлен Python 3. Установите необходимые пакеты:
```sh
pip install -r requirements.txt
```

### Запуск сервера
Перед запуском создайте БД:
```sh
python create_db.py
```
Запустите сервер командой:
```sh
python main.py
```
Приложение будет доступно по адресу `http://127.0.0.1:5000/`.

## Структура проекта
```
📂 проект
├── 📂 templates          # HTML-шаблоны
│   ├── index.html        # Основной интерфейс
├── 📂 databases          # База данных SQLite
├── 📂 excel_files        # Генерируемые файлы Excel
├── 📂 csv_files          # Генерируемые файлы CSV
├── create_db.py         # Скрипт для создания базы данных
├── excel.py             # Функции экспорта в Excel
├── excel_2.py           # Альтернативный экспорт в Excel и CSV
├── main.py              # Основной Flask-сервер
├── parser_1.py          # Основной парсер lori.ru
├── parser_for_one_image.py  # Парсер для одного изображения
├── yandeximagesparser.py # Парсер Яндекс.Картинок
├── passenger_wsgi.py    # Конфигурация для сервера
└── README.md            # Описание проекта
```
## Как использовать
1. Введите URL изображения или страницы lori.ru (в формате https://lori.ru/profile (если страница пользователя) или https://lori.ru/0123 (если страница картинки)).
2. Укажите диапазон страниц и параметры сортировки.
3. Выберите формат вывода (Excel или CSV).
4. При необходимости выберите удаление дубликатов.
5. Нажмите кнопку "Готово" и скачайте файл с результатами.

## Лицензия
Проект распространяется под MIT License.

## Картинки
![Главная (Dark)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20(Dark).png)
![Главная (Light)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20(Light).png)
![Ожидание (Dark)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%9E%D0%B6%D0%B8%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8%20(Dark).png)
![Ожидание (Light)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%9E%D0%B6%D0%B8%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8%20(Light).png)
![Сервер (1)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D0%BF%D0%B0%D1%80%D1%81%D0%B5%D1%80%D0%B0%20(%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80).png)
![Сервер (2)](https://github.com/latwiks/Lori-Yandex-parser/blob/b2c6e6ff58f9c27dad63d491258f7ce44ebf19c9/images/%D0%A0%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%20%D0%BF%D0%B0%D1%80%D1%81%D0%B5%D1%80%D0%B0%202%20(%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80).png)

