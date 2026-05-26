import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

def reciprocal_rank_fusion(
    rankings: List[List[int]], k: int = 60
) -> List[Tuple[int, float]]:
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

corpus = [
    "Apache Kafka is a distributed event streaming platform.",
    "Kafka 3.6 release notes detail various improvements and fixes.",
    "The changelog for Apache Kafka 3.7 includes bug fixes and new features.",
    "Introduction to distributed messaging systems and Kafka basics.",
    "Kafka version 3.7 documentation provides detailed upgrade instructions."
]

model = SentenceTransformer("all-MiniLM-L6-v2")
bm25_idx = BM25Okapi([doc.lower().split() for doc in corpus])
embs = model.encode(corpus, normalize_embeddings=True)

query = "Kafka changelog version 3.7"
q_emb = model.encode([query], normalize_embeddings=True)[0]

vec_scores  = np.dot(embs, q_emb)
vec_ranking = list(np.argsort(vec_scores)[::-1])

bm25_scores  = bm25_idx.get_scores(query.lower().split())
bm25_ranking = list(np.argsort(bm25_scores)[::-1])

fused = reciprocal_rank_fusion([vec_ranking, bm25_ranking])

print("=== Тільки векторний пошук ===")
for idx in vec_ranking[:3]:
    print(f"  [{vec_scores[idx]:.3f}]{corpus[idx]}")

print("\\n=== Тільки BM25 ===")
for idx in bm25_ranking[:3]:
    print(f"  [{bm25_scores[idx]:.3f}]{corpus[idx]}")

print("\\n=== Гібридний RRF ===")
for doc_id, score in fused[:3]:
    print(f"  [RRF={score:.4f}]{corpus[doc_id]}")
