from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.schemas import Message, User, UserCreate, UserResponse

route = APIRouter()
templates = Jinja2Templates(directory='templates')


database = [
    User(
        id='e537577e-54b5-4ce7-8589-d6fc0fb5d79d',
        name='leonardo',
        email='leonardo@owner.com',
        password='owner123',
        job_title='owner',
    ),
    User(
        id='55fbe272-1143-45c5-9b71-f62a9296d430',
        name='admin',
        email='admin@manager.com',
        password='admin123',
        job_title='manager',
    ),
    User(
        id='dfd1591a-e706-4ab9-9726-5080be2a5d9a',
        name='user',
        email='user@developer.com',
        password='user123',
        job_title='developer',
    ),
    User(
        id='867ba3ee-366a-494c-a092-c67f59992150',
        name='operator',
        email='operator@operation.com',
        password='operator123',
        job_title='operation',
    ),
]


# Rotas de usuario
@route.get('/', response_model=list[UserResponse], status_code=HTTPStatus.OK)
def get_users():
    return database


@route.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate):
    user = User(
        id=f'{uuid4()}',
        name=user.name,
        email=f'{user.name}@{user.job_title}.com',
        job_title=user.job_title,
        password=user.password,
    )
    database.append(user)
    return user


@route.get('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user():
    print([item.model_dump() for item in database])
    return {'message': 'Users', 'status_code': HTTPStatus.OK}


@route.put('/{user_id}', response_model=Message, status_code=HTTPStatus.OK)
def update_user(user_id: str):
    return {'message': f'User {user_id} updated', 'status_code': HTTPStatus.OK}

