# Week 5 Activity 2 --- College Management CLI (W5-A1 OOP project)

## Assignment

> Based on the designed ER and UML diagrams, develop the OOP project for
> **W5-A1 (College project)** as a CLI.

This folder turns the **University Management System** modelled in
[`Week5Activity1`](../Week5Activity1) (ER diagram, activity diagram, use
case diagram and UML class diagram) into a working, menu-driven Python
command line application backed by a **MySQL** database running in
**Docker**. The database access style follows
[`Week3Activity4`](../Week3Activity4): a `docker-compose` stack with
MySQL + Flyway migrations, accessed with `mysql-connector-python`.

The original OOP class-hierarchy exercise, `university_people.py`
(`Person -> Student / Staff -> General / Academic -> Lecturer`), is kept
in this folder as well.

---

## Domain model

The entities and relationships come straight from the UML class diagram:

| Entity | Key attributes | Operations |
| --- | --- | --- |
| `Student` | `student_code`, `first_name`, `last_name`, `national_id`, `birth_date` | create / update / delete / list |
| `Enrollment` | `course_name`, `course_code`, `start_date` | create / update / delete / list |
| `Subject` | `subject_code`, `unit`, `description` | create / update / delete / list |
| `Lecturer` | `first_name`, `last_name`, `email`, `address` | create / update / delete / list |
| `Lecture` | `lecture_name`, `start_time`, + FKs to enrollment, lecturer, subject | create / update / delete / list |

Relationships:

- **Student `>--<` Enrollment** --- many-to-many through the
  `student_enrollment` link table (a student can enrol in several
  courses; a course has many students).
- **Lecture `>--` Enrollment / Lecturer / Subject** --- each lecture
  belongs to one enrollment, is delivered by one lecturer and covers one
  subject.

```text
student ──< student_enrollment >── enrollment ──< lecture >── subject
                                                      │
                                                      └──> lecturer
```

---

## Architecture

The code is layered so the CLI never touches SQL directly:

```text
main.py
  └── college/
        config.py        DatabaseConfig (env / .env)
        db.py            Database  – connection + query/execute helpers (context manager)
        models.py        Student, Enrollment, Subject, Lecturer, Lecture  (dataclasses)
        repositories.py  BaseRepository + one repository per table (create/update/delete/list)
        seed.py          optional sample-data loader (uses faker if installed)
        cli.py           CollegeCLI – the interactive menu tree
```

- **`Database`** wraps a single `mysql.connector` connection, is used as
  a context manager, and exposes `query` / `query_one` / `execute` /
  `execute_many`.
- **Repositories** map rows to model objects and own every SQL string.
  `BaseRepository` provides `list_all`, `find`, `exists` and `delete`;
  each subclass adds `create` / `update` plus any reporting queries.
- **`CollegeCLI`** builds the menu tree, validates input, and catches
  `mysql.connector.Error` so a bad value (e.g. a duplicate code) prints a
  message instead of crashing.

---

## Setup

From this folder:

```bash
# 1. Start MySQL and apply the schema migrations
docker compose up -d

# 2. Install the Python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run the CLI
python3 main.py
```

`docker compose up -d` starts MySQL on `127.0.0.1:3306`
(`college` / `college` / db `college`) and runs the Flyway migrations in
[`migrations/`](migrations). Connection settings can be overridden with a
`.env` file --- see [`.env.example`](.env.example).

Stop and wipe everything with `docker compose down -v`.

---

## Using the CLI

```text
=== Main menu ===
  1. Manage students
  2. Manage enrollments
  3. Manage subjects
  4. Manage lecturers
  5. Manage lectures
  6. Manage student enrollments (links)
  7. Reports
  8. Load sample data
  0. Back
```

Each management screen offers **list / add / update / delete**. Update
pre-fills the current value --- press Enter to keep it. "Load sample
data" inserts a small related dataset (students, courses, lecturers,
lectures and enrolments) so the reports have something to show.

**Reports:**

- Students per enrollment
- Students enrolled in 2 or more courses
- Lecture schedule (lectures joined with course, subject and lecturer)

---

## `university_people.py` (OOP hierarchy exercise)

```text
Person
├── Student
└── Staff
    ├── General      -> calculate_pay_rate()
    └── Academic     -> calculate_publications()
        └── Lecturer
```

```bash
python3 university_people.py
```
