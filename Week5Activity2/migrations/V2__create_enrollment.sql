-- migrations/V2__create_enrollment.sql

CREATE TABLE
    enrollment (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        course_name VARCHAR(255) NOT NULL,
        course_code VARCHAR(50) NOT NULL UNIQUE,
        start_date DATE NOT NULL
    );
