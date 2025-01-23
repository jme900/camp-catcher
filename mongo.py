import os
from pymongo import MongoClient

mongodb_connection_string = os.environ.get('MONGODB_CAMPCATCHER_CONN')


def get_db():
    if mongodb_connection_string is None:
        raise ValueError("MongoDB connection string not found in environment variables.")

    # Connect to MongoDB
    client = MongoClient(mongodb_connection_string)

    return client['campcatcher']
