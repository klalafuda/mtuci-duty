from sqlmodel import create_engine, Session

from src.config import postgres_config

engine = create_engine(postgres_config.postgres_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
