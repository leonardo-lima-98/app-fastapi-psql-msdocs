
import os
import pathlib

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_app.middleware.auth import AuthMiddleware

from fastapi_app.handlers.errors import not_found_handler, unauthorized_handler, internal_error_handler
from fastapi_app.routes.bingo import route as bingo_route
from fastapi_app.routes.glances import route as glances_route
from fastapi_app.routes.auth import route as auth_route
from fastapi_app.routes.main import route as main_route
from fastapi_app.routes.users import route as users_route
from fastapi_app.routes.restaurant import route as restaurant_route


# Setup FastAPI app:
app = FastAPI()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


# app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


app.add_middleware(AuthMiddleware)

app.include_router(main_route, tags=['Main'])

app.include_router(bingo_route, prefix='/bingo', tags=['Bingo'])
app.include_router(glances_route, prefix='/glances', tags=['Glances'])
app.include_router(auth_route, prefix='/auth', tags=['Auth'])
app.include_router(users_route, prefix='/users', tags=['Users'])
app.include_router(restaurant_route, prefix='/restaurant', tags=['Restaurant'])


app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_handler)
app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, unauthorized_handler)
# app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, internal_error_handler)
