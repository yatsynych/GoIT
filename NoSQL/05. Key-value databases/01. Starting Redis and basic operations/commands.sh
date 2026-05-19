# Підготовка (скачування образу Redis)
docker pull redis:7.2-alpine

#######################
# 1.1 Запуск контейнера
#######################
docker-compose up -d

# Перевірка статусу контейнера
docker-compose ps

# Підключення до Redis CLI
docker exec -it app-redis redis-cli

# Виконання команд Redis. Очікуваний результат: PONG
PING

# 

########################################
# 1.2 Рядки: базова модель ключ-значення
########################################

SET user:1001:name "Alice"
GET user:1001:name

SET user:1001:age 29
GET user:1001:age

SET user:1002:name "Bob"
SET user:1002:age 34

# Дивимося що у нас є
KEYS user:*

# Видалення ключа
DEL user:1002:name

# Перевірка наявності ключів
EXISTS user:1002:name
EXISTS user:1001:name

###########################
# 1.3 TTL — час життя ключа
###########################
SET session:abc123 "user_id:1001"
EXPIRE session:abc123 10
TTL session:abc123

# Через 10 секунд
TTL session:abc123
GET session:abc123

# Встановити ключ і TTL однією командою
SETEX session:xyz789 30 "user_id:1002"
TTL session:xyz789

#########################
# 1.4 Атомарні лічильники
#########################
SET page:home:views 0
INCR page:home:views
INCR page:home:views
INCR page:home:views
GET page:home:views

INCRBY page:home:views 10
GET page:home:views

DECR page:home:views
GET page:home:views

##################################
# 1.5 Хеші — структуровані об’єкти
##################################
HSET user:1001 name "Alice" email "alice@example.com" age 29
HGET user:1001 name
HGET user:1001 email
HGETALL user:1001
HKEYS user:1001
HVALS user:1001

HSET user:1001 age 30
HGET user:1001 age

HDEL user:1001 age
HGETALL user:1001
