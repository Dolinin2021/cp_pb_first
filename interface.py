import json

import ya_disk

import vk_classes

from ya_disk import YandexDisk

from vk_classes import VkUser


with open('ya_token.txt', 'r', encoding='utf-8') as file_yandex:
    token_yandex = file_yandex.read().strip()


with open('vk_token.txt', 'r', encoding='utf-8') as file_vk:
    token_vk = file_vk.read().strip()


main_menu = """
Главное меню:

/documentation - вывести дополнительное меню документации программы,

/get_photos – получить информацию о фотографиях пользователя Вконакте,

/create_vk_user_directory – создать папку на Яндекс.Диске с определённым именем,

/download_vk_user_file – загрузить файлы на Яндекс.Диск по определённому пути,

/exit_save_all - выйти из программы, предварительно сохранив данные в лог программы.

/exit_not_save - выйти из программы без сохранения данных.
"""


documentation = """
Документация программы:

/program_interface_doc - документация функции program_interface,

/VkUser_doc - документация класса VkUser,

/_error_validator_doc – документация метода _error_validator класса VkUser (является приватным),

/get_photos_doc – документация метода get_photos класса VkUser,

/YandexDisk_doc – документация класса YandexDisk,

/_error_validator_doc – документация метода _error_validator класса YandexDisk (является приватным),

/_create_directory_on_disk_doc – документация метода _create_directory_on_disk класса YandexDisk (является приватным),

/create_vk_user_directory_doc – документация метода create_vk_user_directory класса YandexDisk,

/_download_file_doc – документация метода _download_file класса YandexDisk (является приватным),

/download_vk_user_file_doc - документация метода download_vk_user_file класса YandexDisk,

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
    но на момент обращения эта переменная ещё не была объявлена.

    '''

    log_list = []

    vk_client = VkUser(token_vk, '5.131')

    yandex_disk = YandexDisk(token_yandex)

    print('Вас приветствует программа по работе с файлами компании Python Software.\n'
        'Ознакомьтесь с главным меню перед тем, как продолжить.')

    print(main_menu)


    while True:

        print()

        user_input = input('Введите команду: ')

        print()

        if user_input == '/documentation':
            print(documentation)

        elif user_input == '/program_interface_doc':
            print(program_interface.__doc__)

        elif user_input == '/VkUser_doc':
            print(vk_classes.VkUser.__doc__)

        elif user_input == '/_error_validator_doc':
            print(vk_classes.VkUser._error_validator.__doc__)

        elif user_input == '/get_photos_doc':
            print(vk_classes.VkUser.get_photos.__doc__)

        elif user_input == '/YandexDisk_doc':
            print(ya_disk.YandexDisk.__doc__)

        elif user_input == '/_error_validator_doc':
            print(ya_disk.YandexDisk._error_validator.__doc__)

        elif user_input == '/_create_directory_on_disk_doc':
            print(ya_disk.YandexDisk._create_directory_on_disk.__doc__)

        elif user_input == '/create_vk_user_directory_doc':
            print(ya_disk.YandexDisk.create_vk_user_directory.__doc__)

        elif user_input == '/_download_file_doc':
            print(ya_disk.YandexDisk._download_file.__doc__)

        elif user_input == '/download_vk_user_file_doc':
            print(ya_disk.YandexDisk.download_vk_user_file.__doc__)

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

                rev = int(input('Введите порядок сортировки (1 или 0): '))

                print()

                owner_id =  int(input('Введите идентификатор владельца альбома: '))

                print()

                photo_info = vk_client.get_photos(album_id, rev, owner_id)


            elif user_input == '/create_vk_user_directory':

                owner_id = int(input('Введите имя создаваемой папки: '))

                create = yandex_disk.create_vk_user_directory(owner_id)


            elif user_input == '/download_vk_user_file':

                owner_id = int(input('Введите имя папки, куда следует загрузить файл: '))

                download = yandex_disk.download_vk_user_file(owner_id, photo_info)


            elif user_input == '/exit_save_all':

                for log in photo_info:
                    log_list.append({'file_name': log['file_name'],
                                     'size': log['size']})

                with open('log_files.json', 'a', encoding='utf-8') as file_obj:
                    print()
                    print('Происходит сохранение данных в лог log_files.json, пожалуйста, подождите...')
                    json.dump(log_list, file_obj, ensure_ascii=False, indent=4)

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
                  'Программа продолжает работу в штатном режиме.\n')

        except UnboundLocalError:
            print()
            print('Возникло исключение UnboundLocalError.\n'
                  'Прежде,чем использовать метод download_vk_user_file() или кнопку exit_save_all, необходимо получить данные с помощью метода get_photos()\n'
                  'Программа продолжает работу в штатном режиме.\n')