-- migrations/V1__create_enrollment.sql
CREATE TABLE
    enrollment (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        code VARCHAR(50) NOT NULL
    );