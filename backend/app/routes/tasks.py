from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_connection

router = APIRouter()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "todo"
    user_id: Optional[int] = None
    priority: int = 1

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

@router.get("/")
def get_all_tasks():
    """
    Get all tasks - Anti-pattern: SELECT * and no LIMIT
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Anti-pattern: gci74-python-dont-use-the-query-select-star-from
    # Should specify columns instead of using *
    cursor.execute("SELECT * FROM tasks")

    # Anti-pattern: No LIMIT clause - returns all results
    tasks = cursor.fetchall()
    conn.close()

    return {"tasks": tasks, "count": len(tasks)}

@router.get("/by-users")
def get_tasks_by_users(user_ids: str):
    """
    Get tasks for multiple users - Anti-pattern: SQL in loop
    """
    conn = get_connection()
    cursor = conn.cursor()

    user_id_list = [int(uid) for uid in user_ids.split(",")]
    results = []

    # Anti-pattern: gci72-python-avoid-sql-request-in-loop
    # Should use IN clause instead of querying in a loop
    for user_id in user_id_list:
        cursor.execute(f"SELECT * FROM tasks WHERE user_id = {user_id}")
        user_tasks = cursor.fetchall()
        results.extend(user_tasks)

    conn.close()
    return {"tasks": results}

@router.get("/by-status")
def get_tasks_by_status(status: str):
    """
    Get tasks by status - Anti-pattern: SELECT *
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Anti-pattern: SELECT * again
    cursor.execute(f"SELECT * FROM tasks WHERE status = '{status}'")
    tasks = cursor.fetchall()

    conn.close()
    return {"tasks": tasks, "status": status}

@router.post("/")
def create_task(task: Task):
    """Create a new task"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, description, status, user_id, priority) VALUES (?, ?, ?, ?, ?)",
        (task.title, task.description, task.status, task.user_id, task.priority)
    )

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {"id": task_id, "message": "Task created successfully"}

@router.put("/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update a task - Anti-pattern: Multiple if-else statements
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Anti-pattern: gci2-python-avoid-multiple-if-else-statement
    # Should use match-case or a better approach
    if task_update.status == "todo":
        priority_modifier = 1
    elif task_update.status == "in_progress":
        priority_modifier = 2
    elif task_update.status == "done":
        priority_modifier = 0
    elif task_update.status == "blocked":
        priority_modifier = 3
    else:
        priority_modifier = 1

    update_fields = []
    values = []

    if task_update.title:
        update_fields.append("title = ?")
        values.append(task_update.title)
    if task_update.description:
        update_fields.append("description = ?")
        values.append(task_update.description)
    if task_update.status:
        update_fields.append("status = ?")
        values.append(task_update.status)
    if task_update.priority:
        update_fields.append("priority = ?")
        values.append(task_update.priority * priority_modifier)

    if not update_fields:
        return {"message": "No fields to update"}

    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    return {"message": "Task updated successfully"}

@router.delete("/{task_id}")
def delete_task(task_id: int):
    """Delete a task"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    conn.commit()
    conn.close()

    return {"message": "Task deleted successfully"}
