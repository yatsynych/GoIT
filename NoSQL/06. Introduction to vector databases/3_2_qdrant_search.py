from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny, Range
from sentence_transformers import SentenceTransformer
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# host_name = "localhost"
host_name = "qdrant"
client = QdrantClient(host=host_name, port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION = "articles"
query = "neural network architectures for images"
query_vec = model.encode(query, normalize_embeddings=True).tolist()

print(f"Запит: '{query}'")
print()

print("=" * 55)
print("1. Без фільтра")
print("=" * 55)
results = client.query_points(
    collection_name=COLLECTION,
    query=query_vec,
    limit=3,
    with_payload=True,
)
for hit in results.points:
    print(f"  [{hit.score:.4f}] [{hit.payload['topic']}] "
          f"{hit.payload['title']} ({hit.payload['year']})")

print()
print("=" * 55)
print("2. Тільки Computer Vision (topic=cv)")
print("=" * 55)
results = client.query_points(
    collection_name=COLLECTION,
    query=query_vec,
    limit=3,
    query_filter=Filter(
        must=[FieldCondition(key="topic", match=MatchValue(value="cv"))]
    ),
    with_payload=True,
)
for hit in results.points:
    print(f"  [{hit.score:.4f}] [{hit.payload['topic']}] "
          f"{hit.payload['title']} ({hit.payload['year']})")

print()
print("=" * 55)
print("3. NLP або ML, починаючи з 2019 року")
print("=" * 55)
results = client.query_points(
    collection_name=COLLECTION,
    query=query_vec,
    limit=3,
    query_filter=Filter(
        must=[
            FieldCondition(key="topic", match=MatchAny(any=["nlp", "ml"])),
            FieldCondition(key="year",  range=Range(gte=2019)),
        ]
    ),
    with_payload=True,
)
for hit in results.points:
    print(f"  [{hit.score:.4f}] [{hit.payload['topic']}] "
          f"{hit.payload['title']} ({hit.payload['year']})")

print()
print("Зверніть увагу: score у Qdrant — це similarity (більше = краще).")
print("У Chroma — distance (менше = краще). Різний сенс одного поля!")