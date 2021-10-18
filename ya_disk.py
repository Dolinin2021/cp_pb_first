import time

import json

import requests

from  tqdm  import  tqdm


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

    _create_directory_on_disk(path: str)
        создаёт папку на Яндекс.Диске. Является приватным методом.

    create_vk_user_directory(owner_id: int)
        создаёт папку на Яндекс.Диске по определённому пути.

    _download_file(path: str, url: str)
        загружает файл по url на Яндекс.Диск. Является приватным методом.

    download_vk_user_file(owner_id: int, list_name: str)
        загружает файл на Яндекс.Диск по определённому пути.


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
    Специальные исключения, которые возникают именно при работе с конкретным методом,
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


    def _create_directory_on_disk(self, path):
        '''
        Метод для создания папки на Яндекс.Диске. Является приватным методом.

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

    def create_vk_user_directory(self, owner_id):
        '''
        Метод для создания папки на Яндекс.Диске с определённым именем.

        Parameters
        ----------
        owner_id: int
            идентификатор владельца альбома.


        Результатом выполнения метода является создание директории на Яндекс.Диске по определённому пути (res_path).

        '''

        res_path = owner_id
        self._create_directory_on_disk(res_path)

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

            return response.json()

        else:
            print('Возникла непредвиденная ошибка. Программа завершает свою работу...')
            exit()


    def download_vk_user_file(self, owner_id, list_name):
        '''
        Метод для загрузки файлов на Яндекс.Диск по определённому пути.

        Parameters
        ----------
        owner_id: int
            идентификатор владельца альбома.

        list_name: list
            список словарей, содержащий информацию о фотографиях пользователя Вконтакте.


        Результатом выполнения метода является загрузка файлов на Яндекс.Диск по определённому пути (res_path).

        '''

        print()

        for photo in tqdm(list_name, desc='Идёт загрузка файлов на диск, пожалуйста, подождите ...', total=5, unit='S'):
            res_path = f"{owner_id}/{photo['file_name']}"
            self._download_file(res_path, photo['url'])
            time.sleep(1)

        print()
        print('Данные успешно загружены.')