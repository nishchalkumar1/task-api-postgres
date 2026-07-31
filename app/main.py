from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup (fallback when Alembic isn't used)."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Task API — PostgreSQL",
    description="Production-quality FastAPI CRUD API backed by PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["root"])
def root() -> dict:
    """Root endpoint — confirms the API is live."""
    return {"message": "Task API is running.", "docs": "/docs"}


@app.get("/health", tags=["root"])
def health() -> dict:
    """Health-check endpoint."""
    return {"status": "ok"}
