from pymongo import MongoClient

# Connect to MongoDB running locally
client = MongoClient("mongodb+srv://suryaraghav8102_db_user:Surya1122@project01.fxbwuoh.mongodb.net/?retryWrites=true&w=majority&appName=Project01")

# Access or create the database
db = client["pharmacy"]

# Access or create the medicines collection
medicine_collection = db["medicines"]

# Access or create the sales collection
sales_collection = db["sales"]
