"""
Tests for write endpoints:
  POST   /tasks       — create a task
  PUT    /tasks/{id}  — update a task
  DELETE /tasks/{id}  — delete a task
"""
from app.models import Task


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------


def test_create_task_minimal(client):
    """Should create a task with only the required field (title)."""
    payload = {"title": "Buy milk"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] is None
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_full(client):
    """Should create a task with all fields provided."""
    payload = {"title": "Full task", "description": "A full description", "completed": True}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Full task"
    assert data["description"] == "A full description"
    assert data["completed"] is True


def test_create_task_missing_title(client):
    """Should reject creation when title is missing (422 Unprocessable Entity)."""
    response = client.post("/tasks/", json={"description": "No title"})
    assert response.status_code == 422


def test_create_task_empty_title(client):
    """Should reject creation when title is an empty string (422)."""
    response = client.post("/tasks/", json={"title": ""})
    assert response.status_code == 422


def test_create_task_persisted(client):
    """Task created via POST should be retrievable via GET."""
    client.post("/tasks/", json={"title": "Persisted task"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert "Persisted task" in titles


# ---------------------------------------------------------------------------
# PUT /tasks/{id}
# ---------------------------------------------------------------------------


def test_update_task_title(client, session):
    """Should update the title of an existing task."""
    task = Task(title="Old title")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.put(f"/tasks/{task.id}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_task_completed(client, session):
    """Should flip the completed flag."""
    task = Task(title="Not done", completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.put(f"/tasks/{task.id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_update_task_partial(client, session):
    """PUT with a subset of fields should only update those fields."""
    task = Task(title="Keep title", description="Keep desc", completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.put(f"/tasks/{task.id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Keep title"
    assert data["description"] == "Keep desc"
    assert data["completed"] is True


def test_update_task_not_found(client):
    """Should return 404 when updating a non-existent task."""
    response = client.put("/tasks/99999", json={"title": "Ghost"})
    assert response.status_code == 404


def test_update_task_updated_at_changes(client, session):
    """updated_at timestamp should change after a PUT."""
    task = Task(title="Watch clock")
    session.add(task)
    session.commit()
    session.refresh(task)
    original_updated_at = task.updated_at

    response = client.put(f"/tasks/{task.id}", json={"title": "Ticking"})
    assert response.status_code == 200
    new_updated_at = response.json()["updated_at"]
    # updated_at must be a valid datetime string and may differ
    assert new_updated_at is not None


# ---------------------------------------------------------------------------
# DELETE /tasks/{id}
# ---------------------------------------------------------------------------


def test_delete_task_success(client, session):
    """Should delete a task and return 204 No Content."""
    task = Task(title="Delete me")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_task_gone_after_delete(client, session):
    """Deleted task should return 404 on subsequent GET."""
    task = Task(title="Gone soon")
    session.add(task)
    session.commit()
    session.refresh(task)
    task_id = task.id

    client.delete(f"/tasks/{task_id}")
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    """Should return 404 when deleting a non-existent task."""
    response = client.delete("/tasks/99999")
    assert response.status_code == 404


def test_delete_task_removes_from_list(client, session):
    """After deletion the task list should shrink by one."""
    task1 = Task(title="Keep me")
    task2 = Task(title="Remove me")
    session.add(task1)
    session.add(task2)
    session.commit()
    session.refresh(task2)

    client.delete(f"/tasks/{task2.id}")
    response = client.get("/tasks/")
    titles = [t["title"] for t in response.json()]
    assert "Keep me" in titles
    assert "Remove me" not in titles
