import csv
import chromadb
import os
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# Підключаємо нашу модель як функцію ембеддингу
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./articles_db")

# Пересоздаємо колекцію для чистоти експерименту
client.delete_collection("articles") if "articles" in [c.name for c in client.list_collections()] else None
collection = client.create_collection(
    name="articles",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

# Завантажуємо дані з CSV
ids, documents, metadatas = [], [], []
with open("articles.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        ids.append(row["id"])
        documents.append(f"{row['title']}.{row['text']}")  # об'єднуємо заголовок і текст
        metadatas.append({
            "title": row["title"],
            "topic": row["topic"],
            "year":  int(row["year"]),
            "lang":  row["lang"],
        })

collection.add(ids=ids, documents=documents, metadatas=metadatas)

print(f"\n\n\nЗавантажено {collection.count()} статей у колекцію 'articles'\n")

# Перевіряємо: шукаємо без фільтрів
results = collection.query(
    query_texts=["how do transformers process text"],
    n_results=3,
    include=["documents", "metadatas", "distances"],
)

print("Топ-3 за запитом 'how do transformers process text':\n")
for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print(f"  [{dist:.4f}] ({meta['topic']}, {meta['year']}) {meta['title']}")