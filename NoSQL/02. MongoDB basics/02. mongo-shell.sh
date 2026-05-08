# Copy these commands to install MongoDB in Docker and connect via Mongo Shell

### 3. Mongo Shell Commands after connecting to MongoDB

# 3.1.Show all databases

# 3.1.1. Connect to MongoDB shell using the container name and credentials
docker exec -it mongodb mongosh
use admin
db.auth("admin", "secretpassword")
# Show all databases (should show "admin" and "local" at least)
show dbs

# 3.1.2.Or Simply
docker exec -it mongodb mongosh "mongodb://admin:secretpassword@localhost:27017/admin"
# Show all databases (should show "admin" and "local" at least)
show dbs

# 3.2. Switch to database (created automatically on first entry)
use learningdb

# 3.3. Show current database
db

# 3.4. Show collections in current database
show collections

# 3.5. Get help on commands
db.help()

# 3.6. Get help on collection methods
db.users.help()

# 3.7. Check MongoDB version
db.version()

###  4. Simple data operations
# 4.1 Insert a document into a collection (created automatically if it doesn't exist)
db.products.insertOne({
  name: "Wireless Mouse",
  category: "Electronics",
  price: 29.99,
  inStock: true
});

# 4.2. Find documents in a collection
db.products.find({ category: "Electronics" });

# 4.3. Count documents in a collection
db.products.countDocuments({ inStock: true });

# 4.4. Pretty print documents
db.products.find().pretty();