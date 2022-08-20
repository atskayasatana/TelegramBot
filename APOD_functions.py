import requests

from functions import download_img
from functions import get_file_extension
from pathlib import Path
from urllib.parse import urlparse, unquote, urlencode

def get_APOD(url,query, download_dir_name):
    path=Path.cwd()
    img_download_dir=path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    params=urlencode(query)
    response=requests.get(url, params=params)
    response.raise_for_status()
    for item, elem in enumerate(response.json()):
        img_url=elem['url']
        file_name=f'nasa_apod_{str(item)}{get_file_extension(img_url)}'
        download_path=img_download_dir.joinpath(file_name)
        download_img(img_url, download_path)
