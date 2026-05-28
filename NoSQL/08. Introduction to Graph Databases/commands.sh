# 1. Модель даних: Tags, Fields і кардинальність

# 1.1.Запустити Neo4j
docker compose up -d

# Відкрити в браузері http://localhost:7474
# Authentication type: Username / Password
# Username: neo4j
# Password: secret12345


# 1.2. Проблема дублювання: CREATE проти MERGE

# Створення вузла Person з властивостями name та city
# Виконуємо тричі
CREATE (:Person {name: "Alice", city: "Berlin"})

# Проблема дублювання: CREATE проти MERGE
MATCH (p:Person {name: "Alice"})
RETURN count(p) AS alice_count

# Очистити
MATCH (p:Person {name: "Alice"}) DETACH DELETE p

# Правильний підхід
MERGE (p:Person {name: "Alice"})
SET p.city = "Berlin"
RETURN p

# Виконати три рази поспіль і знову перевірити
MATCH (p:Person {name: "Alice"})
RETURN count(p) AS alice_count

# 1.3. Проблема кардинальності: вузол проти властивості
CREATE (:Action {user_id: "u-0001", event: "login", ts: "2024-01-15T10:00:00Z"})
CREATE (:Action {user_id: "u-0002", event: "login", ts: "2024-01-15T10:00:01Z"})
CREATE (:Action {user_id: "u-0003", event: "login", ts: "2024-01-15T10:00:02Z"})
# ... і так далі для 100 000 записів

# Правильна модель
MERGE (u:User {id: "u-0001"})
MERGE (p:Page {url: "/dashboard"})
MERGE (u)-[:VISITED {count: 5, last_at: "2024-01-15"}]->(p)

# Видалемо всі дані в базі (для чистоти експерименту)
MATCH (n)
DETACH DELETE n;

# 2 Мова запитів Cypher: MATCH, OPTIONAL MATCH, WITH
# 2.1. Створити граф для роботи

# 2.1.1. Люди
CREATE
  (alice:Person {name: "Alice", age: 30, city: "Berlin"}),
  (bob:Person {name: "Bob", age: 28, city: "Hamburg"}),
  (carol:Person {name: "Carol", age: 35, city: "Berlin"}),
  (dave:Person {name: "Dave", age: 40, city: "Munich"}),
  (eva:Person {name: "Eva", age: 25, city: "Berlin"}),
  (henry:Person {name: "Henry", age: 45, city: "Munich"})

# 2.1.2. Фільми
CREATE
  (inception:Movie {title: "Inception", year: 2010}),
  (matrix:Movie {title: "The Matrix", year: 1999}),
  (interstellar:Movie {title: "Interstellar", year: 2014}),
  (godfather:Movie {title: "The Godfather", year: 1972})

# 2.1.3. Дружба та перегляди
MATCH (alice:Person {name: "Alice"}), (bob:Person {name: "Bob"}),
      (carol:Person {name: "Carol"}), (dave:Person {name: "Dave"}),
      (eva:Person {name: "Eva"}), (henry:Person {name: "Henry"}),
      (inception:Movie {title: "Inception"}), (matrix:Movie {title: "The Matrix"}),
      (interstellar:Movie {title: "Interstellar"}), (godfather:Movie {title: "The Godfather"})
CREATE
  (alice)-[:FRIENDS_WITH]->(bob),
  (alice)-[:FRIENDS_WITH]->(eva),
  (alice)-[:FRIENDS_WITH]->(carol),
  (bob)-[:FRIENDS_WITH]->(dave),
  (dave)-[:FRIENDS_WITH]->(henry),
  (alice)-[:WATCHED {rating: 5}]->(inception),
  (alice)-[:WATCHED {rating: 4}]->(interstellar),
  (bob)-[:WATCHED {rating: 4}]->(inception),
  (bob)-[:WATCHED {rating: 5}]->(matrix),
  (carol)-[:WATCHED {rating: 5}]->(matrix),
  (carol)-[:WATCHED {rating: 5}]->(godfather),
  (eva)-[:WATCHED {rating: 3}]->(inception),
  (eva)-[:WATCHED {rating: 5}]->(interstellar),
  (henry)-[:WATCHED {rating: 5}]->(godfather)

