import argparse
import requests

from datetime import date, datetime, timedelta
from functions import download_img
from functions import parse_date
from pathlib import Path
from urllib.parse import urlencode

URL = 'https://api.spacexdata.com/v5/launches'

FOLDER_TO_DOWNLOAD = "Images"


def get_foto_of_launch_by_id(url, launch_id='latest'):
    launch_url=f'{url}/{launch_id}'
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
        download_img(link, download_path)

        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('id',
                        help="id of spaceX launch to download images",
                        nargs='?',
                        default=None)
    spacex_launch_id = parser.parse_args().id   
    if spacex_launch_id:
        links = get_foto_of_launch_by_id(URL, spacex_launch_id)
    else:
        links = get_foto_of_launch_by_id(URL)
        if not links:
            latest_launch_with_foto_id = get_launch_id(URL)
            links = get_foto_of_launch_by_id(URL, latest_launch_with_foto_id)         
    path = Path.cwd()
    download_path = path.joinpath(FOLDER_TO_DOWNLOAD)
    Path.mkdir(download_path, exist_ok=True)
    fetch_spacex_launch_images(links, download_path)
