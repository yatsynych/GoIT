import redis
import os

# Підключення до Redis серверу lокально на стандартному порту
# hostDB = 'localhost'

# Якщо Redis запущений в Docker контейнері з ім'ям "redis", то підключаємося до нього
hostDB = 'redis'

def init():
    # Очищення консолі для кращої візуалізації результатів
    os.system('cls' if os.name == 'nt' else 'clear')
    return redis.Redis(
        host=hostDB, 
        port=6379, 
        decode_responses=True
    )