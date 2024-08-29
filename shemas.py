from typing import Union
from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: Union[str, None] = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    first_name: int
    last_name: int
    notes: list[Note] = []

    class Config:
        from_attributes = True
