import csv
import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# 1. Заходимо на https://app.pinecone.io/ → Sign Up
# 2. Ліве меню → API keys → + API key
# 3. Ім’я ключа: `practice-lesson`
# 4. Натискаємо Create key
# 5. Копіюємо ключ одразу — він показується тільки один раз

API_KEY = "YOUR_API_KEY_HERE"   # вставте ваш ключ
INDEX_NAME = "articles-index"
DIM = 384

pc = Pinecone(api_key=API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Створюємо serverless-індекс — якщо вже є, пропускаємо
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Індекс '{INDEX_NAME}' створено")
else:
    print(f"Індекс '{INDEX_NAME}' вже існує")

index = pc.Index(INDEX_NAME)

# Завантажуємо дані з того самого CSV
rows = []
with open("articles.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

texts = [f"{r['title']}.{r['text']}" for r in rows]
embeddings = model.encode(texts, normalize_embeddings=True)

# Формуємо вектори для upsert
vectors = [
    {
        "id": row["id"],
        "values": emb.tolist(),
        "metadata": {
            "title": row["title"],
            "topic": row["topic"],
            "year": int(row["year"]),
            "lang": row["lang"],
            "text": row["text"],
        },
    }
    for emb, row in zip(embeddings, rows)
]

# namespace — логічне розділення всередині індексу
# Аналог схеми (schema) у PostgreSQL
index.upsert(vectors=vectors, namespace="science")

import time
print("Чекаємо кілька секунд поки індекс оновиться...")
time.sleep(3)

stats = index.describe_index_stats()
print(f"Всього векторів в індексі: {stats['total_vector_count']}")
print(f"Namespace 'science': {stats['namespaces'].get('science', {}).get('vector_count', 0)} векторів")