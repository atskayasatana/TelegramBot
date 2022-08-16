import argparse
import os
import sys

from dotenv import load_dotenv
from functions import get_EPIC


FOLDER_TO_DOWNLOAD="EPIC"

if __name__ == '__main__':
     load_dotenv()
     api_key=os.getenv('api_key')
     
     parser = argparse. ArgumentParser()
     parser.add_argument('epic_count',
                         nargs='?',
                         default=10,
                         type=int)

     count=int(parser.parse_args().epic_count)

     params={'api_key':api_key
             }
     get_EPIC(params,FOLDER_TO_DOWNLOAD, count)

