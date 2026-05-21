from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# host_name = "localhost"
host_name = "qdrant"
client = QdrantClient(host=host_name, port=6333)

model = SentenceTransformer("all-MiniLM-L6-v2")

def find_similar_topic(topic: str, query: str, top_k: int = 3):
    query_vec = model.encode(query, normalize_embeddings=True).tolist()
    results = client.query_points(
        collection_name="articles",
        query=query_vec,
        limit=top_k,
        query_filter=Filter(
            must=[FieldCondition(key="topic", match=MatchValue(value=topic))]
        ),
        with_payload=True,
    )
    return [(hit.score, hit.payload["title"]) for hit in results.points]

# Тест
for topic, query in [
    ("nlp",  "how to generate text with language models"),
    ("cv",   "image classification deep learning"),
    ("db",   "fast vector similarity search"),
]:
    print(f"\nТема: {topic}, Запит: '{query}'")
    for score, title in find_similar_topic(topic, query):
        print(f"  [{score:.4f}] {title}")