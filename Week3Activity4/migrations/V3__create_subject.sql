-- migrations/V3__create_subject.sql

CREATE TABLE
    subject (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        unit VARCHAR(255) NOT NULL,
        description TEXT NOT NULL
    );
