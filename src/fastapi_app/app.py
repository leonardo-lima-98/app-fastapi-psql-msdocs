import logging
import os
import pathlib
import time
from datetime import datetime

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from sqlmodel import Session, select

from fastapi_app.models import Restaurant, Review, engine




# Setup FastAPI app:
app = FastAPI()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


# @app.middleware("http")
# async def set_root_path_middleware(request: Request, call_next):
#     path = request.url.path
#     base_prefix = path.split("/")[1]  # pega o primeiro segmento após "/"
#     request.scope["root_path"] = f"/{base_prefix}"
#     response = await call_next(request)
#     return response


# Dependency to get the database session
def get_db_session():
    with Session(engine) as session:
        yield session




from fastapi_app.handlers.errors import not_found_handler
from fastapi_app.routes.bingo import route as bingo_route
from fastapi_app.routes.glances import route as glances_route
from fastapi_app.routes.login import route as login_route
from fastapi_app.routes.main import route as main_route
from fastapi_app.routes.users import route as users_route
from fastapi_app.routes.restaurant import route as restaurant_route

app.include_router(main_route, tags=['Main'])

app.include_router(bingo_route, prefix='/bingo', tags=['Bingo'])
app.include_router(glances_route, prefix='/glances', tags=['Glances'])
app.include_router(login_route, prefix='/login', tags=['Login'])
app.include_router(users_route, prefix='/users', tags=['Users'])
app.include_router(restaurant_route, prefix='/restaurant', tags=['Restaurant'])


app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
