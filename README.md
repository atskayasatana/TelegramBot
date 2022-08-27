# TelegramBot

Скрипт для загрузки фотографий в телеграм канал.

Для запуска нужен Python версии не ниже 3, а также библиотеки из файла requirements.txt. 
Архив с кодом нужно скачать к себе на компьютер и разархивировать в любую удобную директорию.

Перед началом работы установим необходимые библиотеки:
```Python
pip install -r requirements.txt
```
Для работы также понадобятся api_key, который можно сгенерировать здесь: https://api.nasa.gov/ и токен для ТелеграмБота(@BotFather).

При первом запуске нужно создать файл окружения, в котором будут храниться необходимые для работы ключи и токены.
Запускаем скрипт set_environment.py

```Python
python set_environment.py
```
Будут запрошены ключ для сайта, токен для телеграма и chat id для отправки сообщений.

![](https://github.com/atskayasatana/Images/blob/105e28a38d698edc4953fd471ec5351d5aabe6a1/4_credentials.png)

Эти данные будут записаны в .env файл и использоваться при запусках скриптов для бота.
Если ключи меняются, то скрипт нужно запустить снова и передать новые значения.

Также в файл можно добавить переменную FILE_TO_SEND- путь к картинке для отправки в чат при запуске скрипта. Если переменной не будет, то при запуске будет отправляться рандомная картинка.

Образец .env файла:

``` Python

NASA_API_KEY=# ваш api для сайта NASA
TELEGRAM_BOT_TOKEN=# ваш уникальный токен
TELEGRAM_CHAT_ID=# id чата для отправки сообщений
DELAY_HOURS=4 # периодичность отправки сообщений(значение по умолчанию 4 часа)
FILE_TO_SEND= # путь к картинке для отправки при запуске

```

Контент для телеграм-канала скачивается с сайтов: https://api.spacexdata.com/ и https://api.nasa.gov/.

 ## Скрипты для скачивания
 
 ### fetch_spacex_images.py
 
 Скачивает фотографии с запусков SpaceX.
 
 ```Python
 python fetch_spacex_images.py [id запуска]
 ```
 Если указать id запуска, то будут скачаны фотографии с запуска с указанным id. При запуске скрипта без данного параметра, то будут скачаны фотографии 
 с последнего запуска во время которого делались фото. Фотографии скачиваются в папку Images в директории проекта.
 
 
 ### fetch_picture_of_a_day.py
 
 Скачивает картинку дня - astronomy picture of the day c сайта NASA в папку APOD директории проекта.
 
 ```Python
 python fetch_picture_of_a_day.py [количество картинок для скачивания]
 ```
 Если не указать количество картинок для скачивания, то будет скачано 5 картинок. 
 На сайте установлено ограничение в 100 картинок для скачивания, поэтому при значениях больше 100 будет скачано 100 картинок. 
  
### fetch_epic_images.py

Скачивает изображения Земли с EPIC камеры NASA в папку EPIC директории проекта.

```Python
python fetch_epic_images.py [количество картинок для скачивания]
```

Если не указать количество картинок для скачивания, то будут скачаны 10 последних изображений. 

## Функции

## functions.py
Файл с общими функциями, которые используются во всех скриптах(работа с датами, скачивание)

### parse_date(date)
Принимает на вход дату в формате datetime и возвращает три значения: год, месяц, день в текстовом формате с 0 в начале для значений меньше 10.

### download_img(img_url, download_path)

Скачивает картину с img_url в файл download_path

### get_file_extension(url)

Функция для получения расширения файла с указанным url

### get_image(path)

Загружает картинку c адресом path в объект для дальнейшей работы.


### Функции для скачивания фото

### get_foto_of_launch_by_id(url, launch_id)

Возвращает список ссылок на фотографии с запуска SpaceX с заданным launch_id. Если launch_id не указан, то скачивает фото с самого последнего запуска.

### get_launch_id(url)

Функция для поиска проследнего запуска, для которого есть фотографии. Если get_foto_of_launch_by_id вернула пустой список ссылок, то можно вызвать get_launch_id и найти последний запуск с фотографиями. Поиск идет с 1 января 2022 по текущую дату.

### fetch_spacex_launch_images(links, path)

Функция для скачивания фотографий по списку ссылок links в директорию path.

### get_APOD(url,query, download_dir_name)

Функция для скачивания картинок дня в указанную в download_dir_name директорию. Аргумент query содержит параметры запроса, такие как api_key и количество картинок для скачивания.

### get_EPIC(params,download_dir_name, number_of_images)

Скачивает number_of_images число изображений с epic камеры в папку download_dir_name. Функция собирает нужное количество изображений начиная от текущей даты по каждому дню.

### get_available_for_date_epic(params, date)

Возвращает json - файл с данными о картинках доступных на дату date.


## bot.py

Скрипт для публикации контента в телеграмм-канал. 

```Python
python bot.py 
```
При запуске скрипт отправляет в чат с chat_id сообщение TEXT. Если в файле окружения есть переменная FILE_TO_SEND, то будет отправлена картинка, путь к которой указан в переменной. Если FILE_TO_SEND отсутствует, то при первом запуске будет отправлена рандомная картинка.
Далее, с указанной периодичностью DELAY_HOURS в чат будут отправлятся выбранные случайным образом из папок EPIC, APOD и Images фотографии. 
