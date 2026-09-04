"""Optional sample-data loader.

Uses ``faker`` when it is installed (see ``requirements.txt``); otherwise
falls back to a small fixed dataset so the CLI still has something to show.
"""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta

from .models import Enrollment, Lecture, Lecturer, Student, Subject
from .repositories import Repositories

try:  # pragma: no cover - depends on optional dependency
    from faker import Faker

    _fake = Faker()
except Exception:  # noqa: BLE001 - faker is genuinely optional
    _fake = None


def _has_data(repos: Repositories) -> bool:
    return bool(repos.students.list_all() or repos.enrollments.list_all())


def load_sample_data(repos: Repositories, students: int = 8) -> str:
    """Insert a handful of related rows. Returns a short summary string."""

    if _has_data(repos):
        return "Sample data skipped: the database already contains records."

    subjects = [
        repos.subjects.create(Subject(code, unit, desc))
        for code, unit, desc in [
            ("SUB-MATH", "Mathematics", "Calculus, algebra and discrete maths."),
            ("SUB-CS", "Computer Science", "Programming, algorithms and databases."),
            ("SUB-PHY", "Physics", "Mechanics, thermodynamics and waves."),
        ]
    ]

    enrollments = [
        repos.enrollments.create(
            Enrollment(name, code, date.today() - timedelta(days=offset))
        )
        for name, code, offset in [
            ("BSc Computer Science", "ENR-CS", 30),
            ("BSc Physics", "ENR-PHY", 20),
            ("Foundation Year", "ENR-FND", 10),
        ]
    ]

    lecturers = []
    for i in range(3):
        if _fake is not None:
            first, last = _fake.first_name(), _fake.last_name()
            email = _fake.unique.email()
            address = _fake.address().replace("\n", ", ")
        else:
            first, last = f"Lecturer{i}", "Smith"
            email = f"lecturer{i}@college.edu"
            address = f"{i} Campus Road"
        lecturers.append(
            repos.lecturers.create(Lecturer(first, last, email, address))
        )

    created_students = []
    for i in range(students):
        if _fake is not None:
            first, last = _fake.first_name(), _fake.last_name()
            nid = _fake.unique.bothify("NID-#######")
            birth = _fake.date_of_birth(minimum_age=18, maximum_age=30)
        else:
            first, last = f"Student{i}", "Doe"
            nid = f"NID-{1000000 + i}"
            birth = date(2003, 1, 1) + timedelta(days=i)
        created_students.append(
            repos.students.create(
                Student(f"STU-{2024000 + i}", first, last, nid, birth)
            )
        )

    for student in created_students:
        for enrollment in random.sample(enrollments, random.randint(1, len(enrollments))):
            repos.student_enrollments.link(
                student.id, enrollment.id, date.today()
            )

    for i in range(6):
        repos.lectures.create(
            Lecture(
                lecture_name=f"Lecture {i + 1}",
                start_time=datetime.now() + timedelta(days=i, hours=1),
                enrollment_id=random.choice(enrollments).id,
                lecturer_id=random.choice(lecturers).id,
                subject_id=random.choice(subjects).id,
            )
        )

    source = "faker" if _fake is not None else "built-in fixtures"
    return (
        f"Sample data loaded via {source}: "
        f"{len(created_students)} students, {len(enrollments)} enrollments, "
        f"{len(lecturers)} lecturers, {len(subjects)} subjects, 6 lectures."
    )
