# Copy these commands to install MongoDB in Docker and connect via Mongo Shell

### 1. MongoDB Installation and Connection Commands

# 1.1. Run a MongoDB container (in background, with authentication and persistent storage)
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secretpassword \
  -v mongodb_data:/data/db \
  mongo:7.0

# 1.2. Connect to MongoDB shell inside the running container
docker exec -it mongodb mongosh -u admin -p secretpassword

# 1.3. Stop a running container
docker stop mongodb

# 1.4. Remove container (must be stopped first)
docker rm mongodb

# 1.5. Force stop and remove container 
docker rm -f mongodb



### 2. MongoDB Replica Set Setup and Testing Commands
### Need docker-compose.yml file with MongoDB configuration for server

# 2.1. Start all services defined in the docker-compose file (run in background)
docker-compose up -d

# 2.1. View logs of the "mongodb" service (follow mode, not status!)
docker-compose logs -f mongodb

# 2.2. Stop and remove containers and networks (volumes are kept)
docker-compose down

# 2.3. Stop and remove containers, networks, AND volumes (data will be deleted)
docker-compose down -v