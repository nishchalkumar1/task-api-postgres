from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Table creation is intentionally omitted here: in production, Alembic
    migrations (``alembic upgrade head``) are responsible for schema management.
    In tests, conftest.py calls SQLModel.metadata.create_all on the in-memory
    SQLite engine before each test function.
    """
    yield


app = FastAPI(
    title="Task API — PostgreSQL",
    description="Production-quality FastAPI CRUD API backed by PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Routes ────────────────────────────────────────────────────────────────────

app.include_router(tasks_router)


@app.get("/", tags=["root"])
def root() -> dict:
    """Root endpoint — confirms the API is live."""
    return {"message": "Task API is running.", "docs": "/docs"}


@app.get("/health", tags=["root"])
def health() -> dict:
    """Health-check endpoint."""
    return {"status": "ok"}
