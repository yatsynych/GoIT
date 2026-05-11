# Demo in MongoDB Shell

# 1. Create docker container
# docker-compose.yml:

version: '3.8'

services:
  mongo1:
    image: mongo:7.0
    container_name: mongo1
    ports:
      - "27017:27017"
    command: mongod --replSet rs0 --bind_ip_all

  mongo2:
    image: mongo:7.0
    container_name: mongo2
    ports:
      - "27018:27017"
    command: mongod --replSet rs0 --bind_ip_all

  mongo3:
    image: mongo:7.0
    container_name: mongo3
    ports:
      - "27019:27017"
    command: mongod --replSet rs0 --bind_ip_all

# 2. Start the replica set
docker compose up -d

# 3. Connect to the primary node
docker exec -it mongo1 mongosh

# 4. Initialize the replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})

# 5. Check the status of the replica set
rs.status()

# 6. Create a database
use testdb

# 7. Create a collection and insert sample data
db.orders.insertMany([
  {
    customer: "Ivan",
    product: "Laptop",
    category: "Electronics",
    qty: 2,
    price: 1200
  },
  {
    customer: "Olena",
    product: "Laptop",
    category: "Electronics",
    qty: 1,
    price: 1200
  },
  {
    customer: "Petro",
    product: "Mouse",
    category: "Electronics",
    qty: 5,
    price: 25
  },
  {
    customer: "Anna",
    product: "Keyboard",
    category: "Electronics",
    qty: 3,
    price: 80
  },
  {
    customer: "Maksym",
    product: "Chair",
    category: "Furniture",
    qty: 2,
    price: 300
  },
  {
    customer: "Iryna",
    product: "Desk",
    category: "Furniture",
    qty: 1,
    price: 450
  },
  {
    customer: "Taras",
    product: "Chair",
    category: "Furniture",
    qty: 4,
    price: 300
  }
])

# 8. MapReduce

# 8.1 map()
var mapFunction = function () {
  emit(this.category, this.qty);
};

# 8.2 reduce()
var reduceFunction = function (key, values) {
  return Array.sum(values);
};

# 8.3 execute MapReduce
db.orders.mapReduce(
  mapFunction,
  reduceFunction,
  {
    out: "category_totals"
  }
)

# 8.4 view results
db.category_totals.find()

# Results:
# { _id: 'Electronics', value: 11 }
# { _id: 'Furniture', value: 7 }

# 9. Aggregation Pipeline

db.orders.aggregate([
  {
    $group: {
      _id: "$category",
      totalQty: { $sum: "$qty" }
    }
  },
  {
    $sort: {
      totalQty: -1
    }
  }
])

# Results:
# [
# { _id: 'Electronics', totalQty: 11 },
#   { _id: 'Furniture', totalQty: 7 }
# ]