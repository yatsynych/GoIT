#Preloading HBase image
docker pull harisekhon/hbase:latest

# Launching and first commands in HBase Shell
docker-compose up -d
docker-compose ps

# Access HBase Shell
http://localhost:16010

# Access HBase Shell
docker exec -it hbase hbase shell

# First commands in HBase Shell
version # Check HBase version
status # Check HBase cluster status
status 'simple' # Check HBase cluster status in simple format
status 'detailed' # Check HBase cluster status in detailed format
status 'summary' # Check HBase cluster status in summary format
status 'compact' # Check HBase cluster status in compact format
status 'json' # Check HBase cluster status in JSON format
status 'xml' # Check HBase cluster status in XML format
status 'yaml' # Check HBase cluster status in YAML format
status 'csv' # Check HBase cluster status in CSV format
status 'tsv' # Check HBase cluster status in TSV format
status 'html' # Check HBase cluster status in HTML format
status 'markdown' # Check HBase cluster status in Markdown format

# Create a table named 'orders' with column families 'info', 'items', and 'status'
create 'orders', 'info', 'items', 'status'



#########################################################################################################
### Check if the table 'orders' exists, list all tables, and describe the structure of the 'orders' table
#########################################################################################################

# List all tables
list

# Describe the structure of the 'orders' table
describe 'orders'

# Check if the table 'orders' exists
exists 'orders'



##############################################
### Insert sample data into the 'orders' table
##############################################

# Order 001: Classic development
put 'orders', 'order_001', 'info:customer_id', 'user_it_01'
put 'orders', 'order_001', 'info:total', '2450'
put 'orders', 'order_001', 'info:created_at', '2026-05-10'
put 'orders', 'order_001', 'items:book_1', 'Clean Code (Robert Martin)'
put 'orders', 'order_001', 'items:book_2', 'The Pragmatic Programmer'
put 'orders', 'order_001', 'status:current', 'delivered'

# Order 002: Computer Science and Algorithms
put 'orders', 'order_002', 'info:customer_id', 'user_it_02'
put 'orders', 'order_002', 'info:total', '1800'
put 'orders', 'order_002', 'info:created_at', '2026-05-11'
put 'orders', 'order_002', 'items:book_1', 'Introduction to Algorithms (CLRS)'
put 'orders', 'order_002', 'status:current', 'shipped'

# Order 003: High Load and Architecture
put 'orders', 'order_003', 'info:customer_id', 'user_it_01'
put 'orders', 'order_003', 'info:total', '1200'
put 'orders', 'order_003', 'info:created_at', '2026-05-12'
put 'orders', 'order_003', 'items:book_1', 'Designing Data-Intensive Applications (Martin Kleppmann)'
put 'orders', 'order_003', 'status:current', 'processing'

# Order 004: Python та Data Science
put 'orders', 'order_004', 'info:customer_id', 'user_it_03'
put 'orders', 'order_004', 'info:total', '3100'
put 'orders', 'order_004', 'info:created_at', '2026-05-13'
put 'orders', 'order_004', 'items:book_1', 'Fluent Python (Luciano Ramalho)'
put 'orders', 'order_004', 'items:book_2', 'Hands-On Machine Learning (Aurelien Geron)'
put 'orders', 'order_004', 'items:book_3', 'Deep Learning (Ian Goodfellow)'
put 'orders', 'order_004', 'status:current', 'new'

# Order 005: DevOps and Clouds
put 'orders', 'order_005', 'info:customer_id', 'user_it_04'
put 'orders', 'order_005', 'info:total', '950'
put 'orders', 'order_005', 'info:created_at', '2026-05-13'
put 'orders', 'order_005', 'items:book_1', 'Phoenix Project'
put 'orders', 'order_005', 'items:book_2', 'Site Reliability Engineering (Google)'
put 'orders', 'order_005', 'status:current', 'new'



########################################
### Reading data from the 'orders' table
########################################

# Read the entire row
get 'orders', 'order_001'

# Read a single column
get 'orders', 'order_001', 'info:total'

# Read multiple columns
get 'orders', 'order_001', {COLUMNS => ['info:customer_id', 'status:current']}

# Scan the entire table
scan 'orders'

# Scan with a limit
scan 'orders', {LIMIT => 2}

# Only certain columns
scan 'orders', {COLUMNS => 'info:total'}

###########
### Removal
###########

# Delete one column
delete 'orders', 'order_003', 'status:current'

# Check
get 'orders', 'order_003'

# Delete the entire row
deleteall 'orders', 'order_003'

# Check
scan 'orders'

