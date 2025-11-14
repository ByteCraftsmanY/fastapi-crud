import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

# PostgreSQL Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://admin:admin123@localhost:5432/test"
)

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
