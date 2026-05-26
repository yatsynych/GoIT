import faiss
import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

np.random.seed(42)
d, n = 128, 100_000
xb = np.random.randn(n, d).astype(np.float32)
xq = np.random.randn(5, d).astype(np.float32)

# Еталон -- точний brute-force
index_flat = faiss.IndexFlatL2(d)
index_flat.add(xb)
_, I_exact = index_flat.search(xq, k=10)

# HNSW індекс
M = 32  # ребер на вершину
index_hnsw = faiss.IndexHNSWFlat(d, M)
index_hnsw.hnsw.efConstruction = 64  # якість побудови графа
index_hnsw.add(xb)

for ef in [16, 32, 64, 128]:
    index_hnsw.hnsw.efSearch = ef
    _, I_hnsw = index_hnsw.search(xq, k=10)
    recall = sum(
        len(set(I_hnsw[i]) & set(I_exact[i])) / 10
        for i in range(len(xq))
    ) / len(xq)
    print(f"efSearch = {ef:4d} → recall@10 = {recall:.3f}")