# 2.2. Пастка №1: MATCH як INNER JOIN
MATCH (p:Person)-[:WATCHED]->(m:Movie)
WHERE p.age > 28
RETURN p.name, count(m) AS watched_count
ORDER BY watched_count DESC

# Правильне рішення
MATCH (p:Person)
WHERE p.age > 28
OPTIONAL MATCH (p)-[:WATCHED]->(m:Movie)
RETURN p.name, count(m) AS watched_count
ORDER BY watched_count DESC

# Пастка №2: агрегат у WHERE
MATCH (p:Person)-[:FRIENDS_WITH]->(friend:Person)
WHERE count(friend) > 2
RETURN p.name, count(friend) AS friend_count

# Правильне рішення
MATCH (p:Person)-[:FRIENDS_WITH]->(friend:Person)
WITH p, count(friend) AS friend_count
WHERE friend_count > 2
RETURN p.name, friend_count
ORDER BY friend_count DESC

# Ще одна пастка: агрегація без WITH
MATCH (p:Person)-[:FRIENDS_WITH]->(friend:Person)
RETURN p.name, count(friend) AS friend_count
ORDER BY friend_count DESC

# 3. Обхід графа: шляхи та змінна довжина
# 3.1. Pнайти фільми, які дивилися друзі Alice, але яких сама Alice не бачила

MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend:Person)
MATCH (friend)-[:WATCHED]->(m:Movie)
MATCH (alice)-[:WATCHED]->(m)
RETURN DISTINCT m.title

# Правильне рішення
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)-[:WATCHED]->(m:Movie)
WHERE NOT (alice)-[:WATCHED]->(m)
RETURN DISTINCT m.title, count(friend) AS recommended_by
ORDER BY recommended_by DESC

# 3.2. Глибина обходу та продуктивність
# 3.2.1. Глибина 1 — тільки прямі друзі
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH*1..1]->(p:Person)
RETURN DISTINCT p.name

# 3.2.2. Глибина 2 — друзі та друзі друзів
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH*1..2]->(p:Person)
RETURN DISTINCT p.name

# 3.2.3. Глибина 3 — друзі, друзі друзів і далі
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH*1..3]->(p:Person)
RETURN DISTINCT p.name

# 3.2.4. Без обмеження глибини — всі досяжні друзі
# Антепатерн, не робіть так на продакшені
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH*]->(p:Person)
RETURN DISTINCT p.name

# 3.3. shortestPath: правильний і неправильний спосіб
# Найкоротший шлях між Alice та Henry
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Henry"})
MATCH path = (a)-[:FRIENDS_WITH*]->(b)
RETURN path, length(path)
ORDER BY length(path)
LIMIT 1

# Правильно – вбудований BFS, зупиняється при першому знайденому шляху
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Henry"})
MATCH path = shortestPath((a)-[:FRIENDS_WITH*]-(b))
RETURN path, length(path)

# Вивести всі вузли вздовж шляху
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Henry"})
MATCH path = shortestPath((a)-[:FRIENDS_WITH*]-(b))
RETURN [n IN nodes(path) | n.name] AS chain, length(path) AS hops

# 4. Продуктивність: індекси та EXPLAIN
# 4.1. Повне сканування: EXPLAIN до індексу
EXPLAIN
MATCH (p:Person {name: "Alice"})
RETURN p

# Додати індекс
CREATE INDEX person_name_idx FOR (p:Person) ON (p.name)

# Порівняти
EXPLAIN
MATCH (p:Person {name: "Alice"})
RETURN p

# 4.2. Індекс по неправильному полю
# Створюємо індекс по city
CREATE INDEX person_city_idx FOR (p:Person) ON (p.city)

# Видаляємо старий індекс по імені, щоб він не заважав демонстрації
DROP INDEX person_name_idx

# Фільтруємо по name — індекс по city не допоможе
EXPLAIN
MATCH (p:Person {name: "Alice"})
RETURN p

# 4.3. PROFILE: дивимося реальні числа
PROFILE
MATCH (p:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend:Person)
RETURN friend.name