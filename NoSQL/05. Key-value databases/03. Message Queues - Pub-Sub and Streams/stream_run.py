import threading
import time
import redis
from db import init
r = init()

from stream_producer import produce
from stream_consumer import consume

STREAM = 'orders:stream'
GROUP  = 'order-processors'

# Очищаємо стрим якщо запускаємо повторно
r.delete(STREAM)

# Створюємо Consumer Group
try:
    r.xgroup_create(STREAM, GROUP, id='0', mkstream=True)
    print(f"Consumer Group '{GROUP}' створено.\n")
except redis.exceptions.ResponseError as e:
    if 'BUSYGROUP' in str(e):
        print(f"Consumer Group '{GROUP}' вже існує.\n")

# Запускаємо продюсера і двох воркерів паралельно
t_producer  = threading.Thread(target=produce)
t_worker_1  = threading.Thread(target=consume, args=('worker-1',))
t_worker_2  = threading.Thread(target=consume, args=('worker-2',))

t_producer.start()
time.sleep(0.5)  # Даємо продюсеру опублікувати перші замовлення

t_worker_1.start()
t_worker_2.start()

t_producer.join()
t_worker_1.join()
t_worker_2.join()

# Фінальна перевірка
print("=" * 50)
pending_info = r.xpending(STREAM, GROUP)
print(f"Необроблених (pending) замовлень: {pending_info['pending']}")

stream_info = r.xinfo_stream(STREAM)
print(f"Всього замовлень у стримі: {stream_info['length']}")

if pending_info['pending'] == 0:
    print("\nВсі замовлення успішно оброблено!")