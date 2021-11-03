import time

import json

import requests

from  tqdm  import  tqdm

from pprint import pprint


class YandexDisk:
    '''
    Класс YandexDisk - используется для работы с Яндекс.Диском.

    Основное применение - работа с файлами на Яндекс.Диске.

    Attributes
    ----------
    token: str
        OAuth - токен


    Methods
    -------
    get_headers()
        возвращает заголовки запроса.

    _error_validator(response: dict)
        обрабатывает возникающие ошибки. Является приватным методом.

    get_files_list()
        возвращает список файлов на Яндекс.Диске.

    create_directory_on_disk(path: str)
        создаёт папку на Яндекс.Диске.

    _download_file(path: str, url: str)
        загружает файл по url на Яндекс.Диск. Является приватным методом.

    download_vk_user_file(owner_id: int, list_name: str)
        загружает файл на Яндекс.Диск по определённому пути.

    delete_file_to_disk(path: str)
        удаляет файл на Яндекс.Диске.


    Exceptions
    ----------
    400	- Некорректные данные.

    401	- Не авторизован.

    403	- API недоступно. Ваши файлы занимают больше места, чем у вас есть.
    Удалите лишнее или увеличьте объём Диска.

    406	- Ресурс не может быть представлен в запрошенном формате.

    429	- Слишком много запросов.

    503	- Сервис временно недоступен.

    507	- Недостаточно свободного места.

    Эти исключения являются общими для используемых методов работы с Яндекс.Диском в данном классе.

    Специальные исключения, которые возникают при работе с конкретным методом,
    можно найти в документации к этим методам.

    '''

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _error_validator(self, response):
        '''
        Метод для обработки ошибок.
        Возвращает сообщение об ошибке и записывает возникающие ошибки в файл.

        Parameters
        ----------
        response: dict
            ответ сервера.


        В качестве возврата (return) метод использует логическое значение true либо false.

        '''

        if 'error' in response:

            print(f"\nРабота метода была прервана ошибкой. Происходит обработка ошибки, пожалуйста, подождите...\n"
                  f"Название ошибки: \n{response['error']}\n"
                  f"Сообщение об ошибке: \n{response['message']}\n"
                  f"Описание ошибки: \n{response['description']}\n")

            with open('log_yandex.json', 'a', encoding='utf-8') as file_obj:
                print('Данные об ошибке сохранены в лог log_yandex.json')
                json.dump(response, file_obj, ensure_ascii=False, indent=4)

            return True

        else:
            return False

    def get_files_list(self):
        '''
        Метод для получения списка файлов, упорядоченных по имени.

        Exceptions
        ----------
        403	- Недостаточно прав для изменения данных в общей папке.

        404 - Не удалось найти запрошенный ресурс.

        Данные исключения являются специальными для данного метода.


        В качестве возврата (return) метод использует список файлов на Яндекс.Диске.

        '''

        disk_file_list = []

        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url=files_url, headers=headers)
        req = response.json()

        for item in req['items']:

            disk_file_list.append({'file_name': item['name'], 'path': item['path']})

        return disk_file_list

    def create_directory_on_disk(self, path):
        '''
        Метод для создания папки на Яндекс.Диске.

        Parameters
        ----------
        path: str
            путь к создаваемой папке на Яндекс.Диске.


        Exceptions
        ----------
        404	- Не удалось найти запрошенный ресурс.

        409	- Ресурс "{path}" уже существует.

        423	- Ресурс заблокирован. Возможно, над ним выполняется другая операция.

        Данные исключения являются специальными для данного метода.


        В качестве возврата (return) метод использует ответ сервера в формате .json().

        '''

        create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(url=create_url, headers=headers, params=params)
        req = response.json()

        if self._error_validator(req) == False:

            print()
            print('Создание папки прошло успешно.')

            return req

        else:
            print('Программа продолжает работу в штатном режиме.\n')

    def _download_file(self, path, url):
        '''
        Метод для загрузки файлов по url на Яндекс.Диск. Является приватным методом.

        Parameters
        ----------
        path: str
            путь, куда будет помещён ресурс.

        url: str
            URL внешнего ресурса, который следует загрузить.


        Exceptions
        ----------
        409	- Указанного пути "{path}" не существует.

        Данное исключение является специальным для данного метода.


        В качестве возврата (return) метод использует ответ сервера в формате .json().

        '''

        download_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path, 'url': url}
        response = requests.post(url=download_url, headers=headers, params=params)
        req = response.json()

        if self._error_validator(req) == False:

            return req

        else:
            print('Возникла непредвиденная ошибка. Программа завершает свою работу...')
            exit()


    def download_vk_user_file(self, path, list_name):
        '''
        Метод для загрузки файлов на Яндекс.Диск по определённому пути.

        Parameters
        ----------
        path: str
            путь, куда будет помещён ресурс.

        list_name: list
            список словарей, содержащий информацию о фотографиях пользователя Вконтакте.


        Результатом выполнения метода является загрузка файлов на Яндекс.Диск по определённому пути (res_path).

        '''

        print()

        for info in tqdm(list_name, desc='Идёт загрузка файлов на Яндекс.Диск, пожалуйста, подождите ...', unit='S'):
            time.sleep(1)
            res_path = f"{path}/{info['file_name']}"
            self._download_file(res_path, info['url'])

        print()
        print('Данные успешно загружены.')

    def delete_file_to_disk(self, path, permanently=False):
        '''
        Метод для удаления файлов на Яндекс.Диске.

        Parameters
        ----------
        path: str
            путь к тому ресурсу, который нужно удалить.


        Exceptions
        ----------
        400	- Проверка md5 возможна только для файлов.

        404 - Не удалось найти запрошенный ресурс.

        409 - Ресурс "{path}" уже существует.

        423 - Ресурс заблокирован. Возможно, над ним выполняется другая операция.

        Данные исключения являются специальными для данного метода.


        По умолчанию удаляет ресурс в Корзину.
        Чтобы удалить ресурс не помещая в корзину, следует указать параметр permanently=true.
        Если удаление происходит асинхронно, то вернёт ответ со статусом 202 и ссылкой на асинхронную операцию.
        Иначе вернёт ответ со статусом 204 и пустым телом.

        '''

        delete_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": path, "permanently": permanently}
        response = requests.delete(url=delete_url, headers=headers, params=params)
        return response.status_code