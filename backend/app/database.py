import sqlite3
import os

# Anti-pattern: Global variable (gci4-python-avoid-using-global-variables)
db_connection = None

def get_db_path():
    return os.path.join(os.path.dirname(__file__), "..", "tasks.db")

def init_db():
    """Initialize the database with sample data"""
    global db_connection
    db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'todo',
            user_id INTEGER,
            priority INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # Insert sample users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("Alice Johnson", "alice@example.com"),
            ("Bob Smith", "bob@example.com"),
            ("Carol Williams", "carol@example.com"),
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)

    # Insert sample tasks
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        tasks = [
            ("Complete project proposal", "Write and submit the Q1 proposal", "todo", 1, 3),
            ("Review pull requests", "Review pending PRs in the repository", "in_progress", 1, 2),
            ("Update documentation", "Update API documentation for new endpoints", "todo", 2, 1),
            ("Fix bug #123", "Resolve the login issue reported by users", "done", 2, 3),
            ("Deploy to staging", "Deploy latest changes to staging environment", "in_progress", 3, 2),
        ]
        cursor.executemany(
            "INSERT INTO tasks (title, description, status, user_id, priority) VALUES (?, ?, ?, ?, ?)",
            tasks
        )

    conn.commit()
    conn.close()
    db_connection = conn

def get_connection():
    """Get database connection"""
    return sqlite3.connect(get_db_path())
