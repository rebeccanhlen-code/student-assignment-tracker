# Build Log — Student Assignment Tracker

Capstone project for Code2College Applied AI Cohort (Summer 2026 pilot).
Each entry follows the M5/M7 routine: brief → plan → confirm → implement → verify.

---

<!-- Entries go below, newest at the bottom -->
## Task 1 — Scaffold the repo and write the CLAUDE.md
- Brief: Create the capstone repo and a CLAUDE.md that documents the project, tech stack, commands, and conventions for Claude Code.
- What Claude proposed: A CLAUDE.md covering what the project is, the Python/Flask/Jinja2 stack, run/test commands, and a list of conventions and things Claude should not do.
- What I changed before approving: Reviewed and merged in home directory conventions; confirmed the project description matched the capstone brief.
- Verification: `git log --oneline` shows CLAUDE.md committed on main.
- One thing I learned: CLAUDE.md acts like standing instructions, whatever you write there shapes how Claude behaves in every future conversation in this repo.

## Task 2 — Define the assignment data structure
- Brief: Create the assignment data model with all required fields and a hardcoded test entry that prints from app.assignments.
- What Claude proposed: A `TypedDict` called `Assignment` with fields id, title, due_date (MM-DD-YYYY), subject, status, notes, links. Module-level `assignments` list with one hardcoded entry and a `next_id` counter.
- What I changed before approving: Changed due_date format from YYYY-MM-DD to MM-DD-YYYY as it is what I am used to.
- Verification: `python -c "from app import assignments; print(assignments)"` prints the hardcoded entry. `pytest` passes 6 tests.
- One thing I learned: Claude ensures that you don't make it automate everything, it also helps you practice coding so that you are not always relaying on it.

## Task 3 — Build the homepage to display assignments
- Brief: Render the assignments list in the browser with all fields visible using a Jinja2 template.
- What Claude proposed: A `templates/index.html` that loops over assignments with Jinja2, updated `/` route to call `render_template`.
- What I changed before approving: —
- Verification: Started `python app.py`, opened http://localhost:5000, saw Math Homework assignment with all fields displayed.
- One thing I learned: ...

## Task 4 — Add a new assignment form
- Brief: Build a form to add new assignments that redirects to the homepage on submit, with each new entry getting a unique id.
- What Claude proposed: A `templates/new.html` form with POST to `/assignments/new`, a new route that appends to the assignments list and increments `next_id`, and a link on the homepage.
- What I changed before approving: —
- Verification: Submitted the form with a new assignment, was redirected to homepage, new assignment appeared in the list. `pytest` passes 9 tests.
- One thing I learned: ...

