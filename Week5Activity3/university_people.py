"""A small OOP example based on a university people class hierarchy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class Person:
    """A person at the university."""

    person_id: int
    name: str


@dataclass
class Student(Person):
    """A university student."""

    student_id: int


@dataclass
class Staff(Person):
    """Base class for university employees."""

    staff_id: int
    tax_num: str


@dataclass
class General(Staff):
    """A general staff member paid at an hourly rate."""

    rate_of_pay: float

    def calculate_pay_rate(self) -> float:
        """Return the staff member's hourly pay rate."""
        return self.rate_of_pay


@dataclass
class Academic(Staff):
    """An academic staff member whose publications can be counted."""

    publications: Sequence[str] = field(default_factory=list)

    def calculate_publications(self) -> int:
        """Return the number of publications held by this academic."""
        return len(self.publications)


class Lecturer(Academic):
    """A named academic role used by the program requirements."""


def main() -> None:
    """Create example objects and display the requested calculations."""
    lecturer = Lecturer(
        person_id=1001,
        name="Dr Ada Lovelace",
        staff_id=501,
        tax_num="TX-12345",
        publications=(
            "Computing Machines",
            "Analytical Engine Notes",
            "Mathematics in Practice",
        ),
    )
    general_staff = General(
        person_id=1002,
        name="Sam Taylor",
        staff_id=502,
        tax_num="TX-67890",
        rate_of_pay=31.50,
    )

    print(f"Lecturer: {lecturer.name}")
    print(f"Number of publications: {lecturer.calculate_publications()}")
    print(f"General staff member: {general_staff.name}")
    print(f"Pay rate: ${general_staff.calculate_pay_rate():.2f} per hour")


if __name__ == "__main__":
    main()
