from pymongo import MongoClient, WriteConcern

# Replace with your actual connection string
connection_string = "mongodb+srv://Epic2:w85NP8dEHmQxA5s7@cluster0.tttvsf9.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

# Specify your database
db = "character_catcherr" # Change 'mydb' to your database name

# Access collections
user_collection = db.user_collection.with_options(write_concern=WriteConcern(w=1))
collection = db.collection_name  # Add other collections as needed