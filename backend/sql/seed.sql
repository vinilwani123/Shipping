-- ============================================================
-- Shipping POC - MySQL Seed Data
-- ============================================================
-- This script creates the necessary tables and populates
-- initial seed data for testing the shipping POC system.
-- ============================================================

-- Use the shipping_poc database
USE shipping_poc;

-- ============================================================
-- DROP EXISTING TABLES (in correct order due to foreign keys)
-- ============================================================
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS banned_items;
DROP TABLE IF EXISTS country_rules;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS users;

-- ============================================================
-- CREATE TABLES
-- ============================================================

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Countries table
CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    iso_code VARCHAR(10) NOT NULL,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Country rules table
CREATE TABLE country_rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT UNIQUE NOT NULL,
    max_weight_kg FLOAT NOT NULL,
    max_size_cm FLOAT NOT NULL,
    custom_duty_percent FLOAT NOT NULL DEFAULT 0.0,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Banned items table
CREATE TABLE banned_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    country_id INT NOT NULL,
    weight_kg FLOAT NOT NULL,
    size_cm FLOAT NOT NULL,
    item_description TEXT NOT NULL,
    shipping_charge FLOAT,
    status ENUM('PENDING', 'CONFIRMED', 'REJECTED') NOT NULL DEFAULT 'PENDING',
    rejection_reason TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- SEED DATA
-- ============================================================

-- Insert Countries
INSERT INTO countries (name, iso_code) VALUES
    ('India', 'IN'),
    ('United States', 'US');

-- Insert Country Rules
INSERT INTO country_rules (country_id, max_weight_kg, max_size_cm, custom_duty_percent) VALUES
    (1, 50.0, 200.0, 5.0),   -- India
    (2, 70.0, 220.0, 10.0);  -- United States

-- Insert Banned Items
-- India banned items
INSERT INTO banned_items (country_id, item_name) VALUES
    (1, 'lithium battery'),
    (1, 'explosives');

-- United States banned items
INSERT INTO banned_items (country_id, item_name) VALUES
    (2, 'firearms');

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Display inserted data
SELECT 'Countries' AS Table_Name;
SELECT * FROM countries;

SELECT 'Country Rules' AS Table_Name;
SELECT cr.*, c.name AS country_name 
FROM country_rules cr 
JOIN countries c ON cr.country_id = c.id;

SELECT 'Banned Items' AS Table_Name;
SELECT bi.*, c.name AS country_name 
FROM banned_items bi 
JOIN countries c ON bi.country_id = c.id;

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================
SELECT '✅ Database seeded successfully!' AS Status;
