from app import assignments
import re

import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_assignments_is_not_empty() -> None:
    assert len(assignments) > 0


def test_assignment_has_required_fields() -> None:
    required = {"id", "title", "due_date", "subject", "status", "notes", "links"}
    for assignment in assignments:
        assert required.issubset(assignment.keys())


def test_assignment_id_is_unique() -> None:
    ids = [a["id"] for a in assignments]
    assert len(ids) == len(set(ids))


def test_assignment_status_is_valid() -> None:
    for assignment in assignments:
        assert assignment["status"] in ("incomplete", "in progress", "complete")


def test_due_date_format() -> None:
    for assignment in assignments:
        assert re.match(r"^\d{2}-\d{2}-\d{4}$", assignment["due_date"])


def test_title_is_not_empty() -> None:
    for assignment in assignments:
        assert assignment["title"] != ""


def test_homepage_sorted_by_due_date(client) -> None:
    from app import assignments
    assignments.clear()
    assignments.extend([
        {"id": 10, "title": "Late", "due_date": "12-01-2026", "subject": "Math", "status": "incomplete", "notes": "", "links": []},
        {"id": 11, "title": "Early", "due_date": "06-01-2026", "subject": "Math", "status": "incomplete", "notes": "", "links": []},
    ])
    response = client.get("/")
    body = response.data.decode()
    assert body.index("Early") < body.index("Late")
    assignments.clear()
    assignments.append({"id": 1, "title": "Math Homework Chapter 5", "due_date": "05-28-2026", "subject": "Math", "status": "incomplete", "notes": "Review sections 5.1 through 5.3", "links": []})


def test_toggle_cycles_status(client) -> None:
    from app import assignments
    assignments[0]["status"] = "incomplete"
    client.post("/assignments/1/toggle")
    assert assignments[0]["status"] == "in progress"
    client.post("/assignments/1/toggle")
    assert assignments[0]["status"] == "complete"
    client.post("/assignments/1/toggle")
    assert assignments[0]["status"] == "incomplete"


def test_toggle_unknown_id_returns_404(client) -> None:
    response = client.post("/assignments/9999/toggle")
    assert response.status_code == 404


def test_delete_removes_assignment(client) -> None:
    from app import assignments
    assignments.append({"id": 99, "title": "To Delete", "due_date": "12-01-2026", "subject": "Math", "status": "incomplete", "notes": "", "links": []})
    response = client.post("/assignments/99/delete")
    assert response.status_code == 302
    assert not any(a["id"] == 99 for a in assignments)


def test_delete_unknown_id_returns_404(client) -> None:
    response = client.post("/assignments/9999/delete")
    assert response.status_code == 404


def test_filter_incomplete_hides_complete(client) -> None:
    from app import assignments
    assignments.clear()
    assignments.extend([
        {"id": 10, "title": "Done Task", "due_date": "12-01-2026", "subject": "Math", "status": "complete", "notes": "", "links": []},
        {"id": 11, "title": "Todo Task", "due_date": "12-02-2026", "subject": "Math", "status": "incomplete", "notes": "", "links": []},
        {"id": 12, "title": "Wip Task", "due_date": "12-03-2026", "subject": "Math", "status": "in progress", "notes": "", "links": []},
    ])
    response = client.get("/?filter=incomplete")
    body = response.data.decode()
    assert "Todo Task" in body
    assert "Wip Task" in body
    assert "Done Task" not in body
    assignments.clear()
    assignments.append({"id": 1, "title": "Math Homework Chapter 5", "due_date": "05-28-2026", "subject": "Math", "status": "incomplete", "notes": "Review sections 5.1 through 5.3", "links": []})


def test_filter_all_shows_everything(client) -> None:
    response = client.get("/?filter=all")
    assert response.status_code == 200


def test_urgency_class_overdue() -> None:
    from datetime import date, timedelta
    from app import urgency_class
    yesterday = (date.today() - timedelta(days=1)).strftime("%m-%d-%Y")
    assert urgency_class(yesterday) == "overdue"


def test_urgency_class_due_tomorrow() -> None:
    from datetime import date, timedelta
    from app import urgency_class
    tomorrow = (date.today() + timedelta(days=1)).strftime("%m-%d-%Y")
    assert urgency_class(tomorrow) == "urgent"


def test_urgency_class_due_in_5_days() -> None:
    from datetime import date, timedelta
    from app import urgency_class
    five_days = (date.today() + timedelta(days=5)).strftime("%m-%d-%Y")
    assert urgency_class(five_days) == "soon"


def test_urgency_class_far_future() -> None:
    from app import urgency_class
    assert urgency_class("01-01-2099") == ""


def test_homepage_returns_200(client) -> None:
    response = client.get("/")
    assert response.status_code == 200

def test_homepage_shows_assignment_title(client) -> None:
    response = client.get("/")
    assert b"Math Homework Chapter 5" in response.data


def test_empty_form_shows_errors(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "", "due_date": "", "subject": "", "notes": "", "links": ""
    })
    assert response.status_code == 200
    assert b"required" in response.data


def test_invalid_date_format_shows_error(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "Test", "due_date": "not-a-date", "subject": "Math", "notes": "", "links": ""
    })
    assert response.status_code == 200
    assert b"MM-DD-YYYY" in response.data


def test_impossible_date_shows_error(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "Test", "due_date": "04-42-2026", "subject": "Math", "notes": "", "links": ""
    })
    assert response.status_code == 200
    assert b"real date" in response.data


def test_past_year_shows_error(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "Test", "due_date": "05-28-2020", "subject": "Math", "notes": "", "links": ""
    })
    assert response.status_code == 200
    assert b"or later" in response.data


def test_partial_form_preserves_filled_values(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "My Assignment", "due_date": "", "subject": "", "notes": "", "links": ""
    })
    assert response.status_code == 200
    assert b"My Assignment" in response.data


def test_new_assignment_redirects_to_homepage(client) -> None:
    response = client.post("/assignments/new", data={
        "title": "Test Assignment",
        "due_date": "06-01-2026",
        "subject": "Science",
        "notes": "",
        "links": "",
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    
