import os
import requests
import random
from dotenv import load_dotenv


def get_comics_api():
    global comment
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    api_comics = response.json()['img']
    comment = response.json()['alt']
    save_image(api_comics)


def save_image(url):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def delete_file():
    os.remove('comics.png')


def public_pic(picture, group_id, token):
    pic_params = f"photo{picture['owner_id']}_{picture['id']}"
    payload = {
        'access_token': token,
        'owner_id': f'-{group_id}',
        'message': comment,
        'attachments': pic_params,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    response.raise_for_status()


def save_pic_to_album(pic, group_id, token):
    payload = {
        'group_id': group_id,
        'server': pic['server'],
        'photo': pic['photo'],
        'hash': pic['hash'],
        'access_token': token,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    params_of_picture = response.json()['response'][0]
    public_pic(params_of_picture, GROUP_ID, VK_TOKEN)


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
    save_pic_to_album(photo_to_save, GROUP_ID, VK_TOKEN)


def get_server(group_id, token):
    payload = {
        'group_id': group_id,
        'access_token': token,
        'v': 5.131
    }
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    upload_server = response.json()['response']['upload_url']
    send_pic_to_serv(upload_server, GROUP_ID, VK_TOKEN)


if __name__ == '__main__':
    load_dotenv()
    number = random.randint(1, 1000)
    filename = 'comics.png'
    comment = ''
    VK_TOKEN = os.getenv("VK_TOKEN")
    GROUP_ID = os.getenv("VK_GROUP_ID")

    get_comics_api()
    get_server(GROUP_ID, VK_TOKEN)
    delete_file()
