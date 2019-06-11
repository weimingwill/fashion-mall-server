import os
import json
import requests
import shutil

IMAGE_PATH = 'images/'
DATA_PATH = 'data/'

def read_image(name):
    with open(IMAGE_PATH + name, "rb") as image:
        f = image.read()
        return bytearray(f)

def download_image(url, path):
    if os.path.isfile(path):
        print('image {} exist'.format(path))
        return

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def read_data(name):
    with open(DATA_PATH + name, 'r') as f:
        data = json.load(f)
        return data

def save_data(name, data):
    path = DATA_PATH + name
    if os.path.isfile(path):
        print('data {} exist'.format(path))
        return

    with open(path, 'w') as f:
        json.dump(data, f)
