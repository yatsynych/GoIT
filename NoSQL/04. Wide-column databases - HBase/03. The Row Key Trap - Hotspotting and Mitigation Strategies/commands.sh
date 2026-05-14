# Start the HBase and Python HBase client containers
docker-compose up -d --build

# Create the table for server logs with two column families: 'log' for storing logs and 'meta' for storing metadata.
docker exec -it python_hbase_client python 01_creating_table_for_server_logs.py

# Now write data with a “bad” Row Key — timestamp at the beginning, which leads to hotspotting. In this example, we simulate logs from three servers, where keys are formed as "timestamp:server_id". This means that all new records will have larger keys than previous ones, leading to all records being written to one region, creating a hotspot when writing data.
docker exec -it python_hbase_client python 02_write_data_with_bad_row_key.py

# To mitigate hotspotting, we can use a technique called "salting". This involves adding a random prefix to the Row Key, which helps distribute the data more evenly across regions. In this example, we will modify the Row Key to include a random salt value at the beginning, followed by the timestamp and server ID. This way, new records will be distributed across different regions, reducing the chances of hotspotting.
docker exec -it python_hbase_client python 03_solution_salting.py

# Finally, we can read the logs of a specific server to verify that our salting strategy is working correctly. We will read the logs for a specific server ID and check that the data is distributed across different regions.
docker exec -it python_hbase_client python 04_reading_logs_of_specific_server.py

# Independent task
docker exec -it python_hbase_client python 05_independent_task.py