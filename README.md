# Student Assignment Tracker

A web app for students to manage their academic workload in one place. Track assignments by subject, due date, and status — so nothing falls through the cracks.

Built as a capstone project for the **Code2College Applied AI Cohort (Summer 2026 pilot)**.

---

## Features

- Add assignments with a title, due date, subject, notes, and an optional link
- Due dates auto-format as you type (no dashes needed)
- Assignments sorted by due date automatically
- Color-coded urgency — overdue, due soon, or on track at a glance
- Three-stage status: **Incomplete → In Progress → Complete**
- Filter by status (Incomplete also shows In Progress so nothing gets hidden)
- Delete assignments with a confirmation prompt
- Dark mode toggle that remembers your preference

---

## Tech Stack

- **Python 3.10+** with **Flask 3.x**
- **Jinja2** for server-rendered templates
- **Vanilla HTML/CSS** — no frontend frameworks
- **pytest** for testing

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/rebeccanhlen-code/student-assignment-tracker.git
cd student-assignment-tracker
```

### 2. Create and activate a virtual environment

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install flask pytest
```

### 4. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

> **GitHub Codespaces?** The app runs on `0.0.0.0` automatically. Go to the **Ports** tab, set port 5000 to **Public**, and open the forwarded URL.

---

## Running Tests

```bash
pytest
```

To run a single file:
```bash
pytest tests/test_assignments.py
```

---

## Project Structure

```
student-assignment-tracker/
├── app.py                  # Flask app, routes, data model
├── conftest.py             # pytest path setup
├── static/
│   └── style.css           # All styles (CSS variables at the top for easy theming)
├── templates/
│   ├── index.html          # Homepage — assignment list
│   └── new.html            # Add assignment form
├── tests/
│   └── test_assignments.py # 25 automated tests
├── BUILD_LOG.md            # Task-by-task build journal
└── CLAUDE.md               # AI assistant instructions
```

---

## Customizing the Theme

Open `static/style.css` and edit the variables at the very top:

```css
:root {
    --accent:  #1a56db;  /* main blue — change this to any color */
    --bg:      #f0f4f8;  /* page background */
    --surface: #ffffff;  /* card background */
    ...
}
```

Change `--accent` to `#7c3aed` for purple, `#059669` for green, etc.
