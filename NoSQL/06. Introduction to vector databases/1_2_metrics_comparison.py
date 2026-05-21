import numpy as np
import os

# Очищення консолі для кращої візуалізації результатів
os.system('cls' if os.name == 'nt' else 'clear')

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def cosine_distance(a, b):
    return 1 - cosine_similarity(a, b)

def l2_distance(a, b):
    return float(np.linalg.norm(a - b))

def dot_product(a, b):
    return float(np.dot(a, b))

# Три вектори у 2D — легко візуалізувати
a = np.array([1.0, 0.0])       # вправо
b = np.array([3.0, 0.0])       # теж вправо, але довший
c = np.array([0.0, 1.0])       # вгору

print("=" * 55)
print("Вектор a = [1, 0]  — вправо")
print("Вектор b = [3, 0]  — теж вправо, але довший")
print("Вектор c = [0, 1]  — вгору (перпендикулярний a і b)")
print("=" * 55)

print()
print("Cosine Similarity (кут між векторами, [-1, 1]):")
print(f"  cosine(a, b) = {cosine_similarity(a, b):.4f}  ← один напрямок → максимум")
print(f"  cosine(a, c) = {cosine_similarity(a, c):.4f}  ← перпендикуляр → нуль")

print()
print("L2 Distance (геометрична відстань, [0, ∞)):")
print(f"  L2(a, b) = {l2_distance(a, b):.4f}  ← b довший, значить вони далеко один від одного")
print(f"  L2(a, c) = {l2_distance(a, c):.4f}  ← однакова довжина, різний напрямок")

print()
print("Dot Product (враховує і кут, і довжину):")
print(f"  dot(a, b) = {dot_product(a, b):.4f}  ← b довший → більше")
print(f"  dot(a, c) = {dot_product(a, c):.4f}  ← перпендикуляр → нуль")

print()
print("=" * 55)
print("Що відбувається після нормалізації?")
print("=" * 55)

a_n = a / np.linalg.norm(a)
b_n = b / np.linalg.norm(b)

print(f"\nПісля нормалізації: a_n = {a_n}, b_n = {b_n}")
print("Вони збіглися — обидва [1, 0]")
print(f"  L2(a_n, b_n)     = {l2_distance(a_n, b_n):.4f}  ← 0, ідентичні")
print(f"  cosine(a_n, b_n) = {cosine_similarity(a_n, b_n):.4f}  ← 1, ідентичні")
print(f"  dot(a_n, b_n)    = {dot_product(a_n, b_n):.4f}  ← теж 1")
print()
print("Висновок: на нормалізованих векторах усі три метрики дають однаковий ПОРЯДОК результатів.")
print("Тому багато моделей нормалізують ембеддинги при генерації — і використовують L2 для швидкості.")