from http import HTTPStatus
import random
import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

route = APIRouter()
parent_path = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=parent_path / "templates")

numeros_ja_exibidos = []

def gera_numero_random():
    num = random.randint(1 , 90)
    return num

@route.get('/', name="bingo", response_class=HTMLResponse)
def bingo_to_play_with_friends(request: Request, status_code=HTTPStatus.OK):
    return templates.TemplateResponse(
    'bingo.html',
    {
        'request': request,
        'title': "Bingo",
        'message': numeros_ja_exibidos,
        'class': 'success',
        'status_code': 0,
    },
    status_code=status_code.value,
    )
    

@route.get('/novo_numero', name="novo_numero", response_class=HTMLResponse)
def novo_numero(request: Request, status_code=HTTPStatus.OK):
    num = gera_numero_random()
    [num != x for x in numeros_ja_exibidos]
    numeros_ja_exibidos.append(num)
    return templates.TemplateResponse(
    'bingo.html',
    {
        'request': request,
        'title': "Bingo",
        'message': numeros_ja_exibidos,
        'class': 'success',
        'status_code': num,
    },
    status_code=status_code.value,
    )


@route.get('/reset_game', name="reset_game", response_class=HTMLResponse)
def reset_game(request: Request, status_code=HTTPStatus.OK):
    numeros_ja_exibidos.clear()
    return templates.TemplateResponse(
    'bingo.html',
    {
        'request': request,
        'title': "Bingo",
        'message': numeros_ja_exibidos,
        'class': 'success',
        'status_code': 0,
    },
    status_code=status_code.value,
    )
