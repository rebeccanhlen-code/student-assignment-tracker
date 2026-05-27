from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run(debug=True)
