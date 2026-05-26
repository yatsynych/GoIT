import faiss
import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

np.random.seed(42)

d = 128
n = 100_000
nlist = 300
k = 10

xb = np.random.randn(n, d).astype(np.float32)
xq = np.random.randn(5, d).astype(np.float32)

# Еталон
index_flat = faiss.IndexFlatL2(d)
index_flat.add(xb)
_, I_exact = index_flat.search(xq, k)

# IVF
quantizer = faiss.IndexFlatL2(d)
index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist)
index_ivf.train(xb)   # ← обов'язково перед add!
index_ivf.add(xb)
index_ivf.nprobe = 30  # скільки кластерів перевіряти

_, I_ivf = index_ivf.search(xq, k)
recall = sum(
    len(set(I_ivf[i]) & set(I_exact[i])) / k
    for i in range(len(xq))
) / len(xq)

print(f"Recall@{k} (nprobe=30): {recall:.3f}")
