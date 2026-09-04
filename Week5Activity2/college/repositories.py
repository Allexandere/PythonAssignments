"""Repository (data-access) layer.

Each repository owns the SQL for one table and translates between rows
and the dataclasses in :mod:`college.models`. This keeps the CLI free of
SQL and mirrors the ``create() / update() / delete()`` operations shown
on every class in the UML diagram.
"""

from __future__ import annotations

from typing import Optional

from .db import Database
from .models import Enrollment, Lecture, Lecturer, Student, Subject


class BaseRepository:
    """Shared list / fetch / delete behaviour for a single table."""

    table: str = ""

    def __init__(self, db: Database) -> None:
        self.db = db

    def _to_model(self, row: dict):  # pragma: no cover - overridden
        raise NotImplementedError

    def list_all(self) -> list:
        rows = self.db.query(f"SELECT * FROM {self.table} ORDER BY id")
        return [self._to_model(row) for row in rows]

    def find(self, entity_id: int):
        row = self.db.query_one(
            f"SELECT * FROM {self.table} WHERE id = %s", (entity_id,)
        )
        return self._to_model(row) if row else None

    def exists(self, entity_id: int) -> bool:
        return (
            self.db.query_one(
                f"SELECT 1 FROM {self.table} WHERE id = %s", (entity_id,)
            )
            is not None
        )

    def delete(self, entity_id: int) -> int:
        return self.db.execute(
            f"DELETE FROM {self.table} WHERE id = %s", (entity_id,)
        )


