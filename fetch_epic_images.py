import argparse
import os
import requests
import sys

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from functions import download_img
from functions import parse_date
from pathlib import Path
from urllib.parse import urlencode

FOLDER_TO_DOWNLOAD = "EPIC"

def get_json(url, params, date):
        year, month, day = parse_date(date)
        url_w_date=f'{url}/{year}-{month}-{day}'
        response = requests.get(url_w_date, params=params)
        response.raise_for_status()
        return response.json(), len(response.json())


def get_EPIC(params, download_dir_name, number_of_images):
    ttl_imgs = 0
    img_links = []
    res = []
    url = (f'https://api.nasa.gov/EPIC/api/natural/date')
    path = Path.cwd()
    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    today = date.today()
    year, month, day = parse_date(today)
    cur_date = today
    while ttl_imgs < number_of_images:
        nasa_json, img_cnt = get_json(url, params, cur_date)
        ttl_imgs += img_cnt
        res.append(nasa_json)
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
        year, month, day = parse_date(dt)
        url = (f'https://api.nasa.gov/EPIC/archive/natural/'
               f'{year}/{month}/{day}/png/{img_name}.png')
        
        download_path = img_download_dir.joinpath(f'{img_name}.png')
        download_img(url, download_path, user_params)

        
if __name__ == '__main__':
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
     
    parser = argparse. ArgumentParser()
    parser.add_argument('epic_count',
                        nargs='?',
                        default=10,
                        type=int)

    count = parser.parse_args().epic_count

    params = {'api_key': nasa_api_key
              }
    get_EPIC(params, FOLDER_TO_DOWNLOAD, count)
