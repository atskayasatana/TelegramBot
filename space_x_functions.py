import requests

from datetime import date, datetime, timedelta
from functions import download_img
from functions import parse_date
from urllib.parse import urlparse, unquote, urlencode


def get_foto_of_launch_by_id(url, launch_id):
    launch_url=f'{url}/{launch_id}'
    response = requests.get(launch_url)
    response.raise_for_status() 
    return response.json()['links']['flickr']['original']


def get_latest_launch_foto(url):
    launch_url=f'{url}/latest'
    response = requests.get(launch_url)
    response.raise_for_status() 
    return response.json()['links']['flickr']['original']


def get_launch_id(url):
    ids=[]
    end_year, end_month, end_day = parse_date(date.today())
    start_year, start_month, start_day = '2022', '01', '01'
    query = {'start': f'{start_year}-{start_month}-{start_day}',
             'end': f'{end_year}-{end_month}-{end_day}'
            }
    filter_value = urlencode(query)
    response = requests.get(url, params=filter_value)
    response.raise_for_status()
    for launch in response.json():
        if launch['links']['flickr']['original']:
            ids.append(launch['id'])   
    return ids[-1]


def fetch_spacex_launch_images(links, path):
    for num, link in enumerate(links):
        filename = f'spacex_{num}.jpg'
        download_path = path.joinpath(filename)
        download_img(link,download_path)
