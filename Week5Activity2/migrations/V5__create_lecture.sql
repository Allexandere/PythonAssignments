-- migrations/V5__create_lecture.sql

CREATE TABLE
    lecture (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        lecture_name VARCHAR(255) NOT NULL,
        start_time DATETIME NOT NULL,
        enrollment_id BIGINT NOT NULL,
        lecturer_id BIGINT NOT NULL,
        subject_id BIGINT NOT NULL,
        CONSTRAINT fk_lecture_enrollment FOREIGN KEY (enrollment_id) REFERENCES enrollment (id) ON DELETE CASCADE,
        CONSTRAINT fk_lecture_lecturer FOREIGN KEY (lecturer_id) REFERENCES lecturer (id),
        CONSTRAINT fk_lecture_subject FOREIGN KEY (subject_id) REFERENCES subject (id)
    );
