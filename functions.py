import os
import requests
import urllib

from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode


def parse_date(date):
    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')
    return year, month, day


def download_img(img_url, download_path, params=None):
    response = requests.get(img_url, params=params)
    response.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(response.content)

    
def get_file_extension(url):
    parsed_url = urlparse(url)
    url_path = unquote(parsed_url.path)
    filename, file_extension = os.path.splitext(url_path)
    return file_extension


def get_image(path):
    try:
        with open(path, 'rb') as image:
            img_data = image.read()
    except FileNotFoundError:
        print('Файл не найден!')
        raise
    return img_data
