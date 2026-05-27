import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
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


def urgency_class(due_date: str) -> str:
    try:
        due = datetime.strptime(due_date, "%m-%d-%Y").date()
        days = (due - datetime.now().date()).days
        if days < 0:
            return "overdue"
        if days <= 3:
            return "urgent"
        if days <= 7:
            return "soon"
    except ValueError:
        pass
    return ""


app.jinja_env.globals["urgency_class"] = urgency_class


def sort_key(a: Assignment) -> str:
    parts = a["due_date"].split("-")
    return f"{parts[2]}-{parts[0]}-{parts[1]}"


@app.route("/")
def index() -> str:
    status_filter = request.args.get("filter", "all")
    filtered = [
        a for a in assignments
        if status_filter == "all"
        or (status_filter == "incomplete" and a["status"] in ("incomplete", "in progress"))
        or (status_filter not in ("all", "incomplete") and a["status"] == status_filter)
    ]
    sorted_assignments = sorted(filtered, key=sort_key)
    return render_template("index.html", assignments=sorted_assignments, current_filter=status_filter)


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
            try:
                parsed = datetime.strptime(due_date, "%m-%d-%Y")
                if parsed.year < datetime.now().year:
                    errors["due_date"] = f"Year must be {datetime.now().year} or later."
            except ValueError:
                errors["due_date"] = "That's not a real date. Please enter a valid MM-DD-YYYY date."
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


@app.route("/assignments/<int:assignment_id>/toggle", methods=["POST"])
def toggle_assignment(assignment_id: int) -> str:
    for assignment in assignments:
        if assignment["id"] == assignment_id:
            cycle = {"incomplete": "in progress", "in progress": "complete", "complete": "incomplete"}
            assignment["status"] = cycle[assignment["status"]]
            return redirect(url_for("index"))
    abort(404)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
