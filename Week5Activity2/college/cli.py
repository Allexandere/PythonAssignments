"""Interactive, menu-driven command line interface.

The menu structure follows the Activity Diagram from ``Week5Activity1``:
the user chooses an area (students, enrollments, lectures, ...) and then a
create / update / delete / view action.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Callable, Optional

import mysql.connector

from .db import Database
from .models import Enrollment, Lecture, Lecturer, Student, Subject
from .repositories import Repositories
from .seed import load_sample_data

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class ExitCLI(Exception):
    """Raised internally to unwind out of every menu and quit."""


# --------------------------------------------------------------------------
# input helpers
# --------------------------------------------------------------------------
def _read(label: str) -> str:
    try:
        return input(label).strip()
    except EOFError as exc:  # Ctrl-D
        raise ExitCLI from exc


def prompt_text(label: str, default: Optional[str] = None, required: bool = True) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = _read(f"{label}{suffix}: ")
        if not value and default is not None:
            return default
        if value or not required:
            return value
        print("  ! A value is required.")


def prompt_int(
    label: str, default: Optional[int] = None, allow_blank: bool = False
) -> Optional[int]:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = _read(f"{label}{suffix}: ")
        if not value:
            if default is not None:
                return default
            if allow_blank:
                return None
        try:
            return int(value)
        except ValueError:
            print("  ! Please enter a whole number.")


def prompt_date(label: str, default: Optional[date] = None) -> date:
    default_str = default.strftime(DATE_FORMAT) if default else None
    suffix = f" [{default_str}]" if default_str else " (YYYY-MM-DD)"
    while True:
        value = _read(f"{label}{suffix}: ")
        if not value and default is not None:
            return default
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            print("  ! Use the format YYYY-MM-DD, e.g. 2026-09-05.")


def prompt_datetime(label: str, default: Optional[datetime] = None) -> datetime:
    default_str = default.strftime(DATETIME_FORMAT) if default else None
    suffix = f" [{default_str}]" if default_str else " (YYYY-MM-DD HH:MM)"
    while True:
        value = _read(f"{label}{suffix}: ")
        if not value and default is not None:
            return default
        try:
            return datetime.strptime(value, DATETIME_FORMAT)
        except ValueError:
            print("  ! Use the format YYYY-MM-DD HH:MM, e.g. 2026-09-05 14:30.")


def confirm(label: str) -> bool:
    return _read(f"{label} [y/N]: ").lower() in {"y", "yes"}


def pause() -> None:
    _read("\nPress Enter to continue... ")


class CollegeCLI:
    """Owns the repositories and renders the menu tree."""

    def __init__(self, db: Database) -> None:
        self.repos = Repositories(db)

    # -- generic menu runner --------------------------------------------
    def _menu(self, title: str, options: "list[tuple[str, Callable[[], None]]]") -> None:
        while True:
            print(f"\n=== {title} ===")
            for index, (label, _) in enumerate(options, start=1):
                print(f"  {index}. {label}")
            print("  0. Back")
            choice = _read("Select: ")
            if choice == "0":
                return
            try:
                _, action = options[int(choice) - 1]
            except (ValueError, IndexError):
                print("  ! Invalid choice.")
                continue
            try:
                action()
            except mysql.connector.Error as err:
                print(f"  ! Database error: {err.msg or err}")

    # -- top level -----------------------------------------------------
    def run(self) -> None:
        print("University Management System (W5-A1)")
        try:
            self._menu(
                "Main menu",
                [
                    ("Manage students", self.students_menu),
                    ("Manage enrollments", self.enrollments_menu),
                    ("Manage subjects", self.subjects_menu),
                    ("Manage lecturers", self.lecturers_menu),
                    ("Manage lectures", self.lectures_menu),
                    ("Manage student enrollments (links)", self.links_menu),
                    ("Reports", self.reports_menu),
                    ("Load sample data", self.load_sample_data),
                ],
            )
        except ExitCLI:
            pass
        print("\nGoodbye.")

    # -- students ----------------------------------------------------
    def students_menu(self) -> None:
        self._menu(
            "Students",
            [
                ("List students", self.list_students),
                ("Add student", self.add_student),
                ("Update student", self.update_student),
                ("Delete student", self.delete_student),
            ],
        )

    def list_students(self) -> None:
        rows = self.repos.students.list_all()
        _print_list(rows, "No students yet.")

    def add_student(self) -> None:
        student = Student(
            student_code=prompt_text("Student code"),
            first_name=prompt_text("First name"),
            last_name=prompt_text("Last name"),
            national_id=prompt_text("National ID"),
            birth_date=prompt_date("Birth date"),
        )
        self.repos.students.create(student)
        print(f"  + Created {student}")

    def update_student(self) -> None:
        student = self._pick(self.repos.students, "student")
        if not student:
            return
        student.student_code = prompt_text("Student code", student.student_code)
        student.first_name = prompt_text("First name", student.first_name)
        student.last_name = prompt_text("Last name", student.last_name)
        student.national_id = prompt_text("National ID", student.national_id)
        student.birth_date = prompt_date("Birth date", student.birth_date)
        self.repos.students.update(student)
        print(f"  * Updated {student}")

    def delete_student(self) -> None:
        self._delete_from(self.repos.students, "student")

    # -- enrollments -----------------------------------------------
    def enrollments_menu(self) -> None:
        self._menu(
            "Enrollments",
            [
                ("List enrollments", self.list_enrollments),
                ("Add enrollment", self.add_enrollment),
                ("Update enrollment", self.update_enrollment),
                ("Delete enrollment", self.delete_enrollment),
            ],
        )

    def list_enrollments(self) -> None:
        _print_list(self.repos.enrollments.list_all(), "No enrollments yet.")

    def add_enrollment(self) -> None:
        enrollment = Enrollment(
            course_name=prompt_text("Course name"),
            course_code=prompt_text("Course code"),
            start_date=prompt_date("Start date"),
        )
        self.repos.enrollments.create(enrollment)
        print(f"  + Created {enrollment}")

    def update_enrollment(self) -> None:
        enrollment = self._pick(self.repos.enrollments, "enrollment")
        if not enrollment:
            return
        enrollment.course_name = prompt_text("Course name", enrollment.course_name)
        enrollment.course_code = prompt_text("Course code", enrollment.course_code)
        enrollment.start_date = prompt_date("Start date", enrollment.start_date)
        self.repos.enrollments.update(enrollment)
        print(f"  * Updated {enrollment}")

    def delete_enrollment(self) -> None:
        self._delete_from(self.repos.enrollments, "enrollment")

    # -- subjects -------------------------------------------------
    def subjects_menu(self) -> None:
        self._menu(
            "Subjects",
            [
                ("List subjects", self.list_subjects),
                ("Add subject", self.add_subject),
                ("Update subject", self.update_subject),
                ("Delete subject", self.delete_subject),
            ],
        )

    def list_subjects(self) -> None:
        _print_list(self.repos.subjects.list_all(), "No subjects yet.")

    def add_subject(self) -> None:
        subject = Subject(
            subject_code=prompt_text("Subject code"),
            unit=prompt_text("Unit / name"),
            description=prompt_text("Description"),
        )
        self.repos.subjects.create(subject)
        print(f"  + Created {subject}")

    def update_subject(self) -> None:
        subject = self._pick(self.repos.subjects, "subject")
        if not subject:
            return
        subject.subject_code = prompt_text("Subject code", subject.subject_code)
        subject.unit = prompt_text("Unit / name", subject.unit)
        subject.description = prompt_text("Description", subject.description)
        self.repos.subjects.update(subject)
        print(f"  * Updated {subject}")

    def delete_subject(self) -> None:
        self._delete_from(self.repos.subjects, "subject")

    # -- lecturers -----------------------------------------------
    def lecturers_menu(self) -> None:
        self._menu(
            "Lecturers",
            [
                ("List lecturers", self.list_lecturers),
                ("Add lecturer", self.add_lecturer),
                ("Update lecturer", self.update_lecturer),
                ("Delete lecturer", self.delete_lecturer),
            ],
        )

    def list_lecturers(self) -> None:
        _print_list(self.repos.lecturers.list_all(), "No lecturers yet.")

    def add_lecturer(self) -> None:
        lecturer = Lecturer(
            first_name=prompt_text("First name"),
            last_name=prompt_text("Last name"),
            email=prompt_text("Email"),
            address=prompt_text("Address"),
        )
        self.repos.lecturers.create(lecturer)
        print(f"  + Created {lecturer}")

    def update_lecturer(self) -> None:
        lecturer = self._pick(self.repos.lecturers, "lecturer")
        if not lecturer:
            return
        lecturer.first_name = prompt_text("First name", lecturer.first_name)
        lecturer.last_name = prompt_text("Last name", lecturer.last_name)
        lecturer.email = prompt_text("Email", lecturer.email)
        lecturer.address = prompt_text("Address", lecturer.address)
        self.repos.lecturers.update(lecturer)
        print(f"  * Updated {lecturer}")

    def delete_lecturer(self) -> None:
        self._delete_from(self.repos.lecturers, "lecturer")

    # -- lectures ----------------------------------------------
    def lectures_menu(self) -> None:
        self._menu(
            "Lectures",
            [
                ("List lectures", self.list_lectures),
                ("Add lecture", self.add_lecture),
                ("Update lecture", self.update_lecture),
                ("Delete lecture", self.delete_lecture),
            ],
        )

    def list_lectures(self) -> None:
        rows = self.repos.lectures.list_detailed()
        if not rows:
            print("  No lectures yet.")
            return
        for row in rows:
            print(
                f"  [{row['id']}] {row['lecture_name']} | {row['start_time']} | "
                f"course: {row['course_name']} | subject: {row['subject_unit']} | "
                f"lecturer: {row['lecturer_name']}"
            )

    def add_lecture(self) -> None:
        if not self._require_supporting_rows():
            return
        print("\n-- enrollments --")
        self.list_enrollments()
        enrollment_id = self._pick_id(self.repos.enrollments, "enrollment")
        print("\n-- lecturers --")
        self.list_lecturers()
        lecturer_id = self._pick_id(self.repos.lecturers, "lecturer")
        print("\n-- subjects --")
        self.list_subjects()
        subject_id = self._pick_id(self.repos.subjects, "subject")
        if None in (enrollment_id, lecturer_id, subject_id):
            return
        lecture = Lecture(
            lecture_name=prompt_text("Lecture name"),
            start_time=prompt_datetime("Start time"),
            enrollment_id=enrollment_id,
            lecturer_id=lecturer_id,
            subject_id=subject_id,
        )
        self.repos.lectures.create(lecture)
        print(f"  + Created {lecture}")

    def update_lecture(self) -> None:
        lecture = self._pick(self.repos.lectures, "lecture")
        if not lecture:
            return
        lecture.lecture_name = prompt_text("Lecture name", lecture.lecture_name)
        lecture.start_time = prompt_datetime("Start time", lecture.start_time)
        lecture.enrollment_id = self._pick_id(
            self.repos.enrollments, "enrollment", lecture.enrollment_id
        )
        lecture.lecturer_id = self._pick_id(
            self.repos.lecturers, "lecturer", lecture.lecturer_id
        )
        lecture.subject_id = self._pick_id(
            self.repos.subjects, "subject", lecture.subject_id
        )
        self.repos.lectures.update(lecture)
        print(f"  * Updated {lecture}")

    def delete_lecture(self) -> None:
        self._delete_from(self.repos.lectures, "lecture")

    def _require_supporting_rows(self) -> bool:
        missing = []
        if not self.repos.enrollments.list_all():
            missing.append("enrollment")
        if not self.repos.lecturers.list_all():
            missing.append("lecturer")
        if not self.repos.subjects.list_all():
            missing.append("subject")
        if missing:
            print(f"  ! Add at least one {', '.join(missing)} first.")
            return False
        return True

    # -- student <-> enrollment links -------------------------
    def links_menu(self) -> None:
        self._menu(
            "Student enrollments",
            [
                ("Show a student's enrollments", self.show_student_links),
                ("Enrol a student in an enrollment", self.add_link),
                ("Remove a student from an enrollment", self.remove_link),
            ],
        )

    def show_student_links(self) -> None:
        student = self._pick(self.repos.students, "student")
        if not student:
            return
        rows = self.repos.student_enrollments.enrollments_for_student(student.id)
        if not rows:
            print(f"  {student.full_name} has no enrollments.")
            return
        for row in rows:
            print(
                f"  {row['course_code']} - {row['course_name']} "
                f"(since {row['enrolled_on']})"
            )

    def add_link(self) -> None:
        student = self._pick(self.repos.students, "student")
        if not student:
            return
        self.list_enrollments()
        enrollment = self._pick(self.repos.enrollments, "enrollment")
        if not enrollment:
            return
        if self.repos.student_enrollments.is_linked(student.id, enrollment.id):
            print("  ! That student is already enrolled here.")
            return
        self.repos.student_enrollments.link(student.id, enrollment.id, date.today())
        print(f"  + {student.full_name} enrolled in {enrollment.course_code}")

    def remove_link(self) -> None:
        student = self._pick(self.repos.students, "student")
        if not student:
            return
        rows = self.repos.student_enrollments.enrollments_for_student(student.id)
        if not rows:
            print(f"  {student.full_name} has no enrollments.")
            return
        for row in rows:
            print(f"  [{row['id']}] {row['course_code']} - {row['course_name']}")
        enrollment_id = prompt_int("Enrollment id to remove", allow_blank=True)
        if enrollment_id is None:
            return
        removed = self.repos.student_enrollments.unlink(student.id, enrollment_id)
        print("  * Removed." if removed else "  ! No such enrollment for this student.")

    # -- reports ---------------------------------------------
    def reports_menu(self) -> None:
        self._menu(
            "Reports",
            [
                ("Students per enrollment", self.report_students_per_enrollment),
                (
                    "Students with 2+ enrollments",
                    self.report_students_multiple_enrollments,
                ),
                ("Lecture schedule", self.list_lectures),
            ],
        )

    def report_students_per_enrollment(self) -> None:
        rows = self.repos.student_enrollments.student_count_by_enrollment()
        if not rows:
            print("  No enrollments yet.")
            return
        for row in rows:
            print(
                f"  {row['course_code']} - {row['course_name']}: "
                f"{row['student_count']} student(s)"
            )

    def report_students_multiple_enrollments(self) -> None:
        rows = self.repos.student_enrollments.students_with_multiple_enrollments()
        if not rows:
            print("  No student is enrolled in more than one course.")
            return
        for row in rows:
            print(
                f"  {row['student_code']} - {row['full_name']}: "
                f"{row['enrollment_count']} enrollments"
            )

    def load_sample_data(self) -> None:
        if not confirm("Insert sample students, courses and lectures?"):
            return
        print("  " + load_sample_data(self.repos))

    # -- shared selection helpers ---------------------------
    def _pick(self, repo, noun: str):
        entity_id = prompt_int(f"{noun.capitalize()} id", allow_blank=True)
        if entity_id is None:
            return None
        entity = repo.find(entity_id)
        if entity is None:
            print(f"  ! No {noun} with id {entity_id}.")
        return entity

    def _pick_id(self, repo, noun: str, default: Optional[int] = None) -> Optional[int]:
        while True:
            entity_id = prompt_int(f"{noun.capitalize()} id", default=default, allow_blank=True)
            if entity_id is None:
                return None
            if repo.exists(entity_id):
                return entity_id
            print(f"  ! No {noun} with id {entity_id}.")

    def _delete_from(self, repo, noun: str) -> None:
        entity = self._pick(repo, noun)
        if not entity:
            return
        if not confirm(f"Delete {noun} {entity.id}?"):
            return
        repo.delete(entity.id)
        print(f"  - Deleted {noun} {entity.id}.")


def _print_list(rows: list, empty_message: str) -> None:
    if not rows:
        print(f"  {empty_message}")
        return
    for row in rows:
        print(f"  {row}")
