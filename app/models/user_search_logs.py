from pydantic import BaseModel, Field

class UserSearchLogsModel(BaseModel):
    email: str = Field(...)
    query: str = Field(...)
    context: str = Field('general')
    language: str = Field(...)
    response: str = Field(...)
    logged_at: str = Field(...)
    recieved_at: str = Field(...)
    sent_at: str = Field(...)
