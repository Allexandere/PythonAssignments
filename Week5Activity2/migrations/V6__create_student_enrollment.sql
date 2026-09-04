-- migrations/V6__create_student_enrollment.sql

CREATE TABLE
    student_enrollment (
        student_id BIGINT NOT NULL,
        enrollment_id BIGINT NOT NULL,
        enrolled_on DATE NOT NULL,
        PRIMARY KEY (student_id, enrollment_id),
        CONSTRAINT fk_se_student FOREIGN KEY (student_id) REFERENCES student (id) ON DELETE CASCADE,
        CONSTRAINT fk_se_enrollment FOREIGN KEY (enrollment_id) REFERENCES enrollment (id) ON DELETE CASCADE
    );
