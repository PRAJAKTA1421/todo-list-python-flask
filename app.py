from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("todo.db")

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        cur.execute("""
        INSERT INTO tasks (title, category, due_date, priority)
        VALUES (?, ?, ?, ?)
        """, (title, category, due_date, priority))

        conn.commit()
        return redirect("/")

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM tasks")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'")
    completed = cur.fetchone()[0]

    progress = int((completed / total) * 100) if total > 0 else 0

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        progress=progress
    )

@app.route("/complete/<int:id>")
def complete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status='Completed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
