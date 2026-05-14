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

# Створюємо таблицю зі зберіганням до 5 версій для CF 'data'
if b'versioned' in conn.tables():
    conn.disable_table('versioned')
    conn.delete_table('versioned')

conn.create_table(
    'versioned',
    {'data': dict(max_versions=5)}
)
table = conn.table('versioned')

print("\nЗаписуємо 6 версій однієї комірки з паузою 0.3 сек між ними\n")

# Емулюємо історію зміни ціни товару
prices = [1000, 1140, 1210, 1270, 1320, 1390]
for price in prices:
    table.put(
        b'product_001',
        {b'data:price': str(price).encode()}
    )
    print(f"  Записана ціна: {price} USD")
    time.sleep(0.3)

print("\nЧитаємо всі версії ціни:\n")

versions = table.cells(b'product_001', b'data:price', versions=5)
for i, val in enumerate(versions):
    print(f"  Версія {i+1}: {val.decode()} USD")

print()
conn.close()