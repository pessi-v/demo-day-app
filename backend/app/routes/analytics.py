from fastapi import APIRouter
from app.database import get_connection
from app.services.report_service import ReportService

router = APIRouter()

@router.get("/stats")
def get_task_stats():
    """
    Get task statistics - Anti-pattern: Dictionary iteration
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    results = cursor.fetchall()

    stats = {}
    for row in results:
        stats[row[0]] = row[1]

    # Anti-pattern: gci103-python-dont-use-items-to-iterate-over-a-dictionary-when-only-keys-or-values-are-needed
    # We only need values here, but we're using items()
    total = 0
    for key, value in stats.items():
        total += value

    conn.close()

    return {
        "stats": stats,
        "total": total
    }

@router.get("/user-summary")
def get_user_summary():
    """
    Get summary per user - Anti-pattern: SQL in loop
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()

    summaries = []

    # Anti-pattern: gci72-python-avoid-sql-request-in-loop
    for user in users:
        user_id = user[0]
        user_name = user[1]

        cursor.execute(f"SELECT COUNT(*) FROM tasks WHERE user_id = {user_id}")
        task_count = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM tasks WHERE user_id = {user_id} AND status = 'done'")
        completed_count = cursor.fetchone()[0]

        summaries.append({
            "user_id": user_id,
            "name": user_name,
            "total_tasks": task_count,
            "completed_tasks": completed_count
        })

    conn.close()
    return {"summaries": summaries}

@router.get("/report")
def generate_report(format: str = "text"):
    """Generate a task report"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    report_service = ReportService()
    report = report_service.generate_report(tasks)

    return {"report": report, "format": format}

@router.get("/priority-distribution")
def get_priority_distribution():
    """
    Get task distribution by priority - Anti-pattern: Multiple if-else
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    results = cursor.fetchall()

    distribution = {}

    for row in results:
        priority = row[0]
        count = row[1]

        # Anti-pattern: gci2-python-avoid-multiple-if-else-statement
        if priority == 1:
            label = "Low"
        elif priority == 2:
            label = "Medium"
        elif priority == 3:
            label = "High"
        elif priority == 4:
            label = "Critical"
        else:
            label = "Unknown"

        distribution[label] = count

    conn.close()
    return {"distribution": distribution}
