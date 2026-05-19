import time
from db import init
r = init()

QUEUE = 'tasks:scheduled'
r.delete(QUEUE)

now = time.time()

# Додаємо задачі з часом виконання як score
r.zadd(QUEUE, {
    'task:send_welcome_email:001': now + 5,    # через 5 секунд
    'task:process_payment:042':    now + 2,    # через 2 секунди
    'task:generate_report:007':    now + 10,   # через 10 секунд
    'task:cleanup_sessions:099':   now + 1,    # через 1 секунду
})

print("Всі задачі в черзі:")
all_tasks = r.zrange(QUEUE, 0, -1, withscores=True)
for task, scheduled_at in all_tasks:
    delay = scheduled_at - now
    print(f"  через {delay:.0f} сек: {task}")

print()
print("Чекаємо 3 секунди...")
time.sleep(3)

print()
print("Задачі готові до виконання прямо зараз:")
# Обираємо всі задачі, час яких вже настав
ready = r.zrangebyscore(QUEUE, '-inf', time.time())
for task in ready:
    print(f"  [ВИКОНАТИ] {task}")
    # У реальній системі тут була б обробка задачі
    r.zrem(QUEUE, task)  # Видаляємо з черги після виконання

print()
remaining = r.zrange(QUEUE, 0, -1, withscores=True)
print(f"Залишилося в черзі: {len(remaining)} задач")
for task, scheduled_at in remaining:
    delay = scheduled_at - time.time()
    print(f"  ще через {delay:.0f} сек: {task}")