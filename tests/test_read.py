"""
Tests for read endpoints:
  GET /            — root
  GET /health      — health check
  GET /tasks       — list all tasks
  GET /tasks/{id}  — get single task
"""
from app.models import Task


# ---------------------------------------------------------------------------
# Root & Health
# ---------------------------------------------------------------------------


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task API is running."
    assert "docs" in data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# GET /tasks
# ---------------------------------------------------------------------------


def test_list_tasks_empty(client):
    """Should return an empty list when no tasks exist."""
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_all(client, session):
    """Should return all tasks persisted in the DB."""
    task1 = Task(title="First task", description="desc 1", completed=False)
    task2 = Task(title="Second task", completed=True)
    session.add(task1)
    session.add(task2)
    session.commit()

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = {t["title"] for t in data}
    assert titles == {"First task", "Second task"}


def test_list_tasks_response_shape(client, session):
    """Each task in the list must have all required fields."""
    task = Task(title="Shape test", description="hello", completed=False)
    session.add(task)
    session.commit()

    response = client.get("/tasks/")
    assert response.status_code == 200
    item = response.json()[0]
    for field in ("id", "title", "description", "completed", "created_at", "updated_at"):
        assert field in item, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# GET /tasks/{id}
# ---------------------------------------------------------------------------


def test_get_task_success(client, session):
    """Should return the correct task when it exists."""
    task = Task(title="Fetch me", description="detail", completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Fetch me"
    assert data["description"] == "detail"
    assert data["completed"] is False


def test_get_task_not_found(client):
    """Should return 404 when the task id does not exist."""
    response = client.get("/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
