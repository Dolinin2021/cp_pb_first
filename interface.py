import json

import google_drive as google

from ya_disk import YandexDisk

from vk_classes import VkUser

from pprint import pprint


with open('ya_token.txt', 'r', encoding='utf-8') as yandex_file:
    yandex_token = yandex_file.read().strip()

with open('vk_token.txt', 'r', encoding='utf-8') as vk_file:
    vk_token = vk_file.read().strip()


main_menu = """
Главное меню:

/docs - вывести дополнительное меню документации программы.


Класс VkUser:

/get_photos – получить информацию о фотографиях пользователя (пользователей) Вконтакте,

/get_albums - получить информацию о фотоальбомах пользователя (пользователей) Вконтакте.


Класс YandexDisk:

/create_directory_yandex_disk – создать папку на Яндекс.Диске с определённым именем,

/download_photos_yandex_disk – загрузить фото на Яндекс.Диск по определённому пути.


Функционал для работы с Google.Drive:

/create_directory_google_drive - создать папку на Google.Drive с определённым именем,

/download_photos_google_drive - загрузить фото на Google.Drive по определённому пути (задан по умолчанию).


/exit_save_all - выйти из программы, предварительно сохранив данные в лог программы.

/exit_not_save - выйти из программы без сохранения данных.
"""

documentation = """
Документация программы:

/program_interface_doc - документация функции program_interface.


Класс VkUser (документация):

/VkUser_doc - документация класса VkUser,

/_error_validator_doc – документация метода _error_validator (является приватным),

/users_get_doc - документация метода users_get,

/get_albums_doc - документация метода get_albums,

/get_photos_doc – документация метода get_photos.


Класс YandexDisk (документация):

/YandexDisk_doc – документация класса YandexDisk,

/_error_validator_doc – документация метода _error_validator (является приватным),

/get_files_list_doc – документация метода get_files_list,

/create_directory_yandex_disk_doc – документация метода create_directory_yandex_disk,

/_download_files_doc – документация метода _download_files (является приватным),

/download_files_yandex_disk_doc - документация метода download_files_yandex_disk,

/delete_files_yandex_disk_doc - документация метода delete_files_yandex_disk.


Функционал для работы с Google.Drive (документация):

/authorization_doc - документация функции authorization,

/get_files_google_drive_doc - документация функции get_files_google_drive,

/create_directory_google_drive_doc - документация функции create_directory_google_drive,

/download_files_google_drive_doc - документация функции download_files_google_drive,

/delete_files_google_drive_doc - документация функции delete_files_google_drive.


/back - вернуться в главное меню.
"""


