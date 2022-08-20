import os

if __name__ == '__main__':
    
    print('Введите API для сайта NASA',end='\t')
    API_KEY = input()
    if API_KEY and API_KEY not in(' ',''):
        file = open('.env', 'w+')
        file.write(f'API_KEY = {API_KEY}\n')
        file.close()
        
    print('Введите свой токен для ТГ', end='\t')
    TOKEN = input()
    if TOKEN and TOKEN not in(' ',''):
        file = open('.env', 'a')
        file.write(f'TELEGRAM_BOT_TOKEN = {TOKEN}')
        file.close()
    

