from asyncio import exceptions
import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

# Configure the Cosmos DB client
COSMOS_DB_URI = os.getenv('COSMOS_ENDPOINT')
COSMOS_DB_KEY = os.getenv('COSMOS_KEY')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'NewsArticle')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'Items')

client = CosmosClient(COSMOS_DB_URI, COSMOS_DB_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)
# Read the record
def get_posts():
    query = 'SELECT * FROM c'
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

def get_post_by_id(post_id):
    query = f'SELECT * FROM c WHERE c.id="{post_id}"'
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items[0] if items else None

# Insert operation
def insert_post(post_data):
    try:
        container.create_item(body=post_data)
        print(f"Item inserted: {post_data['id']}")
    except exceptions.CosmosHttpResponseError as e:
        print(f"An error occurred: {e.message}")
