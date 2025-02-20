import os
import sqlite3


def create_database(db_name='db.db', directory='databases'):
    db_path = f'{directory}/{db_name}'
    if not os.path.isfile(db_path):
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute('''CREATE TABLE criminals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                criminal_links,
                criminal_descriptions
            );''')
        connection.commit()
        c.execute('''CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                photo_vis,
                link,
                times,
                pages
            );''')
        connection.commit()
        connection.close()
    else:
        print('Database already exists. Delete it first.')
    return db_name


create_database()
