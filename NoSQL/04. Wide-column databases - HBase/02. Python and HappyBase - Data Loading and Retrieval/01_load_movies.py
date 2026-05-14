import csv
import happybase
import os

# Очищення консолі для кращої візуалізації результатів
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()

# Підключення до HBase через Thrift API

# Якщо ви запускаєте цей код на вашій локальній машині, використовуйте 'localhost' як хост
# conn = happybase.Connection('localhost', port=9090)

# Якщо ви запускаєте цей код всередині контейнера, використовуйте 'hbase' як хост
conn = happybase.Connection('hbase', port=9090)

conn.open()

TABLE_NAME = 'movies'

# Видаляємо таблицю якщо вже існує (для чистоти експерименту)
if TABLE_NAME.encode() in conn.tables():
    print(f"Таблиця '{TABLE_NAME}' вже існує, видаляємо...")
    conn.disable_table(TABLE_NAME)
    conn.delete_table(TABLE_NAME)

# Створюємо таблицю з двома Column Families
conn.create_table(
    TABLE_NAME,
    {
        'info': dict(max_versions=1),
        'meta': dict(max_versions=1),
    }
)
print(f"Таблиця '{TABLE_NAME}' створена")

table = conn.table(TABLE_NAME)

# Завантажуємо дані з CSV через batch для ефективності
print("Завантажуємо дані з movies.csv...")

with open('movies.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    # batch_size=100: відправляємо дані на сервер пачками по 100 рядків
    # це набагато швидше, ніж відправляти кожен рядок окремо
    with table.batch(batch_size=100) as batch:
        for row in reader:
            row_key = row['movie_id'].encode()
            batch.put(row_key, {
                b'info:title':    row['title'].encode(),
                b'info:genre':    row['genre'].encode(),
                b'info:year':     row['year'].encode(),
                b'info:rating':   row['rating'].encode(),
                b'meta:director': row['director'].encode(),
            })
            print(f"  Додано:{row['movie_id']} —{row['title']}")

print("\nДані успішно завантажені!")

print()
conn.close()