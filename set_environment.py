import os

if __name__ == '__main__':
    
    print('Введите API для сайта NASA', end='\t')
    nasa_api_key = input().strip()
            
    print('Введите свой токен для ТГ', end='\t')
    token = input().strip()

    print('Введите чат id', end='\t')
    chat_id=input().strip()

    with open('.env', 'w+') as env_file:
        env_file.write(f'NASA_API_KEY={nasa_api_key}\n')
        env_file.write(f'TELEGRAM_BOT_TOKEN={token}\n')
        env_file.write(f'TELEGRAM_CHAT_ID={chat_id}\n')
        env_file.write(f'DELAY_HOURS=4\n')
        env_file.close()
