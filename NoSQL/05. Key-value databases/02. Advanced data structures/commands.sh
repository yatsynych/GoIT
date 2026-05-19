# Запуск контейнера
docker-compose up -d

# 2.1 Sorted Sets — лідерборд // -B опція для вимкнення кешування байт-коду, що дозволяє бачити зміни в коді без перезапуску контейнера
docker exec -it python_redis_client python -B leaderboard.py

# 2.2 Sorted Sets як черга з пріоритетом
docker exec -it python_redis_client python -B task_queue.py

# 2.3 HyperLogLog — підрахунок унікальних відвідувачів
docker exec -it python_redis_client python -B analytics.py