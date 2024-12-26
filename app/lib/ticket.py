from app.config.database import get_ticket_collection
from app.helpers.response_helpers import ticket_helper
ticket_collection = get_ticket_collection()

async def add_ticket(ticket_data: dict) -> dict:
    ticket = await ticket_collection.insert_one(ticket_data)
    new_ticket = await ticket_collection.find_one({"_id": ticket.inserted_id})
    return ticket_helper(new_ticket)