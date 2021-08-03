import requests
import json
import datetime
import yaDisk
import os

class Vk_photo:

    user_id = input('Введите ID пользователя VK: ')
    token = input('Введите VK token: ')
    url = 'https://api.vk.com/method/photos.get'
    if not os.path.exists('profile photo'):
        os.mkdir('profile photo')
    else:
        print('Папка с название profile photo уже существует')
    def write_json(self, data):
        with open('photos.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def main(self):
        res = requests.get(self.url, params={'v': 5.131,
                                             'access_token': self.token,
                                             'owner_id': self.user_id,
                                             'album_id': 'profile',
                                             'extended': 1,
                                             'photo_sizes': 1,
                                             'count': 5}).json()

        all_photos = res['response']['items']
        data_json = []
        name = []
        for photo in all_photos:
            max_size = photo['sizes'][-1]
            date = datetime.datetime.fromtimestamp(photo['date']).strftime('%d-%m-%Y-%H-%M-%S')
            likes = photo['likes']['count']
            if likes not in name:
                name.append(likes)
            else:
                name.append(f'{likes}-{date}')
            photo_data = {}
            for x in name:
                photo_data['file_name'] = f'{x}.jpg'
                photo_data['size'] = max_size['type']
            data_json.append(photo_data)
            self.write_json(data_json)
            download = requests.get(max_size['url'])
            with open('profile photo/%s' % photo_data['file_name'], 'bw') as file:
                file.write(download.content)

        print('Фотографии профиля скачаны в папку profile photo')

if __name__ == '__main__':
    Vk_photo().main()

    ya = yaDisk.YaDisk()
    ya.upload_file_to_disk('vk photo', 'profile photo')
