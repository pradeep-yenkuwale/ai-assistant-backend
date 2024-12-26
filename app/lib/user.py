from app.config.database import get_search_logs_collection, get_user_collection
from app.helpers.response_helpers import search_log_helper, user_helper
user_collection = get_user_collection()
user_search_logs_collection = get_search_logs_collection()

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def get_user(email: str) -> dict:
    print("email", email)
    user_data = await user_collection.find_one({"email": email})
    print("user_data", user_data)
    if(user_data==None):
        return user_data
    return user_helper(user_data)

async def get_search_logs(email: str) -> dict:
    user_logs = await user_search_logs_collection.find({"email": email}).to_list(length=None)
    # print("user_logs", user_logs)
    if(user_logs==None):
        return user_logs
    return search_log_helper(user_logs)