import os
import requests
from datetime import datetime


TOKEN = 'your_token'
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'OAuth {TOKEN}'
}

def create_folder(path: str):
    """Создаёт папку на Яндекс.Диске"""
    requests.put(f'{URL}?path={path}', headers=headers)

def upload_file(loadfile: str, savefile: str, replace: bool = False):
    """Загружает файл на Яндекс.Диск"""
    res = requests.get(
        f'{URL}/upload?path={savefile}&overwrite={replace}',
        headers=headers
    ).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file': f})
        except KeyError:
            print('Ошибка:', res)


def backup(savepath: str, loadpath: str):
    """Резервное копирование папки на Яндекс.Диск"""
    date_folder = f"{os.path.basename(loadpath)}_{datetime.now().strftime('%Y.%m.%d-%H.%M.%S')}"
    create_folder(savepath)
    for address, _, files in os.walk(loadpath):
        remote_dir = f"{savepath}/{date_folder}{address.replace(loadpath, '').replace(os.sep, '/')}"
        create_folder(remote_dir)
        print(f'Загрузка {os.path.basename(address)}')
        for file in files:
            local_file = os.path.join(address, file)
            remote_file = f"{remote_dir}/{file}"
            upload_file(local_file, remote_file)
            
        
if __name__ == '__main__':
    backup('Backup', os.getcwd())
    