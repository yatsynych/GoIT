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

# Створюємо таблицю з TTL = 5 секунд для CF 'session'
# Це навчальний приклад — у реальності TTL зазвичай години або дні
if b'sessions' in conn.tables():
    conn.disable_table('sessions')
    conn.delete_table('sessions')

conn.create_table(
    'sessions',
    {
        'session': dict(time_to_live=5),   # Закінчується через 5 секунд
        'user':    dict(),                 # Без TTL — зберігається вічно
    }
)
table = conn.table('sessions')

print("\nСтворюємо сесію користувача...")
table.put(
    b'sess_abc123',
    {
        b'session:token':      b'eyJhbGciOiJIUzI1NiJ9',
        b'session:ip':         b'192.168.1.100',
        b'user:user_id':       b'user_42',
        b'user:username':      b'ivan_petrov',
    }
)
print("Сесія записана\n")

# Читаємо одразу після запису
print("Читаємо одразу:\n")
row = table.row(b'sess_abc123')
for col, val in row.items():
    print(f"  {col.decode()}: {val.decode()}")

print(f"\nЧекаємо 10 секунд (TTL = 5 сек)...")
time.sleep(10)

print("\nЧитаємо після закінчення TTL:\n")
row = table.row(b'sess_abc123')
if row:
    for col, val in row.items():
        print(f"  {col.decode()}: {val.decode()}")
else:
    print("  Рядок порожній — всі дані з TTL зникли")

print()
conn.close()