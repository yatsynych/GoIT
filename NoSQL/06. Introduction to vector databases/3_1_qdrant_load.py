import uuid
import csv
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PayloadSchemaType
from sentence_transformers import SentenceTransformer

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# host_name = "localhost"
host_name = "qdrant"
client = QdrantClient(host=host_name, port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

DIM = 384
COLLECTION = "articles"


# Пересоздаємо колекцію
if client.collection_exists(collection_name=COLLECTION):
    client.delete_collection(collection_name=COLLECTION)
client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
)


# Створюємо payload-індекси ВІДРАЗУ — до завантаження даних
# Це аналог CREATE INDEX у SQL: прискорює фільтрацію за цими полями
client.create_payload_index(
    collection_name=COLLECTION,
    field_name="topic",
    field_schema=PayloadSchemaType.KEYWORD,  # рядки з точним збігом
)
client.create_payload_index(
    collection_name=COLLECTION,
    field_name="year",
    field_schema=PayloadSchemaType.INTEGER,  # числа з range-запитами
)
print(f"\nPayload-індекси створено")

# Завантажуємо дані з того самого CSV
rows = []
with open("articles.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

texts = [f"{r['title']}.{r['text']}" for r in rows]
embeddings = model.encode(texts, normalize_embeddings=True)

# Формуємо точки (points) — основна одиниця даних у Qdrant
points = [
    PointStruct(
        id=str(uuid.uuid4()),            # UUID як ID
        vector=emb.tolist(),
        payload={
            "original_id": row["id"],
            "title": row["title"],
            "topic": row["topic"],
            "year": int(row["year"]),
            "lang": row["lang"],
            "text": row["text"],
        },
    )
    for emb, row in zip(embeddings, rows)
]

client.upsert(collection_name=COLLECTION, points=points)

info = client.get_collection(COLLECTION)
print(f"Завантажено{info.points_count} точок у колекцію '{COLLECTION}'")
print()
print("Відкрийте http://localhost:6333/dashboard — колекція з'явилася!")