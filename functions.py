import os
import requests
import urllib

from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode


def parse_date(date):
    year = str(date.year)
    month = str(date.month) if date.month>9 else f'0{str(date.month)}'
    day = str(date.day) if date.day>9 else f'0{str(date.day)}'
    return year, month, day


def download_img(img_url, download_path):
    response = requests.get(img_url)
    response.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(response.content)
        file.close()

    
def get_file_extension(url):
    parsed_url = urlparse(url)
    url_path = unquote(parsed_url.path)
    filename, file_extension=os.path.splitext(url_path)
    return file_extension


def get_image(path):
    try:
        with open(path, 'rb') as image:
            img_data = image.read()
            image.close()
    except FileNotFoundError:
        print('Файл не найден!')
        raise
    return img_data
