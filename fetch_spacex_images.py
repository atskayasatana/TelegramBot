import argparse
from functions import get_foto_of_launch_by_id
from functions import get_latest_launch_foto
from functions import fetch_spacex_launch_images
from functions import get_launch_id
from pathlib import Path

URL='https://api.spacexdata.com/v5/launches'

FOLDER_TO_DOWNLOAD="Images"


if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('id',
                        help="id of spaceX launch to download images",
                        nargs='?',
                        default=None)

    spacex_launch_id = parser.parse_args().id
    
    if spacex_launch_id:
        links=get_foto_of_launch_by_id(URL, spacex_launch_id)
    else:
        links=get_latest_launch_foto(URL)
        if not links:
            latest_launch_with_foto_id = get_launch_id(URL)
            links=get_foto_of_launch_by_id(URL, latest_launch_with_foto_id)
            
    path=Path.cwd()
    download_path=path.joinpath(FOLDER_TO_DOWNLOAD)
    Path.mkdir(download_path, exist_ok=True)
    fetch_spacex_launch_images(links, download_path)
    

    
        
    
