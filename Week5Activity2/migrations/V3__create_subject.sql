-- migrations/V3__create_subject.sql

CREATE TABLE
    subject (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        subject_code VARCHAR(50) NOT NULL UNIQUE,
        unit VARCHAR(255) NOT NULL,
        description TEXT NOT NULL
    );
