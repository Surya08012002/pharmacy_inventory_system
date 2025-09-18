from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://suryaraghav8102_db_user:Surya1123@project01.fxbwuoh.mongodb.net/?retryWrites=true&w=majority&appName=Project01")  # change if using Atlas
db = client["pharmacy"]

# Collections
medicine_collection = db["medicines"]
sales_collection = db["sales"]

