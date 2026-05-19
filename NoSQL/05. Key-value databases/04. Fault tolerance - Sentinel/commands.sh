# 4.0 Очистка попереднього кластера і даних
docker-compose down --volumes --remove-orphans

# 4.1 Запуск Sentinel-кластера
docker-compose up -d
docker-compose ps

# 4.2 Перевіряємо реплікацію

# Записуємо дані в мастер
docker exec -it redis-master redis-cli SET important:data "TOP SECRET"
docker exec -it redis-master redis-cli GET important:data

# Читаємо з репліки
docker exec -it redis-replica-1 redis-cli GET important:data
docker exec -it redis-replica-2 redis-cli GET important:data

# Пишемо в репліку (не повинно працювати)
docker exec -it redis-replica-1 redis-cli SET test "Trying to overwrite"

# Перевіряємо стан через Sentinel
docker exec -it sentinel-1 redis-cli -p 26379 SENTINEL masters

# 4.3 Імітуємо відмову майстра

# 4.3.1 Запускаємо моніторинг логів в окремому терміналі
docker logs -f sentinel-1

# 4.3.2 Імітуємо відмову майстра в іншому терміналі
docker stop redis-master

# 4.3.3 Перевіряємо хто тепер мастер
docker exec -it sentinel-1 redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster

# 4.3.4 Читаємо дані від нового мастера:
docker exec -it redis-replica-1 redis-cli GET important:data

# 4.4 Підключення з Python через Sentinel
docker run -it --rm \
  --network 04faulttolerance-sentinel_redis-net \
  -v "$(pwd)/sentinel_client.py:/sentinel_client.py" \
  python:3.11 bash -c "pip install redis -q && python /sentinel_client.py"



  docker run -it --rm \
  --network 04faulttolerance-sentinel_redis-net \
  -v "$(pwd)/test.py:/test.py" \
  python:3.11 bash -c "pip install redis -q && python /test.py"