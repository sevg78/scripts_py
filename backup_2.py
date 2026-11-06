import os
from datetime import datetime
from progress.bar import Bar
import yadisk

TOKEN = 'your_token'
y = yadisk.YaDisk(token=TOKEN)

def backup(savepath: str, loadpath: str):
    """Резервное копирование папки на Яндекс.Диск"""
    date_folder = f"{os.path.basename(loadpath)}_{datetime.now().strftime('%Y.%m.%d-%H.%M.%S')}"
    try:
        y.mkdir(savepath)
    except:
        print(f"Папка {savepath} уже существует.")
    for address, _, files in os.walk(loadpath):
        remote_dir = f"{savepath}/{date_folder}{address.replace(loadpath, '').replace(os.sep, '/')}"
        y.mkdir(remote_dir)
        bar = Bar(f'Загрузка {os.path.basename(address)}', max=len(files))
        for file in files:
            local_file = os.path.join(address, file)
            remote_file = f"{remote_dir}/{file}"
            y.upload(local_file, remote_file)
            bar.next()
        bar.finish()

if __name__ == '__main__':
    if y.check_token():
        print("Токен валиден. Подключение успешно.")
        backup('Backup', os.getcwd())
    else:
        print("Ошибка: Токен недействителен.")
