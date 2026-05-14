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

# Створюємо тимчасову таблицю для тесту
if b'speed_test' in conn.tables():
    conn.disable_table('speed_test')
    conn.delete_table('speed_test')
conn.create_table('speed_test', {'d': dict()})
table = conn.table('speed_test')

N = 500

# Звичайний запис — кожен put окремий мережевий запит
start = time.time()
for i in range(N):
    table.put(
        f'row_{i:05d}'.encode(),
        {b'd:v': str(i).encode()}
    )
elapsed_single = time.time() - start
print();
print(f"Звичайний запис{N} рядків: {elapsed_single:.2f} сек "
      f"({elapsed_single / N * 1000:.1f} мс/рядок)")

# Видаляємо і створюємо знову для чистоти
conn.disable_table('speed_test')
conn.delete_table('speed_test')
conn.create_table('speed_test', {'d': dict()})
table = conn.table('speed_test')

# Batch запис — всі put групуються і відправляються пачками
start = time.time()
with table.batch(batch_size=100) as batch:
    for i in range(N):
        batch.put(
            f'row_{i:05d}'.encode(),
            {b'd:v': str(i).encode()}
        )
elapsed_batch = time.time() - start
print(f"Batch запис{N} рядків: {elapsed_batch:.2f} сек "
      f"({elapsed_batch / N * 1000:.1f} мс/рядок)")

speedup = elapsed_single / elapsed_batch
print(f"\nBatch швидший у {speedup:.1f} разів")

print()
conn.close()