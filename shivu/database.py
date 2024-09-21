from pymongo import MongoClient, WriteConcern

# Replace with your actual connection string
connection_string = "mongodb://myUser:myPassword@localhost:27017/mydb"
client = MongoClient(connection_string)

# Specify your database
db = client.mydb  # Change 'mydb' to your database name

# Access collections
user_collection = db.user_collection.with_options(write_concern=WriteConcern(w=1))
collection = db.collection_name  # Add other collections as needed