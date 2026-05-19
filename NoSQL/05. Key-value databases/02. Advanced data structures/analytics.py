from db import init
r = init()

TODAY = 'analytics:visitors:2026-04-18'
YESTERDAY = 'analytics:visitors:2026-04-17'
WEEK = 'analytics:visitors:week'

r.delete(TODAY, YESTERDAY, WEEK)

# Імітуємо відвідування за сьогодні: 100 000 унікальних користувачів
# плюс 500 повторних візитів
print("Завантажуємо дані за сьогодні (100 000 унікальних + 500 повторних)...")
today_visitors = [f'user:{i}' for i in range(1, 100_001)]
repeat_visitors = [f'user:{i}' for i in range(1, 501)]  # перші 500 повернулися

# Додаємо батчами по 1000 -- не варто надсилати мільйон аргументів однією командою
batch_size = 1000
for i in range(0, len(today_visitors), batch_size):
    r.pfadd(TODAY, *today_visitors[i:i + batch_size])

r.pfadd(TODAY, *repeat_visitors)  # Повторні -- не збільшать лічильник

# Дані за вчора: перетин із сьогоднішніми користувачами + нові
print("Завантажуємо дані за вчора (70 000 унікальних, з них 30 000 також були сьогодні)...")
yesterday_visitors = [f'user:{i}' for i in range(70_001, 140_001)]
for i in range(0, len(yesterday_visitors), batch_size):
    r.pfadd(YESTERDAY, *yesterday_visitors[i:i + batch_size])

print()

# Рахуємо
today_count = r.pfcount(TODAY)
yesterday_count = r.pfcount(YESTERDAY)

print(f"Унікальних за сьогодні (оцінка): {today_count:>10,}  (реально: 100 000)")
print(f"Унікальних за вчора (оцінка): {yesterday_count:>10,}  (реально: 70 000)")

# Об'єднуємо два дні
r.pfmerge(WEEK, TODAY, YESTERDAY)
week_count = r.pfcount(WEEK)

# Реальна кількість за обидва дні: 100 000 + 70 000 - перетин
# Перетин: user:70001 до user:100000 -- це 30 000 користувачів
# Разом: 100 000 + 70 000 - 30 000 = 140 000
print(f"Унікальних за обидва дні (оцінка):{week_count:>10,}  (реально: 140 000)")

print()
print("=== Використання пам'яті ===")
mem_today = r.memory_usage(TODAY)
print(f"HyperLogLog за день: {mem_today:,} байт (~{mem_today / 1024:.1f} КБ)")
print()
print("Для порівняння: звичайний SET з тими ж даними:")
r.sadd('temp:set', *today_visitors[:1000])  # Тільки 1000 для прикладу
mem_set_sample = r.memory_usage('temp:set')
r.delete('temp:set')
# Екстраполюємо на 100 000
approx_set_mem = mem_set_sample * 100
print(f"  ~{approx_set_mem / 1024 / 1024:.1f} МБ (оцінка для 100 000 користувачів)")
print(f"  HyperLogLog економить приблизно у {approx_set_mem / mem_today:.0f} разів більше пам'яті")

