import os
import requests
class YaDisk:

    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

    def create_folder(self, disk_file_path):
        params = {"path": disk_file_path}
        requests.put(self.url, params=params, headers=self.headers)

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
