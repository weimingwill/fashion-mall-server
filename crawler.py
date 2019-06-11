import requests
import hashlib
import json
from helper import util, filename
from datetime import datetime
from bs4 import BeautifulSoup

HOST = 'http://localhost:5000/'
IMAGE_PATH = 'images/'
DATA_PATH = 'data/'

API_SECRET_KEY = 'www.mall.cycle.com'

BASE_URL = 'https://sujiefs.com/'
SUJIE_IMAGE_PATH = BASE_URL + 'update/images/'
WX_JS_CODE2SESSION = BASE_URL + '/api/wechat/jscode2session'
GET_USER_INFO = BASE_URL + '/api/userCenter/getUserInfo'
GET_HOME_DISCOVER_LIST = BASE_URL + '/api/mall/discoverList'
GET_AD_LIST = BASE_URL + '/api/adverts/list'
GET_AD_GOODS_LIST = BASE_URL + '/api/home/hostGoodsList'
GET_GOODS_LIST = BASE_URL + '/api/mall/searchGoodsList'
GET_GOODS_DETAL = BASE_URL + '/api/mall/goods'
FAVORITE_GOODS = BASE_URL + '/api/mall/goodsFavorite/add'
UNFAVORITE_GOODS = BASE_URL + '/api/mall/goodsFavorite/delete'
IS_GOODS_FAVORITE = BASE_URL + '/api/mall/goodsFavorite/goodsIsFavorite'
ADD_TO_CART = BASE_URL + '/api/mall/goodsCart/add'
GET_ROOT_CATEGORY_LIST = BASE_URL + '/api/mall/rootCtegoryList'
GET_CHILD_CATEGORY_LIST = BASE_URL + '/api/mall/childGoodsCatetoryList'
ADD_SEARCH_KEYWORD = BASE_URL + '/api/searchkeyword/add'
GET_SEARCH_KEYWORD_LIST = BASE_URL + '/api/searchkeyword/list'
CLEAR_SEARCH_KEYWORD = BASE_URL + '/api/searchkeyword/clear'

# Helper functions

def get_current_time():
    i = datetime.now()
    return i.strftime('%Y%m%d%H%M%S')

def get_signature():
    return hashlib.md5((get_current_time() + API_SECRET_KEY).lower().encode()).hexdigest()

def request(url, payload):
    headers = { 'Content-Type': 'application/json' }
    payload['sign'] = get_signature()
    payload['time'] = get_current_time()

    r = requests.get(url, headers=headers, params=payload)
    if r.status_code == 200:
        return r.json()
    else:
        print('request {} error, r: {}'.format(url, r))

# Image related

def image_name(path):
    return path.split('/')[-1]

def image_path(url):
    return IMAGE_PATH + image_name(url)

def new_image_url(url):
    return HOST + IMAGE_PATH + image_name(url)

def process_data_list_images(data, list_key, keys, download):
    for i in range(len(data[list_key])):
      for key in keys:
           data[list_key][i][key] = process_image_url(data[list_key][i][key], download)

def process_image_url(url, download):
    if download:
        util.download_image(url, image_path(url))
    return new_image_url(url)

# API Requests

def get_ad_list(download=False):
    data = request(GET_AD_LIST, {})
    process_data_list_images(data, 'list', ['picUrl'], download)
    return data

def get_discover_list(download=False):
    data = request(GET_HOME_DISCOVER_LIST, {'page': 1, 'size': 10})
    process_data_list_images(data, 'list', ['logo'], download)
    return data

def get_ad_goods_list(code, page, sort, download=False):
    data = request(GET_AD_GOODS_LIST, {
            'page': 1,
            'size': 10,
            'cateCode': code,
            'sort': 1,
            'skuval': ''
            })

    data['category']['logo'] = process_image_url(data['category']['logo'], download)
    process_data_list_images(data, 'list', ['logo', 'thumLogo'], download)
    return data

def get_goods_details(id, download=False):
    data = request(GET_GOODS_DETAL, {'id': id})
    data['data']['logo'] = process_image_url(data['data']['logo'], download)
    data['data']['thumLogo'] = process_image_url(data['data']['thumLogo'], download)
    process_data_list_images(data['data'], 'photoList', ['photo', 'thumPhoto'], download)
    detail = data['data']['detailInfo']
    soup = BeautifulSoup(detail, features="html.parser")
    images = soup.find_all('img')

    for image in images:
        if download:
            util.download_image(image['src'], image_path(image['src']))

    if len(images) > 0:
        src = images[0]['src']
        title = src.split('/')[-1]
        src = src.replace(title, '')
        detail = detail.replace(src, HOST + IMAGE_PATH)

    data['data']['detailInfo'] = detail
    return data

def get_root_category_list():
    data = request(GET_ROOT_CATEGORY_LIST, {})
    return data

def get_child_category_list(rootCode, download=False):
    data = request(GET_CHILD_CATEGORY_LIST, {'rootCategoryCode': rootCode})
    for i in range(len(data['list'])):
        data['list'][i]['secondCategory']['thumLogo'] = process_image_url(data['list'][i]['secondCategory']['thumLogo'], download)
    return data

def search_goods_list(keyword, categoryCode, page, sort, download=False):
    data = request(GET_GOODS_LIST, {
          'page': page,
          'size': 10,
          'searchKeyWords': keyword,
          'cateCode': categoryCode,
          'sort': sort,
          'skuval': ''
        })
    process_data_list_images(data, 'list', ['logo', 'thumLogo'], download)
    return data

# Extract data
def get_ids(data):
    ids = []
    for l in data['list']:
        ids.append(l['id'])
    return ids

def get_root_codes(data):
    codes = []
    for l in data['list']:
        codes.append(l['code'])
    return codes

def get_search_keywords(data):
    names = []
    for l in data['list']:
        names.append(l['name'])
    return names

def get_search_names(data):
    names = []
    for l in data['list']:
        names.append(l['secondCategory']['name'])
    return names


def get_search_codes(data):
    codes = []
    for l in data['list']:
        codes.append(l['secondCategory']['code'])
    return codes


if __name__ == "__main__":
    sorts = [-1, 1, 2, 3]
    pages = [1, 2]

    data = get_ad_list(download=True)
    util.save_data(filename.ad_list(), data)

    data = get_discover_list(download=True)
    util.save_data(filename.discover_list(), data)

    ids = []
    adsCodes = ['019', '020', '021', '022']
    for code in adsCodes:
        for page in pages:
            for sort in sorts:
                data = get_ad_goods_list(code, page, sort, download=True)
                ids.extend(get_ids(data))
                util.save_data(filename.ad_goods_list(code, page, sort), data)

    data = get_root_category_list()
    util.save_data(filename.root_category_list(), data)

    keywords = get_search_keywords(data)
    searchCodes = []

    rootCodes = get_root_codes(data)
    for code in rootCodes:
        data = get_child_category_list(code, download=True)
        keywords.extend(get_search_names(data))
        searchCodes.extend(get_search_codes(data))
        util.save_data(filename.child_category_list(code), data)

    for keyword in keywords:
        for page in pages:
            for sort in sorts:
                data = search_goods_list(keyword, '', page, sort, download=True)
                ids.extend(get_ids(data))
                util.save_data(filename.search_goods_list(keyword, '', page, sort), data)

    for code in searchCodes:
        for page in pages:
            for sort in sorts:
                data = search_goods_list('', code, page, sort, download=True)
                ids.extend(get_ids(data))
                util.save_data(filename.search_goods_list('', code, page, sort), data)

    for id in ids:
        data = get_goods_details(id, download=True)
        util.save_data(filename.goods_detail(id), data)
