import happybase
equals_length = 70
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
table = conn.table('movies')

print("=" * equals_length)
print("1. Читаємо один фільм за ID")
print("=" * equals_length)

row = table.row(b'movie_001')
print(f"Заголовок: {row[b'info:title'].decode()}")
print(f"Жанр: {row[b'info:genre'].decode()}")
print(f"Рік: {row[b'info:year'].decode()}")
print(f"Рейтинг: {row[b'info:rating'].decode()}")
print(f"Режисер: {row[b'meta:director'].decode()}")

print()
print("=" * equals_length)
print("2. Читаємо кілька фільмів одразу")
print("=" * equals_length)

keys = [b'movie_002', b'movie_005', b'movie_009']
rows = table.rows(keys)

for key, data in rows:
    title = data[b'info:title'].decode()
    rating = data[b'info:rating'].decode()
    print(f"{key.decode()}:{title} (рейтинг: {rating})")

print()
print("=" * equals_length)
print("3. Скануємо всі фільми, виводимо тільки назву і рейтинг")
print("=" * equals_length)

for key, data in table.scan(columns=[b'info:title', b'info:rating']):
    title = data.get(b'info:title', b'').decode()
    rating = data.get(b'info:rating', b'').decode()
    print(f"{key.decode()}: {title} —{rating}")

print()
print("=" * equals_length)
print("4. Фільтрація на стороні клієнта: фільми з рейтингом >= 8.9")
print("=" * equals_length)

# Важливий момент: HBase не вміє фільтрувати за значенням числа.
# Ми читаємо всі рядки і фільтруємо в Python.
# У реальних системах це вирішується через дизайн Row Key.
top_movies = []
for key, data in table.scan(columns=[b'info:title', b'info:rating']):
    rating = float(data.get(b'info:rating', b'0').decode())
    title = data.get(b'info:title', b'').decode()
    if rating >= 8.9:
        top_movies.append((rating, title))

top_movies.sort(reverse=True)
for rating, title in top_movies:
    print(f"{rating} —{title}")

# Додатково: фільми режисера Christopher Nolan
target_director = 'Christopher Nolan'
print()
print("=" * equals_length)
print(f"5. Фільтрація на стороні клієнта: фільми режисера {target_director}")
print("=" * equals_length)

for key, data in table.scan(columns=[b'info:title', b'meta:director']):
    director = data.get(b'meta:director', b'').decode()
    if director == target_director:
        title = data.get(b'info:title', b'').decode()
        print(f"{key.decode()}: {title}")

print()
conn.close()