def program_interface():
    '''
    Функция, реализующая интерфейс программы.

    Exceptions
    ----------
    ValueError - возникает при несоответствии типов
    (при вводе ожидался тип int, а был принят на вход тип str),
    либо при отсутствии значения на этапе ввода данных,
    либо при несоблюдении принятого формата ввода данных.

    TypeError - возникает при передаче пустого значения
    служебной переменной или аргумента в какой-либо метод,
    либо цикл.

    UnboundLocalError - возникает при текущем обращении к методам,
    которые требуют в качестве аргумента переменную,
    но на момент обращения эта переменная не была объявлена.

    '''

    log_photos_list = []

    log_albums_list = []


    temp_photos_list = []

    temp_albums_list = []

    google_drive_files_list = []


    temp_photos_set = set()

    disk_files_set = set()

    delete_files_set = set()


    vk_client = VkUser(vk_token, '5.131')

    yandex_disk = YandexDisk(yandex_token)

    service = google.authorization()


    print('Вас приветствует программа по работе с файлами компании Python Software.\n'
        'Ознакомьтесь с главным меню перед тем, как продолжить.')

    print(main_menu)


    while True:

        print()

        user_input = input('Введите команду: ')

        print()

        if user_input == '/docs':
            print(documentation)

        elif user_input == '/program_interface_doc':
            print(program_interface.__doc__)

        elif user_input == '/VkUser_doc':
            print(VkUser.__doc__)

        elif user_input == '/_error_validator_doc':
            print(VkUser._error_validator.__doc__)

        elif user_input == '/users_get_doc':
            print(VkUser.users_get.__doc__)

        elif user_input == '/get_albums_doc':
            print(VkUser.get_albums.__doc__)

        elif user_input == '/get_photos_doc':
            print(VkUser.get_photos.__doc__)

        elif user_input == '/YandexDisk_doc':
            print(YandexDisk.__doc__)

        elif user_input == '/_error_validator_doc':
            print(YandexDisk._error_validator.__doc__)

        elif user_input == '/get_files_list_doc':
            print(YandexDisk.get_files_list.__doc__)

        elif user_input == '/create_directory_yandex_disk_doc':
            print(YandexDisk.create_directory_yandex_disk.__doc__)

        elif user_input == '/_download_files_doc':
            print(YandexDisk._download_files.__doc__)

        elif user_input == '/download_files_yandex_disk_doc':
            print(YandexDisk.download_files_yandex_disk.__doc__)

        elif user_input =='/delete_files_yandex_disk_doc':
            print(YandexDisk.delete_files_yandex_disk.__doc__)

        elif user_input == '/authorization_doc':
            print(google.authorization.__doc__)

        elif user_input == '/get_files_google_drive_doc':
            print(google.get_files_google_drive.__doc__)

        elif user_input == '/create_directory_google_drive_doc':
            print(google.create_directory_google_drive.__doc__)

        elif user_input == '/download_files_google_drive_doc':
            print(google.download_files_google_drive.__doc__)

        elif user_input == '/delete_files_google_drive_doc':
            print(google.delete_files_google_drive.__doc__)

        elif user_input == '/back':
            print(main_menu)

        elif user_input == '/exit_not_save':

            print()
            print('Python Software, 2021. Все права защищены.')

            break


        try:

            if user_input == '/get_photos':

                album_id = str(input('Введите индентификатор альбома (wall, profile, saved): '))

                print()

                rev = int(input('Введите порядок сортировки (1 — антихронологический, 0 — хронологический): '))

                print()

                user_ids = str(input('Введите имя пользователя (или пользователей через запятую) (screen_name): '))

                print()

                count = int(input('Введите количество запрашиваемых фотографий: '))

                print()

                owner_id = vk_client.users_get(user_ids)

                for id in owner_id:

                    photo_info = vk_client.get_photos(album_id, rev, id['id'], count)

                    temp_photos_list.append(photo_info)

                    if photo_info is None:

                        print('Нет данных для сохранения.')

                    else:

                        for log_photos in photo_info:

                            log_photos_list.append({'file_name': log_photos['file_name'], 'size': log_photos['size']})

                    print('\nСписок файлов пользователя (пользователей):\n')

                    pprint(temp_photos_list)


            elif user_input == '/get_albums':

                print()

                user_ids = str(input('Введите имя пользователя (или пользователей через запятую) (screen_name): '))

                print()

                count = int(input('Введите количество запрашиваемых альбомов: '))

                print()

                owner_id = vk_client.users_get(user_ids)

                for id in owner_id:

                    albums_info = vk_client.get_albums(id['id'], count)

                    if albums_info is None:

                        print('Нет данных для сохранения.')

                    else:

                        temp_albums_list.append(albums_info)

                        log_albums_list.append(albums_info)

                        print()

                        print('\nСписок альбомов пользователя:\n')

                        pprint(temp_albums_list)

                        temp_albums_list.clear()


            elif user_input == '/create_directory_yandex_disk':

                path = str(input('Введите имя создаваемой папки: '))

                create = yandex_disk.create_directory_yandex_disk(path)


            elif user_input == '/download_photos_yandex_disk':

                get_files_list = yandex_disk.get_files_list()


                for get in get_files_list:

                    disk_files_set.add(get['file_name'])


                path = str(input('\nВведите имя папки, куда следует загрузить файл: '))


                for info in temp_photos_list:

                    for value in info:

                        if value['file_name'] in disk_files_set:

                            delete_files_set.add(value['file_name'])


                for file_name in delete_files_set:

                    delete = yandex_disk.delete_files_yandex_disk(f"{path}/{file_name}")


                for load in temp_photos_list:

                    download = yandex_disk.download_files_yandex_disk(path, load)


                disk_files_set.clear()

                delete_files_set.clear()

                temp_photos_list.clear()


            elif user_input == '/create_directory_google_drive':

                name = str(input('Введите имя создаваемой папки: '))

                create = google.create_directory_google_drive(service, name)


            elif user_input == '/download_photos_google_drive':

                get_files_list_on_google_disk = google.get_files_google_drive(service)

                for get in get_files_list_on_google_disk:

                    google_drive_files_list.append(

                        {
                            'id': get['id'],
                            'file_name': get['name']
                        }

                    )


                for info in temp_photos_list:

                    for value in info:

                        temp_photos_set.add(value['file_name'])


                for value in google_drive_files_list:

                    if value['file_name'] in temp_photos_set:

                        delete_files_set.add(value['id'])


                for fileId in delete_files_set:

                    delete = google.delete_files_google_drive(service, fileId)


                for load in temp_photos_list:

                    download = google.download_files_google_drive(service, load)


                google_drive_files_list.clear()

                temp_photos_list.clear()

                temp_photos_set.clear()

                delete_files_set.clear()


            elif user_input == '/exit_save_all':

                with open('log_photos.json', 'w', encoding='utf-8') as file_obj:
                    print()
                    print('Происходит сохранение данных о фото в лог log_photos.json, пожалуйста, подождите...')
                    json.dump(log_photos_list, file_obj, ensure_ascii=False, indent=4)

                with open('log_albums.json', 'w', encoding='utf-8') as file_obj:
                    print()
                    print('Происходит сохранение данных об альбомах в лог log_albums.json, пожалуйста, подождите...')
                    json.dump(log_albums_list, file_obj, ensure_ascii=False, indent=4)

                print()
                print('Данные успешно сохранены.')
                print()
                print('Python Software, 2021. Все права защищены.')

                break


        except ValueError:
            print()
            print('Возникло исключение ValueError: несоответствие типов при вводе данных.\n'
                  'Программа продолжает работу в штатном режиме.\n')

        except TypeError:
            print()
            print('Возникло исключение TypeError: передано пустое значение служебной переменной или аргумента.\n'
                  'Программа завершает свою работу...\n')
            exit()

        except UnboundLocalError:
            print()
            print('Возникло исключение UnboundLocalError.\n'
                  'Прежде,чем использовать метод download_files_yandex_disk или кнопку exit_save_all, необходимо получить данные с помощью метода get_photos()\n'
                  'Программа продолжает работу в штатном режиме.\n')
