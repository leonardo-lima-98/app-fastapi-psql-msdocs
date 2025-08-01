
from fastapi_app.models import engine
from sqlmodel import Session


# Dependency to get the database session
def get_db_session():
    with Session(engine) as session:
        yield session