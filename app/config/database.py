import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST") or ""
DB_USERNAME = os.getenv("DB_USERNAME") or ""
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""
DB_NAME = os.getenv("DB_NAME") or ""
DB_PORT = os.getenv("DB_PORT") or ""

MONGO_URI = DB_HOST + ':' + DB_PORT + '/'+ DB_NAME
print("MONGO_URI yes", MONGO_URI)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

ticket_collection = database.get_collection("tickets")
user_search_logs_collection = database.get_collection("user_search_logs")
user_collection = database.get_collection("users")

def get_ticket_collection():
    return ticket_collection

def get_search_logs_collection():
    return user_search_logs_collection

def get_user_collection():
    return user_collection