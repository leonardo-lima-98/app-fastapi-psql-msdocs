from sqlmodel import Session


from fastapi_app.models import engine

# Dependency to get the database session
def get_db_session():
    with Session(engine) as session:
        yield session