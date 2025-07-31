from http import HTTPStatus
import pathlib

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

route = APIRouter()
parent_path = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=parent_path / "templates")

# Rotas principais
@route.get('/', name='read_root')
def read_root(request: Request, status_code=HTTPStatus.OK):
    return templates.TemplateResponse(
        'status_code_template.html',
        {
            'request': request,
            'title': status_code.phrase,
            'message': 'Hello, World!',
            'class': 'success',
            'status_code': status_code.value,
        },
        status_code=status_code.value,
    )


@route.get('/health', name='health_check')
def health_check(request: Request, status_code=HTTPStatus.OK):
    return templates.TemplateResponse(
        'status_code_template.html',
        {
            'request': request,
            'title': status_code.phrase,
            'message': 'Health Check Success',
            'class': 'success',
            'status_code': status_code.value,
        },
        status_code=status_code.value,
    )
