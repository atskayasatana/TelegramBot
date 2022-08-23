import argparse
import os
import requests

from dotenv import load_dotenv
from functions import download_img
from functions import get_file_extension
from pathlib import Path
from urllib.parse import unquote, urlencode, urlparse


URL = 'https://api.nasa.gov/planetary/apod'

FOLDER_TO_DOWNLOAD = "APOD"


def get_APOD(url, query, download_dir_name):
    path = Path.cwd()
    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)
    params = urlencode(query)
    response = requests.get(url, params=params)
    response.raise_for_status()
    for item, elem in enumerate(response.json()):
        if elem['media_type']=='image':
            img_url = elem['url']
            file_name = f'nasa_apod_{str(item)}{get_file_extension(img_url)}'
            download_path = img_download_dir.joinpath(file_name)
            download_img(img_url, download_path)

            
if __name__ == '__main__':
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    parser = argparse. ArgumentParser()
    parser.add_argument('image_count',
                        help="number of images to download",
                        nargs='?',
                        default=5,
                        type=int)

    count = min(parser.parse_args().image_count, 100)
     
    params = {'api_key': nasa_api_key,
              'count': count
              }
     get_APOD(URL, params, FOLDER_TO_DOWNLOAD)
