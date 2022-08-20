import requests

from datetime import date, datetime, timedelta
from functions import download_img
from functions import parse_date
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode


def get_EPIC(params,download_dir_name, number_of_images):
    ttl_imgs = 0
    img_links = []
    res = []
    path = Path.cwd()
    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    today = date.today()
    year, month, day = parse_date(today)
    cur_date = today
    while ttl_imgs<number_of_images:
        url = (f'https://api.nasa.gov/EPIC/api/'
               f'natural/date/{year}-{month}-{day}')
        response = requests.get(url, params=params)
        response.raise_for_status()
        ttl_imgs += len(response.json())
        res.append(response.json())
        new_date = cur_date-timedelta(days=1)
        year, month, day = parse_date(new_date)
        cur_date = new_date        
    for elem in res:
        for data in elem:
            img_links.append((data['date'],data['image']))
    user_params = urlencode(params)
    for link in img_links:
        img_date, img_name = link
        dt = datetime.fromisoformat(img_date)
        year, month, day = parse_date(dt)
        url = (f'https://api.nasa.gov/EPIC/archive/natural/'
               f'{year}/{month}/{day}/png/{img_name}.png')
        img_url = f'{url}?{user_params}'
        download_path = img_download_dir.joinpath(f'{img_name}.png')
        download_img(img_url, download_path)
