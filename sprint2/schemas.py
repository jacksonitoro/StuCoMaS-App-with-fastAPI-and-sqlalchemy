from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
