import chromadb
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# PersistentClient зберігає дані на диск — вони переживають перезапуск
client = chromadb.PersistentClient(path="./vector_db")

# get_or_create — ідемпотентно: якщо колекція є — відкриває, ні — створює
collection = client.get_or_create_collection(
    name="demo",
    metadata={"hnsw:space": "cosine"}  # задаємо метрику
)

# Додаємо документи — Chroma сама рахує ембеддинги вбудованою моделлю
collection.add(
    ids=["id-1", "id-2", "id-3"],
    documents=[
        "Трансформери зробили революцію в обробці тексту.",
        "Нейромережі навчаються на великих масивах даних.",
        "Реляційні бази даних зберігають дані в таблицях.",
    ],
)

# Шукаємо — рядок запиту теж перетворюється на вектор автоматично
results = collection.query(
    query_texts=["Як працює машинне навчання?"],
    n_results=2,
)

print("Результати пошуку:")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] {doc}")

print()
print(f"Дані збережено в ./vector_db")
print(f"Спробуйте перезапустити скрипт — дані залишаться.")