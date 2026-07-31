import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/tasks")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:  # type: ignore[return]
    """Yield a SQLModel session. Used by FastAPI dependency injection."""
    with Session(engine) as session:
        yield session
