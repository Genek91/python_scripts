from functools import wraps
from typing import Callable, Any
from sqlite3 import Cursor
import sqlite3

DB_PATH = 'db.sqlite3'


def db_connection(func: Callable) -> Callable:
    '''
    Декоратор для подключения к базе данных SQLite.
    '''
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            result = func(cursor, *args, **kwargs)
        return result
    return wrapper


@db_connection
def create_and_fill_db(cursor: Cursor) -> None:
    '''Создает таблицу Users и заполняет её начальными данными.'''
    cursor.execute(
        '''
        SELECT count(*)
        FROM sqlite_master
        WHERE type="table" AND name="Users"
        '''
    )
    table_exists = cursor.fetchone()[0]
    if not table_exists:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
            '''
        )
        cursor.executemany(
            'INSERT INTO Users (name, age) VALUES (?, ?)',
            [
                ('user_1', 33),
                ('user_2', 28),
                ('user_3', 25),
                ('user_4', 45)
            ]
        )


@db_connection
def get_data(cursor: Cursor) -> list[tuple[str, int]]:
    '''
    Извлекает имена и возраст пользователей старше 30 лет из таблицы Users.
    '''
    cursor.execute('SELECT name, age FROM Users WHERE age > 30')
    return cursor.fetchall()


def main() -> None:
    '''Основная функция.'''
    create_and_fill_db()
    users = get_data()
    for name, age in users:
        print(f'Имя: {name}, Возраст: {age}')


if __name__ == '__main__':
    main()
