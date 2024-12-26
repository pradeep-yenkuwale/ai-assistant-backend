from fastapi.responses import JSONResponse
from dateutil import parser


def response_helper(data, code, message):
    data = {
        "result": data,
        "status": code,
        "message": message
    }
    return JSONResponse(status_code=code, content=data)

def ticket_helper(ticket):
    return {
        "id": str(ticket['_id']),
        "title": ticket['title'],
        "details": ticket['details'],
        "contact": ticket['contact']
    }

def user_helper(user):
    return {
        "id": str(user['_id']),
        "email": user['name'],
        "name": user['email'],
    }

def search_log_helper(log_data):
    final_log_data = []
    for log in log_data:
        log_item = {
            "id": str(log['_id']),
            "query": log['query'],
            "response":  log['response'],
            "email":  log['email'],
            "sent_at": str(log['sent_at']),
            "received_at": str(log['received_at']),
            "logged_at": str(log['logged_at'])
        }
        final_log_data.append(log_item)
    return final_log_data


