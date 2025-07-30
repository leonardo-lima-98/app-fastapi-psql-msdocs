from enum import Enum

from pydantic import BaseModel, EmailStr


class JobTitles(str, Enum):
    owner = 'owner'
    manager = 'manager'
    developer = 'developer'
    operation = 'operation'


class Message(BaseModel):
    message: str
    status_code: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    job_title: str


class UserCreate(BaseModel):
    name: str
    password: str
    job_title: JobTitles


class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    job_title: str
    password: str
