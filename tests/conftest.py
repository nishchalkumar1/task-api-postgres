"""
Shared pytest fixtures for the Task API test suite.

Uses an in-memory SQLite database so tests run without a live PostgreSQL
instance or Docker.  The app's real get_session dependency is overridden
for every test via FastAPI's dependency_overrides mechanism.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app

# ---------------------------------------------------------------------------
# Engine — shared across the whole test session (StaticPool keeps one
# connection alive so the in-memory DB isn't destroyed between requests)
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite://"  # in-memory


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """Yield a fresh SQLite session (with schema) for each test function."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client", scope="function")
def client_fixture(session: Session):
    """Return a TestClient that injects the test session."""

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
