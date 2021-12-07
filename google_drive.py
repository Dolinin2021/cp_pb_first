from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
from  tqdm  import  tqdm
import requests
import os.path
import time
import io


# Если вы изменяете область доступа, удалите файл token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def authorization():
    '''
    Функция, обеспечивающая авторизацию пользователя и вход в систему.
    '''

    creds = None

    # Файл token.json хранит токены доступа и обновления пользователя,
    # он создается автоматически, когда поток авторизации завершается.

    if os.path.exists('./token.json'):
        creds = Credentials.from_authorized_user_file('./token.json', SCOPES)

    # Если нет доступных (действительных) учетных данных, позвольте пользователю войти в систему.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохранение учетных данных для следующего запуска.

        with open('./token.json', 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    return service


def get_files_google_drive(service):
    '''
    Функция для получения списка файлов на Google.Drive.

    Parameters
    ----------
    service
        сервис, который будет использовать 3ю версию REST API Google.Drive,
        отправляя запросы из-под учетных данных credentials.

    pageSize: int
        количество результатов выдачи

    fields: дополнительные поля

        nextPageToken: str
            токен следующей страницы, если все результаты не помещаются в один ответ.

        files()
            параметр, указывающий, что нужно возвращать список файлов,
            где в скобках указан список полей для файлов, которые нужно показывать в результатах выдачи.

            В данном случае указаны поля для файлов:
            id - идентификатор файла,
            name - имя файла,
            mimeType - тип файла,
            parents — ID папки, в которой расположен файл/подпапка,
            createdTime — дата создания файла/папки.

            Со всеми возможными полями можно ознакомиться в документации
            (https://developers.google.com/drive/api/v3/reference/files) в разделе «Valid fields for files.list».

    pageToken: str
        токен страницы с результатом запроса.

    В качестве возврата (return) функция использует список с информацией о файлах на Google.Drive.

    '''

    # Вызов API Drive v3

    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType, parents, createdTime)").execute()
    nextPageToken = results.get('nextPageToken')

    while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']

    return results.get('files')


def create_directory_google_drive(service, name):
    '''
    Функция для создания папок на Google.Drive.

    Parameters
    ----------
    service
        сервис, который будет использовать 3ю версию REST API Google.Drive,
        отправляя запросы из-под учетных данных credentials.

    name: str
        имя создаваемой папки.

    Результатом работы функции является создание новой директории на Google.Drive.

    '''

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()

    print()
    print('Создание папки прошло успешно')
    print()
    print('Folder ID: %s' % file.get('id'))


def download_files_google_drive(service, list_name):
    '''
    Функция для загрузки файлов на Google.Drive.

    Parameters
    ----------
    service
        сервис, который будет использовать 3ю версию REST API Google.Drive,
        отправляя запросы из-под учетных данных credentials.

    list_name: list
        список с информацией о загружаемых файлах.

    Результатом работы функции является загрузка файлов на Google.Drive.

    '''

    folder_id = '1Y0u2CF44I3Ewx5C63UAsXBXeKEk4wPjZ'

    print()

    for info in tqdm(list_name, desc='Идёт загрузка файлов на Google.Drive, пожалуйста, подождите ...', unit='S'):
        time.sleep(1)
        response = requests.get(info['url'])
        file_content = io.BytesIO(response.content)
        file_metadata = {'name': f"{info['file_name']}", 'parents': [folder_id]}
        media = MediaIoBaseUpload(file_content, mimetype='image/jpeg')
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print()
    print('Данные успешно загружены.')


def delete_files_google_drive(service, fileId):
    '''
    Функция для удаления файлов на Google.Drive.

    Parameters
    ----------
    service
        сервис, который будет использовать 3ю версию REST API Google.Drive,
        отправляя запросы из-под учетных данных credentials.

    fileId: str
        индентификатор файла.

    Результатом работы функции является удаление файла на Google.Drive.

    '''

    service.files().delete(fileId=fileId).execute()
