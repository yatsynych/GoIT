# Очистка попереднього кластера і даних (якщо потрібно)
docker-compose down --volumes --remove-orphans

# Запуск
docker-compose up -d --build
docker-compose ps

# 1.1. HNSW: вплив efSearch на recall
docker exec -it python_vector_client python 1_1_HNSW_efSearch_impact_on_recall_HNSW_efSearch_impact_on_recall.py

# 1.2. IVF: кластеризація простору
docker exec -it python_vector_client python 1_2_IVF_clustering_IVF_clustering.py

# 1.3. IVF+PQ: стиснення пам’яті
docker exec -it python_vector_client python 1_3_IVF_PQ_memory_compression.py

# 2.1. Fixed-size: просто і передбачувано
docker exec -it python_vector_client python 2_1_fixed_size_fixed_size.py

# 2.2. Semantic chunking: за змістом
docker exec -it python_vector_client python 2_2_semantic_chunking_semantic_chunking.py

# 3.1. Гібридний пошук: BM25 + RRF + Qdrant
docker exec -it python_vector_client python 3_1_hybrid_search_BM25_RRF_Qdrant.py

# 3.2. RRF вручну: зрозуміти механіку
docker exec -it python_vector_client python 3_2_RRF_manually_understand_mechanics.py

# 3.3. Гібридний пошук у Qdrant
docker exec -it python_vector_client python 3_3_hybrid_search_Qdrant.py