from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Кішка спить на дивані.",
    "Пухнастий кіт лежить на дивані.",
    "Фондовий ринок обвалився сьогодні вранці.",
]

embeddings = model.encode(sentences)

print(f"\n\n\nФорма масиву ембеддингів: {embeddings.shape}")
print(f"Розмірність одного вектора: {embeddings.shape[1]}")
print(f"Тип даних: {embeddings.dtype}")
print(f"\nПерші 8 компонент першого вектора:")
print(f"{embeddings[0][:8]}")
print()

# Дивимося на числа — вони нічого не значать самі по собі
# Важливі лише відстані між векторами
print("Важливо не значення компонент, а відстані між векторами:")
print()

# Евклідова відстань
def l2(a, b):
    return float(np.linalg.norm(a - b))

pairs = [(0, 1, "кішка ↔ кіт"), (0, 2, "кішка ↔ ринок"), (1, 2, "кіт ↔ ринок")]
for i, j, label in pairs:
    d = l2(embeddings[i], embeddings[j])
    print(f"  L2 ({label}) = {d:.4f}")