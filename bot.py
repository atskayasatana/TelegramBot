import os
import random
import telegram
import time

from dotenv import load_dotenv
from functions import get_image
from pathlib import Path
from retry import retry


@retry(telegram.error.NetworkError, tries=100, delay=2)
def send_initial_message_w_image(bot, chat_id, text, image):
    try:
        bot.send_message(chat_id=chat_id, text=text)
        bot.send_photo(chat_id=chat_id, photo=image)
    except telegram.error.NetworkError:
        print("Ошибка подключения!")
        print("Попытка соединения...")
        raise


@retry(telegram.error.NetworkError, tries=100, delay=2)
def send_random_image(bot, chat_id, image):
    try:
        bot.send_photo(chat_id=chat_id, photo=image)
    except telegram.error.NetworkError:
        print("Ошибка подключения!")
        print("Попытка соединения...")
        raise


def main():
    TEXT = "Hello, I'm the coolest bot ever!"
    DELAY_HOURS = 0.001

    load_dotenv()
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    file_to_send = os.environ.get("FILE_TO_SEND", None)
    delay = os.environ.get("DELAY_HOURS", DELAY_HOURS) * 3600

    directories = [
        Path.cwd().joinpath("images"),
        Path.cwd().joinpath("EPIC"),
        Path.cwd().joinpath("APOD"),
    ]
    dir_num = random.randint(0, 2)
    images = os.listdir(directories[dir_num])
    random_image = directories[dir_num].joinpath(random.choice(images))

    bot = telegram.Bot(token=token)

    if file_to_send:
        try:
            img_data = get_image(file_to_send)
        except FileNotFoundError:
            print("Указанный файл не найден. Будет отправлено случайное фото")
            img_data = get_image(random_image)
    else:
        img_data = get_image(random_image)

    send_initial_message_w_image(bot, chat_id, TEXT, img_data)

    while True:
        time.sleep(float(delay))
        dir_num = random.randint(0, 2)
        images = os.listdir(directories[dir_num])
        random_image = directories[dir_num].joinpath(random.choice(images))
        img_data = get_image(random_image)
        send_random_image(bot, chat_id, img_data)


if __name__ == "__main__":
    main()
