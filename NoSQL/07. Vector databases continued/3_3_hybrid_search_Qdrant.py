from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams,
    SparseVectorParams, SparseIndexParams,
    PointStruct, SparseVector,
    FusionQuery, Fusion,
)
from sentence_transformers import SentenceTransformer
import os

# host_name = "localhost"
host_name = "qdrant"
client = QdrantClient(host=host_name, port=6333)
collection_name = "hybrid_demo"

corpus = [
    "Apache Kafka is a distributed event streaming platform.",
    "Kafka 3.6 release notes detail various improvements and fixes.",
    "The changelog for Apache Kafka 3.7 includes bug fixes and new features.",
    "Introduction to distributed messaging systems and Kafka basics.",
    "Kafka version 3.7 documentation provides detailed upgrade instructions."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
dense_vecs = model.encode(corpus, normalize_embeddings=True)

def text_to_sparse(text: str, vocab_size: int = 30000) -> SparseVector:
    """Спрощений sparse-вектор через хеші слів — тільки для демонстрації."""
    indices, values = [], []
    for word in text.lower().split():
        idx = abs(hash(word)) % vocab_size
        if idx not in indices:
            indices.append(idx)
            values.append(1.0)
    return SparseVector(indices=indices, values=values)

# Створюємо колекцію з двома типами векторів
# 1. Перевіряємо, чи існує колекція
if client.collection_exists(collection_name=collection_name):
    # 2. Якщо існує — видаляємо її, щоб почати "з чистого аркуша"
    client.delete_collection(collection_name=collection_name)

# 3. Створюємо колекцію з явною конфігурацією двох типів векторів
client.create_collection(
    collection_name=collection_name,
    # Конфігурація для щільних (dense) векторів (семантичний пошук)
    vectors_config={
        "dense": VectorParams(size=384, distance=Distance.COSINE)
    },
    # Конфігурація для розріджених (sparse) векторів (лексичний пошук)
    sparse_vectors_config={
        "sparse": SparseVectorParams(index=SparseIndexParams(on_disk=False))
    },
)

# Завантажуємо дані
points = [
    PointStruct(
        id=i,
        vector={
            "dense":  dense_vecs[i].tolist(),
            "sparse": text_to_sparse(corpus[i]),
        },
        payload={"text": corpus[i]},
    )
    for i in range(len(corpus))
]
client.upsert(collection_name=collection_name, points=points)

# Гібридний запит
query = "Kafka 3.7 replication improvements"
query_dense  = model.encode([query], normalize_embeddings=True)[0].tolist()
query_sparse = text_to_sparse(query)

results = client.query_points(
    collection_name=collection_name,
    prefetch=[
        {"query": query_dense,               "using": "dense",  "limit": 5},
        {"query": query_sparse.model_dump(), "using": "sparse", "limit": 5},
    ],
    query=FusionQuery(fusion=Fusion.RRF),
    limit=3,
    with_payload=True,
)

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

print("Гібридні результати Qdrant (RRF):")
for point in results.points:
    print(f"   Score: {point.score:.4f} | {point.payload['text']}")
