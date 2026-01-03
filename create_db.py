import sqlite3

conn = sqlite3.connect("todo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    due_date TEXT,
    priority TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()
