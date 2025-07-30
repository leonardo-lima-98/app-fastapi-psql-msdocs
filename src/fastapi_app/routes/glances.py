from http import HTTPStatus, client

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

route = APIRouter()
templates = Jinja2Templates(directory='templates')


# Rota para o Glances
def check_server_up(host: str, port: int) -> bool:
    try:
        conn = client.HTTPConnection(host, port, timeout=2)
        conn.request('GET', '/')
        response = conn.getresponse()
        return response.status == HTTPStatus.OK
    except Exception:
        return False


@route.get('/', name='show_glances', response_class=HTMLResponse)
def show_glances(
    request: Request,
    host: str = Query(default='localhost'),
    port: int = Query(default=80),
):
    # if port == None: port = 80
    glances_url = f'http://{host}:{port}'

    if check_server_up(host, port):
        return templates.TemplateResponse(
            'glances.html',
            {'request': request, 'glances_url': glances_url, 'status_code': HTTPStatus.OK},
            status_code=HTTPStatus.OK,
        )
    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return templates.TemplateResponse(
            'status_code_template.html',
            {
                'request': request,
                'title': status_code.phrase,
                'message': f'Não foi possível acessar {glances_url}',
                'class': 'failed',
                'status_code': status_code.value,
            },
            status_code=status_code.value,
        )

