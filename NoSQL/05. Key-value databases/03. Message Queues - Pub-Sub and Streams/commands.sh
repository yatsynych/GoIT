# Запуск контейнера
docker-compose up -d

# 3.1 Pub/Sub — прості сповіщення
# Термінал 1
docker exec -it python_redis_client python -B subscriber.py

# Термінал 2 (поки subscriber.py працює)
docker exec -it python_redis_client python -B publisher.py

# 3.2 Streams — надійна обробка замовлень
docker exec -it python_redis_client python -B stream_run.py