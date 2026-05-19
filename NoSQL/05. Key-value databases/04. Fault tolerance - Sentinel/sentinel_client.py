from redis.sentinel import Sentinel
import time
import sys

print("=== Запуск скрипта тестування Redis Sentinel ===")

# Використовуємо імена сервісів Docker. Внутрішній порт для всіх — 26379!
SENTINELS = [
    ('sentinel-1', 26379),
    ('sentinel-2', 26379),
    ('sentinel-3', 26379)
]

try:
    # Збільшуємо socket_timeout, щоб дати Docker DNS час відповісти під час навантаження
    sentinel = Sentinel(SENTINELS, socket_timeout=3.0, decode_responses=True)
    
    print("Намагаємось підключитись до Sentinel та знайти майстра...")
    master = sentinel.master_for('mymaster', socket_timeout=3.0)
    replica = sentinel.slave_for('mymaster', socket_timeout=3.0)
    
    # Перевірочний запис
    master.set('product:price', '1499')
    time.sleep(0.2)
    print(f"✓ Успішне підключення! product:price з репліки = {replica.get('product:price')}\n")

except Exception as e:
    print(f"❌ Помилка ініціалізації: {e}")
    sys.exit(1)

print("Записуємо дані щосекунди (можна робити 'docker stop redis-master'):\n")

for i in range(40):
    try:
        master.set('counter', i)
        current = master.get('counter')
        print(f"[{time.strftime('%X')}]   counter = {current}   ✓")
    except Exception as e:
        print(f"[{time.strftime('%X')}]   ⚠️  Помилка: {e} -- Очікування Failover...")
    time.sleep(1)