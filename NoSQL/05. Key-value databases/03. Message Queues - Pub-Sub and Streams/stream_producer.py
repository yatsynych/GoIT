import time
from db import init
r = init()

STREAM = 'orders:stream'

def produce():
    orders = [
        {'order_id': 'ORD-1001', 'customer': 'alice',   'amount': '5990', 'product': 'Ноутбук ASUS'},
        {'order_id': 'ORD-1002', 'customer': 'bob',     'amount': '1200', 'product': 'Клавіатура'},
        {'order_id': 'ORD-1003', 'customer': 'charlie', 'amount': '350',  'product': 'Килимок'},
        {'order_id': 'ORD-1004', 'customer': 'diana',   'amount': '2500', 'product': 'Монітор'},
        {'order_id': 'ORD-1005', 'customer': 'alice',   'amount': '800',  'product': 'Миша'},
        {'order_id': 'ORD-1006', 'customer': 'eve',     'amount': '3200', 'product': 'Навушники'},
    ]

    print("[Продюсер] Починаю публікувати замовлення...\n")
    for order in orders:
        msg_id = r.xadd(
            STREAM,
            order,
            maxlen=1000,     # Стрим не виросте більше 1000 повідомлень
            approximate=True
        )
        print(f"[Продюсер] Замовлення опубліковано: {order['order_id']} "
              f"({order['product']},{order['amount']} грн.) → ID:{msg_id}")
        time.sleep(0.3)

    print("\n[Продюсер] Всі замовлення опубліковано.")