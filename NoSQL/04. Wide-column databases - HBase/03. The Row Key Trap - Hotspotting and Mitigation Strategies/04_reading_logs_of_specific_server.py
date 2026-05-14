import happybase
import hashlib
from datetime import datetime
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

NUM_BUCKETS = 4


def get_server_logs(table, server_id: str, limit: int = 10):
    """
    Читаємо останні N логів для конкретного сервера.

    Оскільки сіль детермінована від server_id,
    ми точно знаємо в якому регіоні лежать дані.
    Скануємо тільки один регіон, а не всі!
    """
    # Обчислюємо сіль — ту саму формулу, що при записі
    h = hashlib.md5(server_id.encode()).hexdigest()
    salt = int(h, 16) % NUM_BUCKETS

    # Діапазон: всі ключі для цього сервера в цьому кошику
    row_start = f"{salt}:{server_id}:".encode()
    row_stop  = f"{salt}:{server_id};".encode()  # ';' > ':' в ASCII

    results = []
    for key, data in table.scan(row_start=row_start,
                                 row_stop=row_stop,
                                 limit=limit):
        results.append({
            'key':     key.decode(),
            'server':  data.get(b'log:server', b'').decode(),
            'message': data.get(b'log:message', b'').decode(),
        })
    return results


# Читаємо логи для кожного сервера
for server in ['web-01', 'web-02', 'web-03']:
    print(f"\nОстанні логи для{server}:")
    logs = get_server_logs(table, server, limit=5)
    if logs:
        for entry in logs:
            print(f"  [{entry['server']}]{entry['message']}")
    else:
        print("  (логів немає)")

print()
conn.close()