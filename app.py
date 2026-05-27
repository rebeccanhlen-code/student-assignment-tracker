from flask import Flask, render_template, request, redirect, url_for
from typing import TypedDict

app = Flask(__name__)


class Assignment(TypedDict):
    id: int
    title: str
    due_date: str   # MM-DD-YYYY
    subject: str
    status: str     # "incomplete" or "complete"
    notes: str
    links: list[str]


assignments: list[Assignment] = [
    {
        "id": 1,
        "title": "Math Homework Chapter 5",
        "due_date": "05-28-2026",
        "subject": "Math",
        "status": "incomplete",
        "notes": "Review sections 5.1 through 5.3",
        "links": [],
    }
]

next_id: int = 2


@app.route("/")
def index() -> str:
    return render_template("index.html", assignments=assignments)


@app.route("/assignments/new", methods=["GET", "POST"])
def new_assignment() -> str:
    global next_id
    if request.method == "POST":
        link = request.form.get("links", "").strip()
        assignments.append({
            "id": next_id,
            "title": request.form.get("title", "").strip(),
            "due_date": request.form.get("due_date", "").strip(),
            "subject": request.form.get("subject", "").strip(),
            "status": "incomplete",
            "notes": request.form.get("notes", "").strip(),
            "links": [link] if link else [],
        })
        next_id += 1
        return redirect(url_for("index"))
    return render_template("new.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
