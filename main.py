import requests
import json
import os
from urllib.parse import urlparse
from urllib.parse import urlunparse
from dotenv import load_dotenv


def shorten_link(headers, url):
    long_link = { 
        "long_url": f"{url}" 
        }
    post_response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', 
                                  headers=headers, json=long_link)
    post_response.raise_for_status()
    short_url = post_response.json()
    return short_url['id']


def count_clicks(url, headers):
    params = (
        ('unit', 'month'),
        ('units', '1'),
    )
    total_clicks = requests.get('https://api-ssl.bitly.com/v4/bitlinks/bit.ly/30WEPTX/clicks/summary',
                                 headers=headers)
    clicks_sum = total_clicks.json()
    return clicks_sum['total_clicks']         


def is_bitlink(url, headers):
    parsed_url = urlparse(url)
    parsed_netloc = parsed_url.netloc
    parsed_path = parsed_url.path
    link = f"{parsed_netloc}{parsed_path}".format(parsed_netloc, parsed_path)
    request_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(request_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    user_url = input('Введите ссылку: ')
    bitly_token = os.environ['BITLY_TOKEN']
    headers = {
        'Authorization': f'Bearer {bitly_token}'
    }
    
    try:
        if is_bitlink(user_url, headers):
            clicks = count_clicks(user_url, headers)
            print('Количество кликов ', clicks)
        else:
            bitlink = shorten_link(headers, user_url)
            print('Битлинк ', bitlink)
    except requests.exceptions.HTTPError:
        print('Ошибка! Вы ввели неправильную ссылку')
    

if __name__ == '__main__':
    main()