import numpy as np
import os

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

# Наша "база знань" — кілька речень із різних тематичних областей
corpus = [
    "A cat is sleeping on the couch.",
    "The feline is resting on the sofa.",
    "Dogs love to play fetch in the park.",
    "The stock market crashed this morning.",
    "Neural networks learn from large datasets.",
    "My dog enjoys running and jumping.",
]

query = "A kitten is lying on the sofa."

# Нормалізуємо — модель рекомендує cosine, на нормалізованих він = L2
corpus_emb = model.encode(corpus, normalize_embeddings=True)
query_emb  = model.encode(query,  normalize_embeddings=True)

scores = cosine_similarity([query_emb], corpus_emb)[0]
ranked = np.argsort(scores)[::-1]

print(f"\n\n\nЗапит: '{query}'")
print()
print("Результати (за спаданням релевантності):\n")
for rank, idx in enumerate(ranked, 1):
    bar = "█" * int(max(scores[idx], 0) * 30)
    print(f"{rank}. [{scores[idx]:+.4f}]{bar}")
    print(f"{corpus[idx]}")
    print()