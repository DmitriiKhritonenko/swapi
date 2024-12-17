# Подключаем библиотеки, необходимые для реализации проекта swapi.
from pathlib import Path
import requests

# Создаем базовый класс, который позволит хранить некоторый базовый url,
# а также отрабатывать составные запросы методом get


class APIRequester():

    # Конструктор класса. Проверяет наличие / на конце пути,
    # т.к. потенциально это проблема для отработки запросов
    def __init__(self, base_url: str):
        if base_url[-1] == '/':
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url

    # Расширенная get функция с проверкой исключений. Может вернуть ошибку.
    def get(self, url_append: str = '/'):
        try:
            response = requests.get(f'{self.base_url}{url_append}')
            response.raise_for_status()
            return response
        except requests.ConnectionError:
            print('Возникла ошибка при выполнении запроса')
            return response
        except requests.HTTPError:
            print('Возникла ошибка при выполнении запроса')
            return response
        except requests.RequestException as e:
            print('Возникла ошибка при выполнении запроса')
            return e

# Дочерний класс к APIRequester, содержит методы получения списка категорий
# и текстовой информации с сайта


class SWRequester(APIRequester):

    # Метод используемый для получения списка категорий сайта.
    # Обрабатывает некоторые исключения. Результат - список
    def get_sw_categories(self):
        try:
            response = self.get()
            response.raise_for_status()
            return response.json().keys()
        except requests.HTTPError:
            return response
        except requests.RequestException as e:
            return e

    # Формирует и отрабатывает запрос к конкретной категории.
    # Возвращает результат в ввиде текста
    def get_sw_info(self, sw_type):
        response = self.get(url_append=f'/{sw_type}/')
        if response:
            return response.text

# Функция создает новую директорию data, куда помещает данные в соответствующие
# файлы: data/<имя категории>.txt


def save_sw_data(url='https://swapi.dev/api'):
    Path("data").mkdir(exist_ok=True)

    r = SWRequester(url)
    cat_list = r.get_sw_categories()
    for cat_s in cat_list:
        str_result = r.get_sw_info(cat_s)

        with open(f'data/{cat_s}.txt', 'w') as f:
            f.write(str_result)


# В конце просто вызываем написанную функцию :)
if __name__ == '__main__':
    save_sw_data('https://swapi.py4e.com/api/')
