# Створюємо таблицю для логів сервера з двома колонковими сімействами: 'log' для зберігання логів та 'meta' для зберігання метаданих.
import happybase
import time
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

# Підготовка: видаляємо таблицю якщо є
for table_name in [b'logs_bad', b'logs_good']:
    if table_name in conn.tables():
        conn.disable_table(table_name)
        conn.delete_table(table_name)

conn.create_table('logs_bad', {'log': dict(max_versions=1)})
conn.create_table('logs_good', {'log': dict(max_versions=1)})

print("Таблиці створені\n")
conn.close()