# 1. Start the MongoDB replica set using docker-compose
docker-compose up -d

# 2. Verify that all containers are running and healthy
docker ps

# 3. Enter the Mongosh shell on the first node (initial Primary candidate)
docker exec -it mongo1 mongosh

# 4. Initialize the replica set configuration
# This defines the members and their network addresses
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})

# 5. Check the replica set status 
# Wait a few seconds until one node transitions to "PRIMARY"
rs.status()

# 6. Insert a test document into the primary node
db.test.insertOne({ id: 1, status: "original" })

# 7. Open a new terminal session and connect to a secondary node (mongo2)
docker exec -it mongo2 mongosh

# 8. Enable reading from secondary members for this session
db.getMongo().setReadPref("secondary")

# 9. Verify that the data has been replicated to the secondary node
db.test.find({ id: 1 })

# 10. Simulate a Primary node failure by stopping the mongo1 container
docker stop mongo1

# 11. Connect to one of the remaining nodes to observe the election process
docker exec -it mongo2 mongosh

# 12. Check the status to see which node was elected as the new PRIMARY
rs.status()

# 13. Simulate a total Quorum loss by stopping another node
# With 2 out of 3 nodes down, the remaining node cannot stay PRIMARY
docker stop mongo3

# 14. Attempt to insert data with 'majority' write concern
# This will fail/timeout because the cluster no longer has a majority of healthy nodes
db.test.insertOne(
  { item: "critical_data" },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)

# 15. Recover the environment by starting all containers
docker-compose up -d

# 16. Final check to ensure the replica set has recovered and elected a leader
docker exec -it mongo1 mongosh
rs.status()