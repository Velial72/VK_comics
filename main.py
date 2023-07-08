import os
import requests
import random
from dotenv import load_dotenv


def get_comics_quantity():
    url = f'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_quantity = response.json()['num']
    return comics_quantity


def get_comics():
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    random_comics = response.json()
    comics_url = random_comics['img']
    comment = random_comics['alt']
    return comics_url, comment


def save_image(url):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def publish_pic(owner_id, picture_id, group_id, token):
    picture = f"photo{owner_id}_{picture_id}"
    payload = {
        'access_token': token,
        'owner_id': f'-{group_id}',
        'message': comment,
        'attachments': picture,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    response.raise_for_status()


def save_pic_to_album(photo_server, photo, photo_hash, group_id, token):
    payload = {
        'group_id': group_id,
        'server': photo_server,
        'photo': photo,
        'hash': photo_hash,
        'access_token': token,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    params_of_picture = response.json()['response'][0]
    owner_id = params_of_picture['owner_id']
    picture_id = params_of_picture['id']
    return owner_id, picture_id


def send_pic_to_serv(url, token, group_id):
    with open(filename, 'rb') as file:
        files = {
            'access_token': token,
            'group_id': group_id,
            'photo': file
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    photo_to_save = response.json()
    photo_server = photo_to_save['server']
    photo = photo_to_save['photo']
    photo_hash = photo_to_save['hash']
    return photo_server, photo, photo_hash


def get_server_url(group_id, token):
    payload = {
        'group_id': group_id,
        'access_token': token,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    upload_server = response.json()['response']['upload_url']
    return upload_server


if __name__ == '__main__':
    load_dotenv()
    number = random.randint(1, get_comics_quantity())
    filename = 'comics.png'
    vk_token = os.getenv("VK_TOKEN")
    group_id = os.getenv("VK_GROUP_ID")

    comics_url, comment = get_comics()
    save_image(comics_url)
    try:
        upload_server = get_server_url(group_id, vk_token)
        photo_to_save = send_pic_to_serv(upload_server, group_id, vk_token)
        params_of_picture = save_pic_to_album(*photo_to_save, group_id, vk_token)
        publish_pic(*params_of_picture, group_id, vk_token)
    except ValueError:
        print("Environment variables error!")
    finally:
        os.remove('comics.png')
