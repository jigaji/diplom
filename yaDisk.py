import os
import requests
class YaDisk:
    print('Предлагаем вам сделать резервную копию фотографий профиля пользователя VK в облачное хранилище Яндекс.Диск.'
          ' Для этого вам нужно будет ввести следующие данные:')
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    token = input('Введите YandexDisk API token: ')
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

    def create_folder(self, disk_file_path):
        params = {"path": disk_file_path}
        new_folder = requests.put(self.url, params=params, headers=self.headers)
        new_folder.raise_for_status()
        if new_folder.status_code == 201:
            print('Папка успешно создана на Яндекс.Диск')
        else:
            print('Папка с таким именем уже существует на Яндекс.Диске')

    def upload_file(self, save_path):
        params = {"path": save_path, "overwrite": "false"}
        response = requests.get(f'{self.url}/upload', headers=self.headers, params=params)
        return response.json()


    def upload_file_to_disk(self, save_path, load_path):
        self.create_folder(save_path)
        for root, folders, files in os.walk(load_path):
            for img in files:
                res = self.upload_file(f'{save_path}/{img}')
                try:
                    upload = requests.put(res['href'], data=open(os.path.join(load_path, img), 'rb'))
                except KeyError:
                    print(res)
        upload.raise_for_status()
        if upload.status_code == 201:
            print(f'Фотошрафии успешно загружены в папку {save_path} на Яндекс Диск')
        else:
            print('Ошибка при загрузке фотографий на Яндекс.Диск')
