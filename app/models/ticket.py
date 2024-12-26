from pydantic import BaseModel, Field


class TicketModel(BaseModel):
    title: str = Field(...)
    details: str = Field(...)
    contact: str = Field(...)