import re
from datetime import datetime
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
        title = request.form.get("title", "").strip()
        due_date = request.form.get("due_date", "").strip()
        subject = request.form.get("subject", "").strip()
        notes = request.form.get("notes", "").strip()
        link = request.form.get("links", "").strip()

        errors: dict[str, str] = {}
        if not title:
            errors["title"] = "Title is required."
        if not due_date:
            errors["due_date"] = "Due date is required."
        elif not re.match(r"^\d{2}-\d{2}-\d{4}$", due_date):
            errors["due_date"] = "Date must be in MM-DD-YYYY format (numbers only)."
        else:
            year = int(due_date.split("-")[2])
            if year < datetime.now().year:
                errors["due_date"] = f"Year must be {datetime.now().year} or later."
        if not subject:
            errors["subject"] = "Subject is required."

        if errors:
            return render_template("new.html", errors=errors, form=request.form)

        assignments.append({
            "id": next_id,
            "title": title,
            "due_date": due_date,
            "subject": subject,
            "status": "incomplete",
            "notes": notes,
            "links": [link] if link else [],
        })
        next_id += 1
        return redirect(url_for("index"))
    return render_template("new.html", errors={}, form={})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
