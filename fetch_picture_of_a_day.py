import argparse
import os

from APOD_functions import get_APOD
from dotenv import load_dotenv
from pathlib import Path

URL='https://api.nasa.gov/planetary/apod'

FOLDER_TO_DOWNLOAD="APOD"


if __name__ == '__main__':
     load_dotenv()
     API_KEY=os.environ['API_KEY']
     parser = argparse. ArgumentParser()
     parser.add_argument('image_count',
                         help="number of images to download",
                         nargs='?',
                         default=5)

     count= min(int(parser.parse_args().image_count), 100)
     
     params={'api_key':API_KEY,
             'count':count
             }
     get_APOD(URL,params, FOLDER_TO_DOWNLOAD)