class StudentRepository(BaseRepository):
    table = "student"

    def _to_model(self, row: dict) -> Student:
        return Student(
            id=row["id"],
            student_code=row["student_code"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            national_id=row["national_id"],
            birth_date=row["birth_date"],
            created_at=row.get("created_at"),
        )

    def create(self, student: Student) -> Student:
        student.id = self.db.execute(
            """
            INSERT INTO student
                (student_code, first_name, last_name, national_id, birth_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                student.student_code,
                student.first_name,
                student.last_name,
                student.national_id,
                student.birth_date,
            ),
        )
        return student

    def update(self, student: Student) -> Student:
        self.db.execute(
            """
            UPDATE student
            SET student_code = %s,
                first_name = %s,
                last_name = %s,
                national_id = %s,
                birth_date = %s
            WHERE id = %s
            """,
            (
                student.student_code,
                student.first_name,
                student.last_name,
                student.national_id,
                student.birth_date,
                student.id,
            ),
        )
        return student


class EnrollmentRepository(BaseRepository):
    table = "enrollment"

    def _to_model(self, row: dict) -> Enrollment:
        return Enrollment(
            id=row["id"],
            course_name=row["course_name"],
            course_code=row["course_code"],
            start_date=row["start_date"],
        )

    def create(self, enrollment: Enrollment) -> Enrollment:
        enrollment.id = self.db.execute(
            """
            INSERT INTO enrollment (course_name, course_code, start_date)
            VALUES (%s, %s, %s)
            """,
            (
                enrollment.course_name,
                enrollment.course_code,
                enrollment.start_date,
            ),
        )
        return enrollment

    def update(self, enrollment: Enrollment) -> Enrollment:
        self.db.execute(
            """
            UPDATE enrollment
            SET course_name = %s, course_code = %s, start_date = %s
            WHERE id = %s
            """,
            (
                enrollment.course_name,
                enrollment.course_code,
                enrollment.start_date,
                enrollment.id,
            ),
        )
        return enrollment


class SubjectRepository(BaseRepository):
    table = "subject"

    def _to_model(self, row: dict) -> Subject:
        return Subject(
            id=row["id"],
            subject_code=row["subject_code"],
            unit=row["unit"],
            description=row["description"],
        )

    def create(self, subject: Subject) -> Subject:
        subject.id = self.db.execute(
            """
            INSERT INTO subject (subject_code, unit, description)
            VALUES (%s, %s, %s)
            """,
            (subject.subject_code, subject.unit, subject.description),
        )
        return subject

    def update(self, subject: Subject) -> Subject:
        self.db.execute(
            """
            UPDATE subject
            SET subject_code = %s, unit = %s, description = %s
            WHERE id = %s
            """,
            (subject.subject_code, subject.unit, subject.description, subject.id),
        )
        return subject


class LecturerRepository(BaseRepository):
    table = "lecturer"

    def _to_model(self, row: dict) -> Lecturer:
        return Lecturer(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            address=row["address"],
        )

    def create(self, lecturer: Lecturer) -> Lecturer:
        lecturer.id = self.db.execute(
            """
            INSERT INTO lecturer (first_name, last_name, email, address)
            VALUES (%s, %s, %s, %s)
            """,
            (
                lecturer.first_name,
                lecturer.last_name,
                lecturer.email,
                lecturer.address,
            ),
        )
        return lecturer

    def update(self, lecturer: Lecturer) -> Lecturer:
        self.db.execute(
            """
            UPDATE lecturer
            SET first_name = %s, last_name = %s, email = %s, address = %s
            WHERE id = %s
            """,
            (
                lecturer.first_name,
                lecturer.last_name,
                lecturer.email,
                lecturer.address,
                lecturer.id,
            ),
        )
        return lecturer


class LectureRepository(BaseRepository):
    table = "lecture"

    def _to_model(self, row: dict) -> Lecture:
        return Lecture(
            id=row["id"],
            lecture_name=row["lecture_name"],
            start_time=row["start_time"],
            enrollment_id=row["enrollment_id"],
            lecturer_id=row["lecturer_id"],
            subject_id=row["subject_id"],
        )

    def create(self, lecture: Lecture) -> Lecture:
        lecture.id = self.db.execute(
            """
            INSERT INTO lecture
                (lecture_name, start_time, enrollment_id, lecturer_id, subject_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                lecture.lecture_name,
                lecture.start_time,
                lecture.enrollment_id,
                lecture.lecturer_id,
                lecture.subject_id,
            ),
        )
        return lecture

    def update(self, lecture: Lecture) -> Lecture:
        self.db.execute(
            """
            UPDATE lecture
            SET lecture_name = %s,
                start_time = %s,
                enrollment_id = %s,
                lecturer_id = %s,
                subject_id = %s
            WHERE id = %s
            """,
            (
                lecture.lecture_name,
                lecture.start_time,
                lecture.enrollment_id,
                lecture.lecturer_id,
                lecture.subject_id,
                lecture.id,
            ),
        )
        return lecture

    def list_detailed(self) -> list:
        """Lectures joined with enrollment / lecturer / subject names."""

        return self.db.query(
            """
            SELECT
                lecture.id,
                lecture.lecture_name,
                lecture.start_time,
                enrollment.course_name,
                subject.unit AS subject_unit,
                CONCAT(lecturer.first_name, ' ', lecturer.last_name) AS lecturer_name
            FROM lecture
            JOIN enrollment ON enrollment.id = lecture.enrollment_id
            JOIN lecturer ON lecturer.id = lecture.lecturer_id
            JOIN subject ON subject.id = lecture.subject_id
            ORDER BY lecture.start_time
            """
        )


class StudentEnrollmentRepository:
    """The ``student_enrollment`` link table plus reporting queries."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def link(self, student_id: int, enrollment_id: int, enrolled_on) -> None:
        self.db.execute(
            """
            INSERT INTO student_enrollment (student_id, enrollment_id, enrolled_on)
            VALUES (%s, %s, %s)
            """,
            (student_id, enrollment_id, enrolled_on),
        )

    def unlink(self, student_id: int, enrollment_id: int) -> int:
        return self.db.execute(
            """
            DELETE FROM student_enrollment
            WHERE student_id = %s AND enrollment_id = %s
            """,
            (student_id, enrollment_id),
        )

    def is_linked(self, student_id: int, enrollment_id: int) -> bool:
        return (
            self.db.query_one(
                """
                SELECT 1 FROM student_enrollment
                WHERE student_id = %s AND enrollment_id = %s
                """,
                (student_id, enrollment_id),
            )
            is not None
        )

    def enrollments_for_student(self, student_id: int) -> list:
        return self.db.query(
            """
            SELECT enrollment.id, enrollment.course_code, enrollment.course_name,
                   student_enrollment.enrolled_on
            FROM student_enrollment
            JOIN enrollment ON enrollment.id = student_enrollment.enrollment_id
            WHERE student_enrollment.student_id = %s
            ORDER BY enrollment.course_code
            """,
            (student_id,),
        )

    def student_count_by_enrollment(self) -> list:
        return self.db.query(
            """
            SELECT enrollment.id, enrollment.course_code, enrollment.course_name,
                   COUNT(student_enrollment.student_id) AS student_count
            FROM enrollment
            LEFT JOIN student_enrollment
                ON student_enrollment.enrollment_id = enrollment.id
            GROUP BY enrollment.id, enrollment.course_code, enrollment.course_name
            ORDER BY enrollment.course_code
            """
        )

    def students_with_multiple_enrollments(self) -> list:
        return self.db.query(
            """
            SELECT student.id, student.student_code,
                   CONCAT(student.first_name, ' ', student.last_name) AS full_name,
                   COUNT(student_enrollment.enrollment_id) AS enrollment_count
            FROM student
            JOIN student_enrollment
                ON student_enrollment.student_id = student.id
            GROUP BY student.id, student.student_code, full_name
            HAVING COUNT(student_enrollment.enrollment_id) >= 2
            ORDER BY enrollment_count DESC, full_name
            """
        )


class Repositories:
    """Convenience container wiring every repository to one connection."""

    def __init__(self, db: Database) -> None:
        self.db = db
        self.students = StudentRepository(db)
        self.enrollments = EnrollmentRepository(db)
        self.subjects = SubjectRepository(db)
        self.lecturers = LecturerRepository(db)
        self.lectures = LectureRepository(db)
        self.student_enrollments = StudentEnrollmentRepository(db)
