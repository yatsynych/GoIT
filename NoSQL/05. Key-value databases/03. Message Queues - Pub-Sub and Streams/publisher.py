import time
from db import init
r = init()

messages = [
    'Нове замовлення #1001 від користувача alice',
    'Платіж по замовленню #1001 підтверджено',
    'Замовлення #1001 передано в доставку',
]

print("Публікую повідомлення в канал 'notifications'...\n")
for msg in messages:
    subscribers_count = r.publish('notifications', msg)
    print(f"  [НАДІСЛАНО] {msg}")
    print(f"             → доставлено {subscribers_count} підписникам")
    time.sleep(1)

