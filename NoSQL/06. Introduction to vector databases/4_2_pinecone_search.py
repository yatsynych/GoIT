import os

from pinecone import Pinecone
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

pc = Pinecone(api_key=API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")
index = pc.Index(INDEX_NAME)

query = "neural network architectures for images"
query_vec = model.encode(query, normalize_embeddings=True).tolist()

print(f"Запит: '{query}'")
print()

print("=" * 55)
print("1. Без фільтра")
print("=" * 55)
results = index.query(
    namespace="science",
    vector=query_vec,
    top_k=3,
    include_metadata=True,
)
for match in results.matches:
    print(f"  [{match.score:.4f}] [{match.metadata['topic']}] "
          f"{match.metadata['title']} ({match.metadata['year']})")

print()
print("=" * 55)
print("2. Тільки Computer Vision + рік >= 2020")
print("=" * 55)
results = index.query(
    namespace="science",
    vector=query_vec,
    top_k=3,
    include_metadata=True,
    filter={
        "$and": [
            {"topic": {"$eq": "cv"}},
            {"year":  {"$gte": 2020}},
        ]
    },
)
for match in results.matches:
    print(f"  [{match.score:.4f}] [{match.metadata['topic']}] "
          f"{match.metadata['title']} ({match.metadata['year']})")

print()
print("=" * 55)
print("3. NLP або ML (оператор $in)")
print("=" * 55)
results = index.query(
    namespace="science",
    vector=query_vec,
    top_k=3,
    include_metadata=True,
    filter={"topic": {"$in": ["nlp", "ml"]}},
)
for match in results.matches:
    print(f"  [{match.score:.4f}] [{match.metadata['topic']}] "
          f"{match.metadata['title']} ({match.metadata['year']})")

print()
print("score у Pinecone — це cosine similarity (більше = краще).")
print("Такий самий сенс як у Qdrant. Відрізняється від Chroma (там distance).")