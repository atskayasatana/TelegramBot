import argparse
import os
import requests

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from functions import download_img
from functions import parse_date
from pathlib import Path
from urllib.parse import urlencode

FOLDER_TO_DOWNLOAD = "EPIC"


def get_available_for_date_epic(params, date):
    url = "https://api.nasa.gov/EPIC/api/natural/date"
    year, month, day = parse_date(date)
    url_w_date = f"{url}/{year}-{month}-{day}"
    response = requests.get(url_w_date, params=params)
    response.raise_for_status()
    epic_json = response.json()
    return epic_json


def get_EPIC(params, download_dir_name, number_of_images):
    ttl_imgs = 0
    img_links = []
    res = []

    path = Path.cwd()
    cur_date = date.today()
    user_params = urlencode(params)

    img_download_dir = path.joinpath(download_dir_name)
    Path.mkdir(img_download_dir, exist_ok=True)

    while ttl_imgs < number_of_images:
        nasa_json = get_available_for_date_epic(params, cur_date)
        ttl_imgs += len(nasa_json)
        res.append(nasa_json)
        cur_date = cur_date - timedelta(days=1)

    for elem in res:
        for data in elem:
            img_links.append((data["date"], data["image"]))

    for link in img_links:
        img_date, img_name = link
        dt = datetime.fromisoformat(img_date)
        year, month, day = parse_date(dt)
        url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{year}/{month}/{day}/png/{img_name}.png"
        )

        download_path = img_download_dir.joinpath(f"{img_name}.png")
        download_img(url, download_path, user_params)


if __name__ == "__main__":
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]

    parser = argparse.ArgumentParser()
    parser.add_argument("epic_count", nargs="?", default=10, type=int)

    count = parser.parse_args().epic_count

    params = {"api_key": nasa_api_key}
    get_EPIC(params, FOLDER_TO_DOWNLOAD, count)
