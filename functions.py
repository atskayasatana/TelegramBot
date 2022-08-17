import os
import requests
import urllib

from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode


def parse_date(date):
    year = str(date.year)
    month = str(date.month) if date.month > 9 else '0'+str(date.month)
    day = str(date.day) if date.day > 9 else '0'+str(date.day)
    return year, month, day


def download_img(img_url, download_path):
    response = requests.get(img_url)
    response.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(response.content)
    
    
def get_foto_of_launch_by_id(url, launch_id):
    launch_url = f'{url}/{launch_id}'
    response = requests.get(launch_url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def get_latest_launch_foto(url):
    launch_url = f'{url}/latest'
    response = requests.get(launch_url)
    response.raise_for_status() 
    return response.json()['links']['flickr']['original']


def get_launch_id(url):
    ids = []
    end_year, end_month, end_day = parse_date(date.today())
    start_year, start_month, start_day = '2022', '01', '01'
    filter_value = (f'start={start_year}-{start_month}-{start_day}'
                    f'&end={end_year}-{end_month}-{end_day}')
    launch_url = f'{url}?{filter_value}'
    response = requests.get(launch_url)
    response.raise_for_status()
    for launch in response.json():
        if launch['links']['flickr']['original']:
            ids.append(launch['id'])   
    return ids[-1]


def fetch_spacex_launch_images(links, path):
    for num, link in enumerate(links):
        filename = 'spacex_'+str(num)+".jpg"
        download_path = path.joinpath(filename)
        download_img(link, download_path)
        

def get_file_extension(url):
    parsed_url = urlparse(url)
    url_path = unquote(parsed_url.path)
    filename, file_extension = os.path.splitext(url_path)
    return file_extension


def get_APOD(url, query, download_dir_name):
    path = Path.cwd()
    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    params = urlencode(query)
    apod_url = f'{url}?{params}'
    response = requests.get(apod_url)
    response.raise_for_status()
    for item, elem in enumerate(response.json()):
        img_url = elem['url']
        file_name = 'nasa_apod_'+str(item)+get_file_extension(img_url)
        download_path = img_download_dir.joinpath(file_name)
        download_img(img_url, download_path)


def get_EPIC(params, download_dir_name, number_of_images):
    ttl_imgs = 0
    img_links = []
    res = []
    path = Path.cwd()
    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    today = date.today()
    year, month, day = parse_date(today)
    cur_date = today
    while ttl_imgs < number_of_images:
        url = (f'https://api.nasa.gov/EPIC/api/natural/date/'
               f'{year}-{month}-{day}')
        response = requests.get(url, params=params)
        response.raise_for_status()
        ttl_imgs += len(response.json())
        res.append(response.json())
        new_date = cur_date-timedelta(days=1)
        year, month, day = parse_date(new_date)
        cur_date = new_date        
    for elem in res:
        for data in elem:
            img_links.append((data['date'], data['image']))

    user_params = urlencode(params)
    for link in img_links:
        img_date, img_name = link
        dt = datetime.fromisoformat(img_date)
        year = str(dt.year)
        month = str(dt.month) if dt.month > 9 else '0'+str(dt.month)
        day = str(dt.day) if dt.day > 9 else '0'+str(dt.day)
        url = (f'https://api.nasa.gov/EPIC/archive/natural/'
               f'{year}/{month}/{day}/png/{img_name}.png')
        img_url = f'{url}?{user_params}'
        download_path = img_download_dir.joinpath(f'{img_name}.png')
        download_img(img_url, download_path)
