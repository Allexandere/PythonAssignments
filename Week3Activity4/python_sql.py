import mysql.connector
import random
from faker import Faker

fake = Faker()


def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="app",
        password="app",
        database="app",
    )


def create_enrollments(conn, count):
    cursor = conn.cursor()

    query = """
        INSERT INTO enrollment (name, start_date, code)
        VALUES (%s, %s, %s)
    """

    enrollments = []

    for _ in range(count):
        enrollments.append(
            (
                fake.catch_phrase(),
                fake.date_time_between(
                    start_date="-1y",
                    end_date="now",
                ),
                fake.unique.bothify("ENR-####"),
            )
        )

    cursor.executemany(query, enrollments)
    conn.commit()

    cursor.execute(
        """
        SELECT id
        FROM enrollment
        ORDER BY id DESC
        LIMIT %s
    """,
        (count,),
    )

    enrollment_ids = [row[0] for row in cursor.fetchall()]

    enrollment_ids.reverse()

    cursor.close()

    return enrollment_ids


def create_lecturers(conn, count):
    cursor = conn.cursor()

    query = """
        INSERT INTO lecturer (
            first_name,
            last_name,
            email,
            address
        )
        VALUES (%s, %s, %s, %s)
    """

    lecturers = []

    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()

        lecturers.append(
            (
                first_name,
                last_name,
                fake.unique.email(),
                fake.address().replace("\n", ", "),
            )
        )

    cursor.executemany(query, lecturers)
    conn.commit()

    cursor.execute(
        """
        SELECT id
        FROM lecturer
        ORDER BY id DESC
        LIMIT %s
    """,
        (count,),
    )

    lecturer_ids = [row[0] for row in cursor.fetchall()]

    lecturer_ids.reverse()

    cursor.close()

    return lecturer_ids


def create_subjects(conn, count):
    cursor = conn.cursor()

    query = """
        INSERT INTO subject (
            unit,
            description
        )
        VALUES (%s, %s)
    """

    subjects = []

    for _ in range(count):
        subjects.append(
            (
                fake.catch_phrase(),
                fake.text(max_nb_chars=200),
            )
        )

    cursor.executemany(query, subjects)
    conn.commit()

    cursor.execute(
        """
        SELECT id
        FROM subject
        ORDER BY id DESC
        LIMIT %s
    """,
        (count,),
    )

    subject_ids = [row[0] for row in cursor.fetchall()]

    subject_ids.reverse()

    cursor.close()

    return subject_ids


def create_students(conn, count):
    cursor = conn.cursor()

    query = """
        INSERT INTO student (
            first_name,
            last_name,
            email
        )
        VALUES (%s, %s, %s)
    """

    students = []

    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()

        students.append(
            (
                first_name,
                last_name,
                fake.unique.email(),
            )
        )

    cursor.executemany(query, students)
    conn.commit()

    cursor.execute(
        """
        SELECT id
        FROM student
        ORDER BY id DESC
        LIMIT %s
        """,
        (count,),
    )

    student_ids = [row[0] for row in cursor.fetchall()]
    student_ids.reverse()

    cursor.close()

    return student_ids


def create_student_enrollments(conn, student_ids, enrollment_ids):
    cursor = conn.cursor()

    query = """
        INSERT INTO student_enrollment (student_id, enrollment_id)
        VALUES (%s, %s)
    """

    student_enrollments = []
    max_enrollments = min(3, len(enrollment_ids))

    for student_id in student_ids:
        enrollment_count = random.randint(1, max_enrollments)

        for enrollment_id in random.sample(enrollment_ids, enrollment_count):
            student_enrollments.append((student_id, enrollment_id))

    cursor.executemany(query, student_enrollments)
    conn.commit()

    cursor.close()


def create_lectures(
    conn,
    enrollment_ids,
    lecturer_ids,
    subject_ids,
    count
):
    cursor = conn.cursor()

    query = """
        INSERT INTO lecture (
            start_date,
            enrollment_id,
            lecturer_id,
            subject_id
        )
        VALUES (%s, %s, %s, %s)
    """

    lectures = []

    for _ in range(count):
        lectures.append(
            (
                fake.date_time_between(
                    start_date="-1m",
                    end_date="+1m",
                ),
                fake.random_element(enrollment_ids),
                fake.random_element(lecturer_ids),
                fake.random_element(subject_ids),
            )
        )

    cursor.executemany(query, lectures)
    conn.commit()

    cursor.close()


def find_student_count_by_enrollment(conn):
    cursor = conn.cursor()

    query = """
        SELECT
            enrollment.id,
            enrollment.name,
            COUNT(student.id) AS student_count
        FROM enrollment
        LEFT JOIN student_enrollment
            ON student_enrollment.enrollment_id = enrollment.id
        LEFT JOIN student ON student.id = student_enrollment.student_id
        GROUP BY enrollment.id, enrollment.name
        ORDER BY enrollment.name
    """

    cursor.execute(query)
    enrollments = cursor.fetchall()
    cursor.close()

    return enrollments


def find_students_with_multiple_enrollments(conn):
    cursor = conn.cursor()

    query = """
        SELECT
            student.id,
            student.first_name,
            student.last_name,
            COUNT(student_enrollment.enrollment_id) AS enrollment_count
        FROM student
        INNER JOIN student_enrollment
            ON student_enrollment.student_id = student.id
        GROUP BY student.id, student.first_name, student.last_name
        HAVING COUNT(student_enrollment.enrollment_id) >= 2
        ORDER BY enrollment_count DESC, student.last_name, student.first_name
    """

    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()

    return students


def main():
    conn = get_connection()

    try:
        enrollment_ids = create_enrollments(conn, 5)

        print(f"Created {len(enrollment_ids)} enrollments")

        lecturer_ids = create_lecturers(conn, 2)

        print(f"Created {len(lecturer_ids)} lecturers")

        subject_ids = create_subjects(conn, 3)

        print(f"Created {len(subject_ids)} subjects")

        student_ids = create_students(conn, 5)

        print("Created 5 students")

        create_student_enrollments(conn, student_ids, enrollment_ids)

        print("Created student enrollments")

        create_lectures(conn, enrollment_ids, lecturer_ids, subject_ids, 6)

        print("Created lectures")

        for enrollment_id, enrollment_name, student_count in find_student_count_by_enrollment(conn):
            print(
                f"Course ID: {enrollment_id}, "
                f"course name: {enrollment_name}, "
                f"students: {student_count}"
            )

        for student_id, first_name, last_name, enrollment_count in find_students_with_multiple_enrollments(conn):
            print(
                f"Student ID: {student_id}, "
                f"student: {first_name} {last_name}, "
                f"enrollments: {enrollment_count}"
            )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
