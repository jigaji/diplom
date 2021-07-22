import requests
from pprint import pprint
import json
import datetime
import os
import yaDisk


with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()



def write_json(photo_info):
    try:
        data = json.load(open('photos.json'))
    except:
        data = []
    data.append(photo_info)

    with open('photos.json', 'w') as file:
        json.dump(data, file, indent=2)


def max_photo(sizes):
    if sizes['width'] <= sizes['height']:
        return sizes['height']
    elif sizes['width'] >= sizes['height']:
        return sizes['width']


def get_photo(version, user_id=None):
    photos_url = 'https://api.vk.com/method/photos.get'
    photos_params = {
        'v': version,
        'access_token': token,
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'count': 5
    }
    res = requests.get(url=photos_url, params=photos_params).json()
    return res


def main(version, user_id=None):
    os.mkdir('profile photo')
    all_photos = get_photo(version, user_id)['response']['items']
    filename = dict()
    for photo in all_photos:
        sizes = photo['sizes']
        max_size = max(sizes, key=max_photo)
        photo['sizes'] = max_size
        date = datetime.datetime.fromtimestamp(photo['date'])
        likes = photo['likes']['count']
        filename['file_name'] = str(likes) + '.jpg'
        photo_data = {**photo['sizes'], **filename}
        information_json = dict()
        information_json['file_name'] = photo_data['file_name']
        information_json['type'] = photo_data['type']
        write_json(information_json)
        response = requests.get(photo_data['url'])

        with open('profile photo/%s' % photo_data['file_name'], 'bw') as file:
            file.write(response.content)
    print('Фотографии профиля скачаны')

if __name__ == '__main__':
    main('5.131', 1)
    ya = yaDisk.YaDisk()
    ya.upload_file_to_disk('vk photo', 'profile photo')
    print(os.path.abspath('profile photo'))

