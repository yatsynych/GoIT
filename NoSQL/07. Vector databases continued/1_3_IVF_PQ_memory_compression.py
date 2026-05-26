import faiss
import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

np.random.seed(42)
d = 384
n = 100_000
k = 5

nlist, m, nbits = 256, 32, 8

xb = np.random.randn(n, d).astype(np.float32)
xq = np.random.randn(1, d).astype(np.float32)

# Точний пошук
index_flat = faiss.IndexFlatL2(d)
index_flat.add(xb)
_, I_exact = index_flat.search(xq, k)
print("Exact: ", I_exact[0])

# IVF+PQ
quantizer = faiss.IndexFlatL2(d)
index_ivfpq = faiss.IndexIVFPQ(quantizer, d, nlist, m, nbits)
index_ivfpq.train(xb)
index_ivfpq.add(xb)
index_ivfpq.nprobe = 16

_, I_approx = index_ivfpq.search(xq, k)
print("IVF+PQ:", I_approx[0], "\n")

# Порівняння пам'яті
size_flat  = n * d * 4    # float32 = 4 байти
size_ivfpq = n * m        # m байт на вектор після стиснення
print(f"Flat:      {size_flat  / 1e6:.1f} МБ")
print(f"IVF+PQ:    {size_ivfpq / 1e6:.1f} МБ")
print(f"Стиснення: {size_flat // size_ivfpq}x")