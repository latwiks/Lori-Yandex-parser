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

