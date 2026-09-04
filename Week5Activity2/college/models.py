"""Domain models for the University Management System.

These dataclasses mirror the entities from the ER / UML class diagram:
Student, Enrollment, Subject, Lecturer and Lecture.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Student:
    """A person enrolled at the college."""

    student_code: str
    first_name: str
    last_name: str
    national_id: str
    birth_date: date
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"[{self.id}] {self.student_code} - {self.full_name} (NID {self.national_id})"


@dataclass
class Enrollment:
    """A course a student can enrol in."""

    course_name: str
    course_code: str
    start_date: date
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"[{self.id}] {self.course_code} - {self.course_name} (starts {self.start_date})"


@dataclass
class Subject:
    """An academic subject taught in lectures."""

    subject_code: str
    unit: str
    description: str
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"[{self.id}] {self.subject_code} - {self.unit}"


@dataclass
class Lecturer:
    """An academic staff member who delivers lectures."""

    first_name: str
    last_name: str
    email: str
    address: str
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"[{self.id}] {self.full_name} <{self.email}>"


@dataclass
class Lecture:
    """A scheduled teaching session linking an enrollment, lecturer and subject."""

    lecture_name: str
    start_time: datetime
    enrollment_id: int
    lecturer_id: int
    subject_id: int
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"[{self.id}] {self.lecture_name} @ {self.start_time}"
