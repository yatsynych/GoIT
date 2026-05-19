import time
from db import init
r = init()

STREAM = 'orders:stream'
GROUP  = 'order-processors'
YELLOW = "\033[93m"
RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"

def consume(worker_name: str):
    print(f"[{worker_name}] Запущено, чекаю замовлення...\n")

    while True:
        # Читаємо до 2 повідомлень, чекаємо до 3 секунд якщо черга порожня
        messages = r.xreadgroup(
            GROUP,
            worker_name,
            {STREAM: '>'},   # '>' = тільки нові, ще не взяті цією групою
            count=2,
            block=3000
        )

        if not messages:
            print(f"[{worker_name}] Нових замовлень немає, завершую роботу.")
            break

        for stream_name, entries in messages:
            for msg_id, fields in entries:
                print(f"[{worker_name}] {BLUE}Обробляю: {RESET}"
                      f"{fields['order_id']} --{fields['product']} "
                      f"({fields['amount']} грн.) від {YELLOW}{fields['customer']}{RESET}")

                # Імітуємо обробку замовлення
                time.sleep(0.2)

                # Підтверджуємо успішну обробку
                r.xack(STREAM, GROUP, msg_id)
                print(f"[{worker_name}] {GREEN}✓ Підтверджено:{RESET} {fields['order_id']}\n")