#!/bin/bash

echo "========================================="
echo " MongoDB Demo: Replica Set + Aggregation "
echo "========================================="

echo ""
echo "[1/8] Starting MongoDB containers..."
docker compose up -d

sleep 10

echo ""
echo "[2/8] Initializing Replica Set..."

docker exec mongo1 mongosh --eval '
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 2 },
    { _id: 1, host: "mongo2:27017", priority: 1 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})
'

echo ""
echo "Waiting for PRIMARY election..."
sleep 40

echo ""
echo "[3/8] Replica Set Status"

docker exec mongo1 mongosh --eval '
rs.status().members.forEach(m =>
  print(m.name + " -> " + m.stateStr)
)
'

echo ""
echo "[4/8] Creating demo database and dataset..."

docker exec mongo1 mongosh --eval '

db = db.getSiblingDB("testdb")

db.orders.drop()
db.customers.drop()

db.customers.insertMany([
  {
    customerId: 1,
    name: "Ivan",
    city: "Lviv"
  },
  {
    customerId: 2,
    name: "Olena",
    city: "Kyiv"
  },
  {
    customerId: 3,
    name: "Petro",
    city: "Odesa"
  }
])

db.orders.insertMany([
  {
    customerId: 1,
    product: "Laptop",
    category: "Electronics",
    qty: 2,
    price: 1200
  },
  {
    customerId: 1,
    product: "Mouse",
    category: "Electronics",
    qty: 5,
    price: 25
  },
  {
    customerId: 2,
    product: "Chair",
    category: "Furniture",
    qty: 2,
    price: 300
  },
  {
    customerId: 2,
    product: "Desk",
    category: "Furniture",
    qty: 1,
    price: 450
  },
  {
    customerId: 3,
    product: "Keyboard",
    category: "Electronics",
    qty: 3,
    price: 80
  }
])

print("Dataset created.")
'

echo ""
echo "[5/8] MapReduce Demo"

docker exec mongo1 mongosh --eval '

db = db.getSiblingDB("testdb")

var mapFunction = function () {
  emit(this.category, this.qty);
};

var reduceFunction = function (key, values) {
  return Array.sum(values);
};

db.orders.mapReduce(
  mapFunction,
  reduceFunction,
  {
    out: "category_totals"
  }
)

print("MapReduce result:")
printjson(db.category_totals.find().toArray())
'

echo ""
echo "[6/8] Aggregation Demo: \$group + \$sort"

docker exec mongo1 mongosh --eval '

db = db.getSiblingDB("testdb")

print("Aggregation result:")

printjson(
  db.orders.aggregate([
    {
      $group: {
        _id: "$category",
        totalQty: { $sum: "$qty" },
        avgPrice: { $avg: "$price" }
      }
    },
    {
      $sort: {
        totalQty: -1
      }
    }
  ]).toArray()
)
'

echo ""
echo "[7/8] Aggregation Demo: \$match + \$project"

docker exec mongo1 mongosh --eval '

db = db.getSiblingDB("testdb")

print("Match + Project result:")

printjson(
  db.orders.aggregate([
    {
      $match: {
        category: "Electronics"
      }
    },
    {
      $project: {
        _id: 0,
        product: 1,
        totalPrice: {
          $multiply: ["$qty", "$price"]
        }
      }
    }
  ]).toArray()
)
'

echo ""
echo "[8/8] Aggregation Demo: \$lookup"

docker exec mongo1 mongosh --eval '

db = db.getSiblingDB("testdb")

print("Lookup result:")

printjson(
  db.orders.aggregate([
    {
      $lookup: {
        from: "customers",
        localField: "customerId",
        foreignField: "customerId",
        as: "customer"
      }
    },
    {
      $unwind: "$customer"
    },
    {
      $project: {
        _id: 0,
        product: 1,
        category: 1,
        qty: 1,
        customerName: "$customer.name",
        city: "$customer.city"
      }
    }
  ]).toArray()
)
'

echo ""
echo "========================================="
echo " Demo completed successfully!"
echo "========================================="
echo ""
echo "Connect manually:"
echo "docker exec -it mongo1 mongosh"
echo ""
echo "Useful commands:"
echo "use testdb"
echo "show collections"
echo "db.orders.find()"
echo "db.category_totals.find()"