from app.config.database import get_search_logs_collection
import datetime
from app.models.user_search_logs import UserSearchLogsModel
from dateutil import parser

async def update_user_search_logs(input_object, response):
    print("Logging User data", input_object)
    logged_date = datetime.datetime.now(datetime.timezone.utc)
    log_object: UserSearchLogsModel = {
        'query': input_object['query'],
        'response': response,
        'email': input_object['email'],
        'sent_at': parser.parse(input_object['sent_at']),
        "received_at": input_object['received_at'],
        "context": input_object['context'],
        'logged_at': logged_date,
        'language': input_object['language']
    }
    search_log_collection = get_search_logs_collection()
    search_log_collection.insert_one(log_object)
    print("Logged User search", log_object)