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

if b'orders_v2' in conn.tables():
    conn.disable_table('orders_v2')
    conn.delete_table('orders_v2')
conn.create_table('orders_v2', {'order': dict()})
table = conn.table('orders_v2')

NUM_BUCKETS = 4

def make_order_key(customer_id: str, timestamp: int) -> bytes:
    h = hashlib.md5(customer_id.encode()).hexdigest()
    salt = int(h, 16) % NUM_BUCKETS
    reversed_ts = 9_999_999_999_999 - timestamp
    return f"{salt}:{customer_id}:{reversed_ts}".encode()

orders = [
    ('cust_100', 1744000001000, 5990, 'Ноутбук'),
    ('cust_200', 1744000002000, 1200, 'Клавіатура'),
    ('cust_100', 1744000003000,  350, 'Килимок'),
    ('cust_300', 1744000004000, 2500, 'Монітор'),
    ('cust_200', 1744000005000,  800, 'Миша'),
    ('cust_100', 1744000006000, 3200, 'Навушники'),
    ('cust_300', 1744000007000,  150, 'Кабель HDMI'),
]

with table.batch() as batch:
    for customer_id, ts, total, product in orders:
        key = make_order_key(customer_id, ts)
        batch.put(key, {
            b'order:customer': customer_id.encode(),
            b'order:total':    str(total).encode(),
            b'order:product':  product.encode(),
        })

# Читаємо всі замовлення cust_100 (останні першими)
h = hashlib.md5('cust_100'.encode()).hexdigest()
salt = int(h, 16) % NUM_BUCKETS
row_start = f"{salt}:cust_100:".encode()
row_stop  = f"{salt}:cust_100;".encode()

print("Замовлення cust_100 (останні першими):")
for key, data in table.scan(row_start=row_start, row_stop=row_stop):
    product = data.get(b'order:product', b'').decode()
    total   = data.get(b'order:total', b'').decode()
    print(f"{product} --{total} грн.")

print()
conn.close()