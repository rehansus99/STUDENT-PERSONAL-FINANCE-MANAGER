-- =============================================================================
-- STUDENT PERSONAL FINANCE MANAGER - DATABASE SCHEMA (SQL DDL)
-- =============================================================================
-- Course: Computational Thinking and Programming (2026CSAE100)
-- University: Bennett University
-- Author: Arpeet Chahal (S26CSEU0929) - Database / Backend Lead
-- =============================================================================

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS student_finance_db;
USE student_finance_db;

-- 2. Drop existing tables if re-initializing (Order respects Foreign Keys)
DROP TABLE IF EXISTS savings_goals;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS students;

-- 3. Students Table (Profile & Monthly Budget)
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    monthly_budget DECIMAL(10, 2) NOT NULL DEFAULT 10000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Expenses Table (Daily Transactions)
CREATE TABLE IF NOT EXISTS expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    expense_date DATE NOT NULL,
    category ENUM('Food', 'Transport', 'Education', 'Entertainment', 'Shopping', 'Hostel', 'Other') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_expenses_student FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_expense_date (expense_date),
    INDEX idx_category (category)
);

-- 5. Savings Goals Table
CREATE TABLE IF NOT EXISTS savings_goals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    goal_name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(10, 2) NOT NULL CHECK (target_amount > 0),
    current_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (current_amount >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_savings_student FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- -----------------------------------------------------------------------------
-- SAMPLE SEED DATA FOR DEMO & TESTING
-- -----------------------------------------------------------------------------
INSERT INTO students (student_id, name, monthly_budget)
VALUES (1, 'Rehan Hussain', 10000.00);

INSERT INTO expenses (student_id, expense_date, category, amount, description) VALUES
(1, '2026-10-01', 'Food', 250.00, 'Lunch at cafeteria'),
(1, '2026-10-02', 'Transport', 80.00, 'Metro card recharge'),
(1, '2026-10-04', 'Education', 1200.00, 'Python Programming textbook'),
(1, '2026-10-06', 'Food', 450.00, 'Weekend dinner with friends'),
(1, '2026-10-08', 'Entertainment', 500.00, 'Cinema ticket and popcorn'),
(1, '2026-10-10', 'Hostel', 650.00, 'Hostel room essentials & laundry'),
(1, '2026-10-12', 'Shopping', 850.00, 'Notebooks and stationary set'),
(1, '2026-10-13', 'Food', 180.00, 'Evening snacks & coffee');

INSERT INTO savings_goals (student_id, goal_name, target_amount, current_amount) VALUES
(1, 'New Headphones', 4000.00, 1800.00),
(1, 'Semester Travel Fund', 8000.00, 2500.00);

-- Query verification
SELECT * FROM students;
SELECT * FROM expenses ORDER BY expense_date DESC;
SELECT * FROM savings_goals;
