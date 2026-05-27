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
- What I changed before approving: Noticed the app wasn't accessible in Codespaces — Claude had to add host="0.0.0.0" to app.run() to fix it. I caught this by trying to open the app and getting a 502 error.
- Verification: Started `python app.py`, opened http://localhost:5000, saw Math Homework assignment with all fields displayed.
- One thing I learned: ...

## Task 4 — Add a new assignment form
- Brief: Build a form to add new assignments that redirects to the homepage on submit, with each new entry getting a unique id.
- What Claude proposed: A `templates/new.html` form with POST to `/assignments/new`, a new route that appends to the assignments list and increments `next_id`, and a link on the homepage.
- What I changed before approving: Wrote my own test (test_redirection) that failed because the route didn't exist and caught that the test was testing the wrong endpoint and fixed it to test the actual POST redirect instead.
- Verification: Submitted the form with a new assignment, was redirected to homepage, new assignment appeared in the list. `pytest` passes 9 tests.
- One thing I learned: ...

## Task 5 — Add form validation
- Brief: Submitting empty fields should show inline error messages without crashing the app.
- What Claude proposed: Check title, due_date, subject in the POST handler; re-render the form with error messages and preserved values if any are blank.
- What I changed before approving: Requested that only numbers be accepted in the date field and that past years be rejected.
- Verification: Submitted the form empty, saw red error messages. Filled in just the title, saw it preserved after the error. `pytest` passes 13 tests.
- One thing I learned: ...

## Task 6 — Sort assignments by due date
- Brief: Assignments should always display sorted by due date, earliest first, regardless of the order they were added.
- What Claude proposed: A `sort_key` helper that converts MM-DD-YYYY to YYYY-MM-DD so Python's string sort works correctly, applied in the index route. Also added auto-dash JS so users just type 8 digits and the dashes appear automatically. Added real date validation so impossible dates like April 42 are rejected.
- What I changed before approving: Requested auto-insert dashes so users don't have to type them. Also asked to validate that the date is a real calendar date.
- Verification: Added two assignments out of order, confirmed the earlier due date appeared first. Typed 05282026 in the date field and it became 05-28-2026 automatically. Tried 04-42-2026 and got an error. `pytest` passes 15 tests.
- One thing I learned: ...

## Task 7 — Mark assignments as complete or incomplete
- Brief: Each assignment needs a button that cycles its status using the assignment id in the route (not list index).
- What Claude proposed: A POST route `/assignments/<id>/toggle` that finds the assignment by id, cycles the status, and redirects. Returns 404 if id not found. Toggle button added inline on the homepage.
- What I changed before approving: Added an "in progress" status so the cycle is incomplete → in progress → complete → incomplete.
- Verification: Clicked through all three statuses on an assignment, page reloaded showing each change correctly. `pytest` passes 17 tests.
- One thing I learned: ...

## Task 8 — Visual priority indicator
- Brief: Assignments due soon should show a visual warning — red for due today or tomorrow, orange for within 3 days.
- What Claude proposed: An `urgency_class` helper that computes days until due and returns "urgent" or "soon", registered as a Jinja2 global, with CSS border styles on each assignment card.
- What I changed before approving: Added a separate "overdue" style (crimson with pink background) for past-due assignments, and widened the thresholds — red within 3 days, orange within 7 days instead of the original 1 and 3.
- Verification: Added a test assignment due tomorrow, confirmed a red left border appeared. Added a past-due assignment, confirmed crimson styling. Far-future assignments had no styling. `pytest` passes 21 tests.
- One thing I learned: ...

## Task 9 — Filtering by status
- Brief: Users should be able to filter assignments by status so incomplete tasks don't get buried under completed ones.
- What Claude proposed: A `?filter=` query param on the index route with All / Incomplete / In Progress / Complete filter links on the homepage.
- What I changed before approving: —
- Verification: Clicked "Incomplete", confirmed complete assignments were hidden. Clicked "All", confirmed everything reappeared. `pytest` passes 23 tests.
- One thing I learned: ...
