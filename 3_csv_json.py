import csv
import json

CSV_FILE_PATH = 'products.csv'
JSON_FILE_PATH = 'sales.json'


def read_csv(file_path: str) -> list[dict[str, str]]:
    '''Читает CSV-файл и возвращает список словарей.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def read_json(file_path: str) -> list[dict[str, str]]:
    '''Читает JSON-файл и возвращает список словарей.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def merge_data(
    products: list[dict[str, str]], sales: list[dict[str, str]]
) -> list[dict[str, str]]:
    '''Объединяет данные по product_id и возвращает итоговую таблицу.'''
    product_dict = {
        int(product['product_id']): product['product_name']
        for product in products
    }
    return [
        {
            'product_id': sale['product_id'],
            'product_name': product_dict[sale['product_id']],
            'sale_id': sale['sale_id'],
            'amount': sale['amount']
        }
        for sale in sales if sale['product_id'] in product_dict
    ]


def main() -> None:
    '''Основная функция.'''
    products = read_csv(CSV_FILE_PATH)
    sales = read_json(JSON_FILE_PATH)
    merged_data = merge_data(products, sales)
    for data in merged_data:
        print(
            f'ID продукта: {data['product_id']}, '
            f'Название продукта: {data['product_name']}, '
            f'ID продажи: {data['sale_id']}, '
            f'Количество: {data['amount']}'
        )


if __name__ == '__main__':
    main()
