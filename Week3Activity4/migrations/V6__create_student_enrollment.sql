CREATE TABLE
    student_enrollment (
        student_id BIGINT NOT NULL,
        enrollment_id BIGINT NOT NULL,
        PRIMARY KEY (student_id, enrollment_id),
        CONSTRAINT fk_student_enrollment_student FOREIGN KEY (student_id) REFERENCES student (id),
        CONSTRAINT fk_student_enrollment_enrollment FOREIGN KEY (enrollment_id) REFERENCES enrollment (id)
    );

ALTER TABLE student
DROP FOREIGN KEY fk_student_enrollment;
