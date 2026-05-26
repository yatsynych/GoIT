from rank_bm25 import BM25Okapi
import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

corpus = [
    "Transformer models use attention mechanisms to process sequences.",
    "Apache Kafka is a distributed event streaming platform.",
    "Vector databases store high-dimensional embeddings for similarity search.",
    "BM25 is a probabilistic ranking algorithm used in information retrieval.",
    "Kafka 3.7 introduced improvements to replication and partition assignment.",
]

bm25 = BM25Okapi([doc.lower().split() for doc in corpus])
query = "Kafka 3.7 replication improvements"
scores = bm25.get_scores(query.lower().split())

print("BM25 Rankings:")
for rank, idx in enumerate(np.argsort(scores)[::-1][:3]):
    print(f"{rank+1}. [{scores[idx]:.3f}] {corpus[idx]}")
