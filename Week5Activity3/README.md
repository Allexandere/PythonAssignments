# Week 5 Activity 3: University People Hierarchy

This program implements the class hierarchy shown in the activity:

```text
Person
├── Student
└── Staff
    ├── General
    └── Academic
        └── Lecturer
```

`Lecturer` inherits from `Academic` and uses `calculate_publications()`
to count its publication records. `General` inherits from `Staff` and
uses `calculate_pay_rate()` to return its hourly rate.

Run the program from the repository root:

```bash
python3 Week5Activity3/university_people.py
```
