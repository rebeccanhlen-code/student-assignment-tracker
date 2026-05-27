from app import assignments
import re

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
        assert assignment["status"] in ("incomplete", "complete")


def test_due_date_format() -> None:
    for assignment in assignments:
        assert re.match(r"^\d{2}-\d{2}-\d{4}$", assignment["due_date"])


def test_title_is_not_empty() -> None:
    for assignment in assignments:
        assert assignment["title"] != ""
