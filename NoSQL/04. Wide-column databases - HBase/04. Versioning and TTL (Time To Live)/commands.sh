# Start the HBase and Python HBase client containers
docker-compose up -d --build

# History of changes through versions
docker exec -it python_hbase_client python 01_history_of_changes_through_versions.py

# Access HBase Shell
docker exec -it hbase hbase shell

# Shell commands:
list
scan 'versioned'
scan 'versioned', {VERSIONS => 5}
scan 'versioned', {VERSIONS => 6}

# Automatic deletion of outdated data using TTL
docker exec -it python_hbase_client python 02_automatic_deletion_of_outdated_data.py