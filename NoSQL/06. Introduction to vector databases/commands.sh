# Очистка попереднього кластера і даних (якщо потрібно)
docker-compose down --volumes --remove-orphans

# Запуск
docker-compose up -d --build
docker-compose ps



### Частина 1. Ембеддинги та метрики

# 1.1. Перші ембеддиг
docker exec -it python_vector_client python 1_1_embeddings_intro.py

# 1.2. Три метрики — в чому різниця
docker exec -it python_vector_client python 1_2_metrics_comparison.py

# 1.3. Семантичний пошук — в чому сенс
docker exec -it python_vector_client python 1_3_semantic_search.py



### Частина 2. Chroma — локальна векторна база без інфраструктури

# 2.1. Встановлення і перший запуск
docker exec -it python_vector_client python 2_1_chroma_intro.py

# 2.2. Реальний датасет: статті про технології
docker exec -it python_vector_client python 2_2_chroma_load.py

# 2.3. Фільтрація за метаданими
docker exec -it python_vector_client python 2_3_chroma_filter.py



### Частина 3. Qdrant — production-ready векторна база

# 3.1. Створення колекції і завантаження даних
docker exec -it python_vector_client python 3_1_qdrant_load.py

# 3.2. Пошук і порівняння з Chroma
docker exec -it python_vector_client python 3_2_qdrant_search.py

# 3.3. Самостійне завдання (10 хвилин)
# Умова: напишіть функцію `find_similar_topic(topic, query, top_k=3)`, яка:
#   - Приймає тему (`"nlp"`, `"cv"`, `"ml"`, `"db"`) і текстовий запит
#   - Шукає у Qdrant тільки статті за цією темою
#   - Повертає топ-`k` результатів
# Перевірте її з кількома парами (тема, запит).
#
# Очікуване рішення
docker exec -it python_vector_client python 3_3_qdrant_search_ext.py



### Частина 4. Pinecone — managed-сервіс і гібридний пошук

# 4.1. Створення індексу і завантаження даних
docker exec -it python_vector_client python 4_1_pinecone_load.py

# 4.2. Пошук з фільтрацією
docker exec -it python_vector_client python 4_2_pinecone_search.py