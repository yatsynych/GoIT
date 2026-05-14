import happybase
import hashlib
import os

# Очищення консолі для кращої візуалізації результатів
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()

# Якщо ви запускаєте цей код на вашій локальній машині, використовуйте 'localhost' як хост
# conn = happybase.Connection('localhost', port=9090)

# Якщо ви запускаєте цей код всередині контейнера, використовуйте 'hbase' як хост
conn = happybase.Connection('hbase', port=9090)

conn.open()
table = conn.table('logs_good')

NUM_BUCKETS = 4  # Кількість "кошиків" для розподілу

def make_salted_key(server_id: str, timestamp: int) -> bytes:
    """
    Створюємо ключ: salt:server_id:reversed_timestamp

    Три ідеї в одному ключі:
    1. Сіль (від server_id) — рівномірно розподіляє по регіонах
    2. server_id — групує логи одного сервера разом
    3. Зворотний timestamp — останні логи читаються першими
    """
    # Сіль: детермінований хеш від server_id
    # Один і той самий сервер ЗАВЖДИ отримує однакову сіль
    h = hashlib.md5(server_id.encode()).hexdigest()
    salt = int(h, 16) % NUM_BUCKETS

    # Зворотний timestamp: віднімаємо від великого числа
    # Чим пізніше подія, тим менше це число
    # → при scan першими йдуть СВІЖІ логи
    reversed_ts = 9_999_999_999_999 - timestamp

    return f"{salt:01d}:{server_id}:{reversed_ts}".encode()

servers = ['web-01', 'web-02', 'web-03']
messages = [
    'Request received',
    'Database query executed',
    'Response sent',
    'Cache miss',
    'User authenticated',
]

print("Записуємо логи з ГАРНИМ Row Key: salt:server_id:reversed_timestamp\\n")

# Показуємо, яку сіль отримає кожен сервер
print("Розподіл серверів по кошиках:")
for server in servers:
    h = hashlib.md5(server.encode()).hexdigest()
    salt = int(h, 16) % NUM_BUCKETS
    print(f"{server} → кошик{salt}")
print()

with table.batch() as batch:
    for i in range(15):
        server = servers[i % 3]
        message = messages[i % 5]
        ts = 1744000000000 + (i * 1000)
        row_key = make_salted_key(server, ts)
        batch.put(row_key, {
            b'log:server': server.encode(),
            b'log:message': message.encode(),
            b'log:level': b'INFO',
        })

print("Дані записані. Подивимось на порядок ключів:\\n")

for key, data in table.scan():
    print(f"{key.decode()}")

print()
conn.close()