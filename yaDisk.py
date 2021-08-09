import os
import requests


class YaDisk:

    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def create_folder(self, disk_file_path, token):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        params = {"path": disk_file_path}
        new_folder = requests.put(self.url, params=params, headers=headers)
        new_folder.raise_for_status()
        if new_folder.status_code == 201:
            print('Папка успешно создана на Яндекс.Диск')
        else:
            print('Папка с таким именем уже существует на Яндекс.Диске')

    def get_upload_link(self, save_path, token):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        params = {"path": save_path, "overwrite": "false"}
        response = requests.get(f'{self.url}/upload', headers=headers, params=params).json()
        return response['href']


    def upload_file_to_disk(self, save_path, load_path, token):
        self.create_folder(save_path, token=token)
        for root, folders, files in os.walk(load_path):
            for img in files:
                res = self.get_upload_link(f'{save_path}/{img}', token=token)
                upload = requests.put(res, data=open(os.path.join(load_path, img), 'rb'))
                upload.raise_for_status()
                if upload.status_code == 201:
                    print(f'Фотография успешно загружена в папку {save_path} на Яндекс Диск')
                else:
                    print('Ошибка при загрузке фотографии на Яндекс.Диск')
