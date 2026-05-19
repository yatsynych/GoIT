from db import init
r = init()

pubsub = r.pubsub()
pubsub.subscribe('notifications')

print("Підписник запущений. Очікую повідомлення з каналу 'notifications'...")
print("(Для зупинки натисніть Ctrl+C)\n")

for message in pubsub.listen():
    # Перше повідомлення -- службове підтвердження підписки, пропускаємо
    if message['type'] == 'message':
        print(f"  [ОТРИМАНО] {message['data']}")