# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

Student Assignment Tracker is a web application that enables students of any age to manage their academic workload in one place. Each assignment entry captures a title, due date, subject, priority level, status (complete / incomplete), and optional notes or external links. It is purpose-built as a student-owned alternative to general-purpose productivity tools like Notion, with the goal of making assignment tracking more efficient and accessible for students worldwide. This project is the capstone for the Code2College Applied AI Cohort (Summer 2026 pilot).

## Tech stack

Python 3.10+ with Flask 3.x for the backend, Jinja2 for server-rendered templates, and vanilla HTML/CSS for the frontend — chosen for simplicity and low setup friction so the focus stays on building features, not configuring tooling. pytest handles testing. Persistence approach (in-memory vs. file/database) is TBD as the project grows.

## Commands

```bash
# Activate venv (PowerShell)
.venv\Scripts\activate

# Run the app
python app.py          # → http://localhost:5000

# Run all tests
pytest

# Run a single test file
pytest tests/test_assignments.py
```

## Conventions Claude should follow

- Use type hints on all function signatures.
- Prefer small, focused functions — one responsibility per function.
- Avoid global state; pass data explicitly or via the app factory pattern.
- Read the relevant test file before writing any code.
- Propose a plan and get agreement before implementing anything non-trivial.
- Keep each PR scoped to one feature or fix; work on a branch per feature.
- Run the relevant tests after each change; run full `pytest` before committing.

## Things Claude should not do

- Add new dependencies without asking first.
- Add a database or persistence layer unless explicitly requested.
- Modify test files to make tests pass — fix the implementation instead.
- Refactor code unrelated to the current task.
- Push directly to `main` — always use a branch and open a PR.
