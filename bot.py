import os
import random
import retry
import telegram
import time

from dotenv import load_dotenv
from functions import get_image
from pathlib import Path
from retry import retry
from telegram import error

TEXT = 'Hello, I\'m the coolest bot ever!'
DEFAULT_DELAY = 4

if __name__ == '__main__':
    load_dotenv()
    token = os.environ['TELEGRAM_BOT_TOKEN']
    directories = [Path.cwd().joinpath("images"),
                   Path.cwd().joinpath("EPIC"),
                   Path.cwd().joinpath("APOD")
                   ]
    bot = telegram.Bot(token=token)
    dir_num = random.randint(0, 2)
    images = os.listdir(directories[dir_num])
    random_image = directories[dir_num].joinpath(random.choice(images))

    print('Введите id чата:', end='\t')
    chat_id = input()
    if not chat_id or chat_id in ('', ' '):
        print('Нужен id чата!')
        exit()
    print('Введите путь к фото д/загрузки:', end='\t')
    image_file = input()
    print('Введите период для отправки:', end='\t')
    delay = input()
    if not delay:
        delay = DEFAULT_DELAY
     
    if image_file and image_file not in ('', ' '):
        try:
            img_data = get_image(image_file)
        except FileNotFoundError:
            print('Указаный файл не найден. Будет отправлено случайное фото')
            img_data = get_image(random_image)         
    else:
        print('Путь к файлу не введен. Будет отправлено случайное фото')
        img_data = get_image(random_image)

    @retry(telegram.error.NetworkError, tries=100, delay=2) 
    def send_message(text, chat_id):

        try:
            bot.send_message(text=text, chat_id=chat_id)
            bot.send_photo(chat_id=chat_id, photo=img_data)
            return
        except telegram.error.NetworkError:
            print('Ошибка подключения!')
            print('Попытка соединения...')
            raise
    send_message(TEXT, chat_id)
            
    while True:
        time.sleep(float(delay)*3600)
        dir_num = random.randint(0, 2)
        images = os.listdir(directories[dir_num])
        random_image = directories[dir_num].joinpath(random.choice(images))
        img_data = get_image(random_image)
        
        @retry(telegram.error.NetworkError, tries=100, delay=5) 
        def send_random_image(img_data):
            try:
                bot.send_photo(chat_id=chat_id, photo=img_data)
            except telegram.error.NetworkError:
                print('Ошибка подключения!')
                print('Попытка соединения...')
                raise    
        send_random_image(img_data)
