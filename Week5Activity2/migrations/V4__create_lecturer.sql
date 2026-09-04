-- migrations/V4__create_lecturer.sql

CREATE TABLE
    lecturer (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        address VARCHAR(255) NOT NULL
    );
