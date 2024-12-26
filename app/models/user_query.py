from pydantic import BaseModel, Field


class UserModel(BaseModel):
    email: str = Field(...)
    name: str = Field(...)
