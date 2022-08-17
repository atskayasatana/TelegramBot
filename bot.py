import argparse
import os
import random
import telegram
import time
from pathlib import Path
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    delay = os.getenv('DELAY_HOURS')
    directories = [Path.cwd().joinpath("images"),
                   Path.cwd().joinpath("EPIC"),
                   Path.cwd().joinpath("APOD")]   
    bot = telegram.Bot(token=token)
    bot.send_message(text="Hello, I'm a space addicted bot",
                     chat_id='@taikong_2022')
    parser = argparse.ArgumentParser()    
    parser.add_argument('file_to_send',
                        nargs='?',
                        default=None)   
    image_file = parser.parse_args().file_to_send
    if image_file:
        bot.send_photo(chat_id='@taikong_2022', photo=open(image_file, 'rb'))
    else:
        dir_num = random.randint(0, 2)
        images = os.listdir(directories[dir_num])
        random_image = directories[dir_num].joinpath(random.choice(images))
        bot.send_photo(chat_id='@taikong_2022', photo=open(random_image, 'rb'))
    while True:
        time.sleep(int(delay)*3600)
        dir_num = random.randint(0, 2)
        images = os.listdir(directories[dir_num])
        random_image = directories[dir_num].joinpath(random.choice(images))
        bot.send_photo(chat_id='@taikong_2022', photo=open(random_image, 'rb'))
