from http import HTTPStatus
import json
import logging
import urllib.request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

URL = 'https://jsonplaceholder.typicode.com/posts'
FILE_PATH = 'data.json'


def get_data(url: str) -> list | None:
    '''Получает данные с указанного URL.'''
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == HTTPStatus.OK:
                return json.loads(response.read().decode())
            else:
                logger.error(f'Код состояния ответа: {response.status}')
    except Exception as exc:
        logger.error(f'Ошибка при получении данных: {exc}')


def save_to_file(data: list, filename: str) -> None:
    '''Сохраняет данные в JSON-файл.'''
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        logger.info(f'Данные сохранены в файл: {filename}')
    except Exception as exc:
        logger.error(f'Ошибка при сохранении данных в файл: {exc}')


def main() -> None:
    '''Основная функция.'''
    data = get_data(URL)
    if data:
        save_to_file(data, FILE_PATH)


if __name__ == '__main__':
    main()
