from fastapi import APIRouter, Body, Query, Request
from fastapi.encoders import jsonable_encoder
from app.helpers.response_helpers import response_helper
from app.lib.ticket import add_ticket
from app.models.ticket import TicketModel

router = APIRouter()

@router.post('/ticket')
async def create_ticket(ticket: TicketModel = Body(...)):
    ticket = jsonable_encoder(ticket)
    new_ticket = await add_ticket(ticket)
    return response_helper(new_ticket, 200, "Ticket have been created successfully")
