-- migrations/V1__create_student.sql

CREATE TABLE
    student (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        student_code VARCHAR(50) NOT NULL UNIQUE,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        national_id VARCHAR(50) NOT NULL UNIQUE,
        birth_date DATE NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
