import time

import json

import requests

from  tqdm  import  tqdm

from pprint import pprint


class VkUser:
    '''
    Класс VkUser - используется для работы с аккаунтом ВКонтакте.

    Основное применение - обработка информации о конкретном пользователе (пользователях).

    Attributes
    ----------
    token: str
        токен пользователя

    version: str
        используемая версия API Вконтакте


    Methods
    -------
    _error_validator(response: dict)
        обрабатывает возникающие ошибки. Является приватным методом.

    users_get(user_ids: str)
        возвращает расширенную информацию о пользователях.

    get_albums(owner_id: int, count: int)
        возвращает список фотоальбомов пользователя (или нескольких пользователей).

    get_photos(album_id: str, rev: int, owner_id: int, extended: int, count: int)
        возвращает список фотографий в альбоме.


    Exceptions
    ----------
    Общих исключений, которые могут возникнуть при работе с API VK, достаточно много,
    и более целесообразно привести на них ссылку в официальной документации: https://vk.com/dev/errors

    Специальные исключения, которые возникают при работе с конкретным методом,
    можно найти в документации к этим методам.

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

    def users_get(self, user_ids):
        '''
        Метод, который возвращает расширенную информацию о пользователях.

        Parameters
        ----------
        user_ids: str
            перечисленные через запятую идентификаторы пользователей или их короткие имена (screen_name).


        Exceptions
        ----------
        При работе с данным методом возникают только общие исключения.

        '''

        res_user_list = []

        users_get_url = self.url + 'users.get'

        users_get_params = {
            'user_ids': user_ids
        }

        response = requests.get(users_get_url, params={**self.params, **users_get_params})

        if response.status_code >= 200 and response.status_code < 300:

            req = response.json()

            if self._error_validator(req) == False:

                for value in req.values():

                    for info in value:

                        user_dict = {
                            'id': info['id'],
                            'last_name': info['last_name'],
                            'first_name': info['first_name'],
                            'is_closed': info['is_closed'],
                            'can_access_closed': info['can_access_closed']
                        }

                        res_user_list.append(user_dict)

                pprint(res_user_list)

                print()

                return res_user_list

            else:
                print('Программа продолжает работу в штатном режиме.\n')

    def get_albums(self, owner_id, count):
        '''
        Возвращает список фотоальбомов пользователя или сообщества.

        Parameters
        ----------
        owner_id: int
            идентификатор пользователя или сообщества, которому принадлежат альбомы.

        count: int
            количество альбомов, которое нужно вернуть.

        Exceptions
        ----------
        30 - This profile is private

        Данное исключение является специальным для данного метода.


        В качестве возврата (return) метод использует результирующий список с информацией о фотоальбомах (res_albums_list).

        '''

        res_albums_list = []

        get_albums_url = self.url + 'photos.getAlbums'

        get_albums_params = {
            'owner_id': owner_id,
            'count': count
        }

        response = requests.get(get_albums_url, params={**self.params, **get_albums_params})

        if (response.status_code >= 200 and response.status_code < 300):

                req = response.json()

                if self._error_validator(req) == False:

                    for value in tqdm(req['response']['items'], desc='Происходит формирование списка с информацией об альбомах, пожалуйста, подождите...', unit='S'):

                        time.sleep(1)

                        album_dict = {
                            'title': value['title'],
                            'user_id': value['owner_id'],
                            'id': value['id'],
                            'size': value['size'],
                            'description': value['description']
                        }

                        res_albums_list.append(album_dict)

                    print()
                    print('Данные успешно сформированы.')
                    print()

                    return res_albums_list

                else:
                    print('Программа продолжает работу в штатном режиме.\n')



    def get_photos(self, album_id, rev, owner_id, count, extended=1):
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
        Максимальное значение 1000.


        Exceptions
        ----------
        30 - This profile is private

        Данное исключение является специальным для данного метода.


        В качестве возврата (return) метод использует результирующий список с информацией о фотографиях (res_photos_list).

        '''

        res_photos_list = []

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

            req = response.json()

            if self._error_validator(req) == False:

                print()

                for value in tqdm(req['response']['items'], desc='Происходит формирование списка с информацией о фото, пожалуйста, подождите...', unit='S'):

                    time.sleep(1)

                    photo_dict = {
                        'file_name': f"{value['likes']['count']}_{value['date']}.jpg",
                        'size': value['sizes'][-1]['type'],
                        'url': value['sizes'][-1]['url']
                    }

                    res_photos_list.append(photo_dict)

                print()
                print('Данные успешно сформированы.')
                print()

                return res_photos_list

            else:
                print('Программа продолжает работу в штатном режиме.\n')