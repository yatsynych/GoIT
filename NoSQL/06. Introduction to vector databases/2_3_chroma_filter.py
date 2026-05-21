import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./articles_db")
collection = client.get_collection("articles", embedding_function=embedding_fn)

query = "neural network architectures for images"

print(f"Запит: '{query}'")
print(f"Всього статей у колекції: {collection.count()}")
print()

print("=" * 55)
print("1. Без фільтра — всі статті")
print("=" * 55)
results = collection.query(
    query_texts=[query],
    n_results=3,
    include=["metadatas", "distances"],
)
for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] [{meta['topic']}]{meta['title']} ({meta['year']})")

print()
print("=" * 55)
print("2. Тільки статті з Computer Vision (topic=cv)")
print("=" * 55)
results = collection.query(
    query_texts=[query],
    n_results=3,
    where={"topic": {"$eq": "cv"}},
    include=["metadatas", "distances"],
)
for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] [{meta['topic']}] {meta['title']} ({meta['year']})")

print()
print("=" * 55)
print("3. Статті 2021 року і пізніше (year >= 2021)")
print("=" * 55)
results = collection.query(
    query_texts=[query],
    n_results=3,
    where={"year": {"$gte": 2021}},
    include=["metadatas", "distances"],
)
for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] [{meta['topic']}] {meta['title']} ({meta['year']})")

print()
print("=" * 55)
print("4. Комбінований фільтр: NLP або ML, не старше 2019")
print("=" * 55)
results = collection.query(
    query_texts=[query],
    n_results=3,
    where={
        "$and": [
            {"topic": {"$in": ["nlp", "ml"]}},
            {"year": {"$gte": 2019}},
        ]
    },
    include=["metadatas", "distances"],
)
for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] [{meta['topic']}] {meta['title']} ({meta['year']})")