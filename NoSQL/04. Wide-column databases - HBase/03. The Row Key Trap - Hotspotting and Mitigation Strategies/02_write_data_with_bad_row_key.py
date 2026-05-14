import happybase
import time
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
table = conn.table('logs_bad')

# Імітуємо логи трьох серверів
servers = ['web-01', 'web-02', 'web-03']
messages = [
    'Request received',
    'Database query executed',
    'Response sent',
    'Cache miss',
    'User authenticated',
]

print("Записуємо логи з ПОГАНИМ Row Key: timestamp:server_id")
print("Формат ключа: 1744000001000_web-01\n")

with table.batch() as batch:
    for i in range(15):
        server = servers[i % 3]
        message = messages[i % 5]
        # ПОГАНИЙ ДИЗАЙН: timestamp на початку
        # Всі нові записи мають ключі більші за попередні
        # → всі пишуться в один регіон
        ts = 1744000000000 + (i * 1000)
        row_key = f"{ts}_{server}".encode()
        batch.put(row_key, {
            b'log:server': server.encode(),
            b'log:message': message.encode(),
            b'log:level': b'INFO',
        })

print("Дані записані. Подивимось на порядок ключів:\n")

for key, data in table.scan():
    print(f"{key.decode()}")

print()
conn.close()