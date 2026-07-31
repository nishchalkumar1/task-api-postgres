# task-api-postgres

A production-quality **FastAPI CRUD API** backed by **PostgreSQL**, containerised with **Docker Compose**.  
Built for the FlyRank Backend AI Engineering assignment.

---

## Tech Stack

| Layer       | Technology               |
|-------------|--------------------------|
| Language    | Python 3.12              |
| Framework   | FastAPI                  |
| ORM         | SQLModel                 |
| Database    | PostgreSQL 16            |
| Driver      | psycopg v3 (binary)      |
| Migrations  | Alembic                  |
| Validation  | Pydantic v2              |
| Server      | Uvicorn                  |
| Containers  | Docker + Docker Compose  |
| Testing     | pytest + httpx           |

---

## Folder Structure

```
task-api-postgres/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application & lifespan
│   ├── database.py      # Engine, session factory
│   ├── models.py        # SQLModel ORM model (Task)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py          # DB helper functions
│   └── dependencies.py  # FastAPI dependencies (session, 404)
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Environment Variables

Copy `.env.example` to `.env` before running:

```bash
cp .env.example .env
```

| Variable            | Default                                                  | Description                  |
|---------------------|----------------------------------------------------------|------------------------------|
| `DATABASE_URL`      | `postgresql+psycopg://postgres:postgres@db:5432/tasks`   | Full SQLAlchemy DSN           |
| `POSTGRES_USER`     | `postgres`                                               | PostgreSQL superuser name     |
| `POSTGRES_PASSWORD` | `postgres`                                               | PostgreSQL password           |
| `POSTGRES_DB`       | `tasks`                                                  | Database name                 |

---

## Installation (local, without Docker)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Docker Setup

### Build & start all services

```bash
docker compose up --build
```

Docker Compose starts PostgreSQL first, waits for its healthcheck to pass, then starts the API.

### Stop all services

```bash
docker compose down
```

### Stop and remove volumes (wipes database)

```bash
docker compose down -v
```

---

## Alembic — Database Migrations

### Generate first migration (autogenerate from models)

```bash
# Inside the running api container
docker compose exec api alembic revision --autogenerate -m "create tasks table"
```

### Apply migrations

```bash
docker compose exec api alembic upgrade head
```

### Roll back one revision

```bash
docker compose exec api alembic downgrade -1
```

### View migration history

```bash
docker compose exec api alembic history --verbose
```

---

## API Endpoints

| Method | Path           | Description                     | Success Code |
|--------|----------------|---------------------------------|--------------|
| GET    | `/`            | Root — confirms API is running  | 200          |
| GET    | `/health`      | Health check                    | 200          |
| GET    | `/tasks`       | List all tasks                  | 200          |
| GET    | `/tasks/{id}`  | Get a single task               | 200          |
| POST   | `/tasks`       | Create a new task               | 201          |
| PUT    | `/tasks/{id}`  | Update an existing task         | 200          |
| DELETE | `/tasks/{id}`  | Delete a task                   | 204          |

---

## How to Run

```bash
# 1. Clone the repository
git clone <repo-url>
cd task-api-postgres

# 2. Copy environment file
cp .env.example .env

# 3. Start with Docker Compose
docker compose up --build

# 4. Apply migrations
docker compose exec api alembic upgrade head
```

---

## Swagger UI

Once running, open:

```
http://localhost:8000/docs
```

---

## Sample curl Commands

```bash
# Root
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# List all tasks
curl http://localhost:8000/tasks

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'

# Get task by id
curl http://localhost:8000/tasks/1

# Update task
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete task
curl -X DELETE http://localhost:8000/tasks/1
```

---

## Screenshots

> _Screenshots will be added in Stage 5._

---

## License

MIT
