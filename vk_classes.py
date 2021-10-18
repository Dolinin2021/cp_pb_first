import time

import json

import requests

from  tqdm  import  tqdm


class VkUser:
    '''
    Класс VkUser - используется для работы с аккаунтом ВКонтакте.

    Основное применение - обработка информации о конкретном пользователе.

    Attributes
    ----------
    token: str
        токен пользователя

    version: str
        используемая версия API Вконтакте


    Methods
    -------
    _error_validator(response: dict)
        обрабатывает возникающие ошибки.
        Является приватным методом.

    get_photos(album_id: str, rev: int, owner_id: int, extended: int, count: int)
        возвращает список фотографий в альбоме.

    '''

    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):

        self.params = {
            'access_token': token,
            'v': version
        }

    def _error_validator(self, response):
        '''
        Метод для обработки ошибок.
        Возвращает сообщение об ошибке и записывает возникающие ошибки в файл.
        Является приватным методом.


        Parameters
        ----------
        response: dict
            ответ сервера.


        В качестве возврата (return) метод использует логическое значение true либо false.

        '''

        for value in response.values():

            if 'error_code' in value:
                print(f"\nРабота метода была прервана ошибкой.\n"
                      f"Происходит обработка данных об ошибке, пожалуйста, подождите...\n"
                      f"\nКод ошибки: {value['error_code']}\n"
                      f"Сообщение об ошибке: \n{value['error_msg']}."
                      f"\n")

                with open('log_vk.json', 'a', encoding='utf-8') as file_obj:
                    print('Данные об ошибке сохранены в лог log_vk.json.')
                    json.dump(response, file_obj, ensure_ascii=False, indent=4)

                return True

            else:
                return False



    def get_photos(self, album_id, rev, owner_id, extended=1, count=5):
        '''
        Метод для формирования списка с информацией о фотографиях.

        Parameters
        ----------
        album_id: str
            индентификатор альбома.

        Для служебных альбомов используются следующие идентификаторы:
        wall — фотографии со стены,
        profile — фотографии профиля,
        saved — сохраненные фотографии.
        Возвращается только с ключом доступа пользователя в формате строки.


        rev: int
            порядок сортировки фотографий.

        Возможные значения:
        1 — антихронологический,
        0 — хронологический.
        Флаг может принимать значения 1 или 0.


        owner_id: int
            идентификатор владельца альбома.


        extended: int
            возвращает дополнительные поля.

        Возможные значения:

        Если был задан параметр extended=1, возвращаются дополнительные поля:
            likes — количество отметок Мне нравится и информация о том, поставил ли лайк текущий пользователь,
            comments — количество комментариев к фотографии,
            tags — количество отметок на фотографии,
            can_comment — может ли текущий пользователь комментировать фото (1 — может, 0 — не может),
            reposts — число репостов фотографии.

        Если был задан параметр extended=0, то дополнительные поля не будут отображены.
        По умолчанию равно 1.


        count: int
            количество записей, которое будет получено.
        Положительное число, по умолчанию 5, максимальное значение 1000.


        Exceptions
        ----------
        30 - This profile is private

        Данное исключение является специальным для данного метода.

        Общих исключений, которые могут возникнуть при работе с API VK, достаточно много,
        и более целесообразно привести на них ссылку в официальной документации: https://vk.com/dev/errors


        В качестве возврата (return) метод использует результирующий список с информацией о фотографиях (res_list).

        '''

        res_list = []

        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': owner_id,
            'rev': rev,
            'album_id': album_id,
            'extended': extended,
            'count': count
        }

        response = requests.get(get_photos_url, params={**self.params, **get_photos_params})

        if response.status_code >= 200 and response.status_code < 300:

            req = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()

            if self._error_validator(req) == False:
                print()

                for value in tqdm(req['response']['items'], desc='Происходит формирование списка с информацией о фото, пожалуйста, подождите...', total=5, unit='S'):
                    time.sleep(1)

                    photo_dict = {
                        'file_name': f"{value['likes']['count']}_{value['date']}.jpg",
                        'size': value['sizes'][-1]['type'],
                        'url': value['sizes'][-1]['url']
                    }

                    res_list.append(photo_dict)

                print()
                print('Данные успешно сформированы.')

                return res_list

            else:
                print('Программа продолжает работу в штатном режиме.\n')