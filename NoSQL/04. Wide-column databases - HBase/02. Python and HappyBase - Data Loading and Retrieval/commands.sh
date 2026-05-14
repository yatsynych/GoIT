# Start the HBase and Python HBase client containers
docker-compose up -d --build

# Load the movies data into HBase using the load_movies.py script
docker exec -it python_hbase_client python 01_load_movies.py

# Read the movies data from HBase using the read_movies.py script
docker exec -it python_hbase_client python 02_read_movies.py

# Read the movies data with extended information from HBase using the read_movies_ext.py script
docker exec -it python_hbase_client python 03_read_movies_ext.py

# Compare batch writing vs regular writing in HBase using the batch_vs_regular_writing.py script
docker exec -it python_hbase_client python 04_batch_vs_regular_writing.py