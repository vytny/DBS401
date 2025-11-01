-- Database Security CTF - Initial Schema Setup
-- This script runs before flag injection

CREATE DATABASE IF NOT EXISTS ctf_database;
USE ctf_database;

-- System Information Table (Challenge 1 & 2)
CREATE TABLE IF NOT EXISTS system_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    info_key VARCHAR(100) NOT NULL,
    info_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (info_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert basic system info
INSERT INTO system_info (info_key, info_value) VALUES
('database_type', 'MySQL'),
('server_name', 'CTF-DB-Server'),
('environment', 'production');

-- Users Table (for authentication challenges)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample users (weak passwords for educational purposes)
INSERT INTO users (username, password, email, role) VALUES
('john_doe', MD5('password123'), 'john@example.com', 'user'),
('jane_smith', MD5('qwerty'), 'jane@example.com', 'user'),
('guest', MD5('guest'), 'guest@example.com', 'user'),
('testuser', MD5('test'), 'test@example.com', 'user');

-- Admin Panel Table (Challenge 5 - Auth Bypass)
CREATE TABLE IF NOT EXISTS admin_panel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    secret_key VARCHAR(255),
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Products Table (Challenge 6 - Blind SQLi)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    stock INT DEFAULT 0,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample products
INSERT INTO products (name, description, price, stock, category) VALUES
('Laptop', 'High-performance laptop', 999.99, 10, 'Electronics'),
('Mouse', 'Wireless mouse', 29.99, 50, 'Electronics'),
('Keyboard', 'Mechanical keyboard', 79.99, 30, 'Electronics'),
('Monitor', '27-inch 4K monitor', 399.99, 15, 'Electronics'),
('Headphones', 'Noise-cancelling headphones', 199.99, 25, 'Electronics');

-- File References Table (Challenge 7 - Local File Read)
CREATE TABLE IF NOT EXISTS file_references (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content TEXT,
    file_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Logs Table (for trigger challenge)
CREATE TABLE IF NOT EXISTS user_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Audit Log Table (Challenge 9 & 10)
CREATE TABLE IF NOT EXISTS audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255),
    flag VARCHAR(255),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample audit logs
INSERT INTO audit_log (action, user_agent) VALUES
('user_login', 'Mozilla/5.0'),
('page_view', 'Chrome/119.0'),
('data_export', 'curl/7.81.0');

-- Create additional user with limited privileges (Challenge 4)
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_pass_2024';
GRANT SELECT, INSERT, UPDATE ON ctf_database.* TO 'app_user'@'%';

CREATE USER IF NOT EXISTS 'readonly_user'@'%' IDENTIFIED BY 'readonly123';
GRANT SELECT ON ctf_database.* TO 'readonly_user'@'%';

-- Create views for information disclosure
CREATE OR REPLACE VIEW user_summary AS
SELECT id, username, email, role, created_at
FROM users;

CREATE OR REPLACE VIEW product_catalog AS
SELECT id, name, description, price, category
FROM products;

-- Session Table
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(128) PRIMARY KEY,
    user_id INT,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Comments Table (for SQLi testing)
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    comment TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample comments
INSERT INTO comments (user_id, product_id, comment, rating) VALUES
(1, 1, 'Great laptop, very fast!', 5),
(2, 2, 'Good mouse, comfortable grip', 4),
(3, 3, 'Love the keyboard feel', 5);

-- Create indexes for performance
CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_product_category ON products(category);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);

-- Configuration Table
CREATE TABLE IF NOT EXISTS config (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO config (config_key, config_value, description) VALUES
('maintenance_mode', 'false', 'Enable/disable maintenance mode'),
('max_login_attempts', '5', 'Maximum failed login attempts'),
('session_timeout', '3600', 'Session timeout in seconds'),
('debug_mode', 'true', 'Enable debug logging');

-- ============================================================
-- NEW TABLES FOR REDESIGNED CHALLENGES
-- ============================================================

-- User Privileges Table (Challenge 4 - Excessive Privileges Detection)
CREATE TABLE IF NOT EXISTS user_privileges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    privilege_type VARCHAR(50),
    security_risk TEXT,
    discovery_flag VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample privilege info
INSERT INTO user_privileges (username, privilege_type, security_risk) VALUES
('ctf_user', 'SELECT', 'Low - Can only read data'),
('app_user', 'SELECT,INSERT,UPDATE', 'Medium - Can modify data'),
('root', 'ALL PRIVILEGES', 'CRITICAL - Full database control');

-- Config Audit Table (Challenge 5 - Insecure Configuration Audit)
CREATE TABLE IF NOT EXISTS config_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    config_name VARCHAR(100) NOT NULL,
    config_value TEXT,
    risk_level VARCHAR(20),
    audit_flag VARCHAR(255),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample config audit findings
INSERT INTO config_audit (config_name, config_value, risk_level) VALUES
('bind_address', '0.0.0.0', 'MEDIUM'),
('skip_name_resolve', 'OFF', 'LOW'),
('general_log', 'ON', 'MEDIUM');

-- User Secrets Table (Challenge 6 - Horizontal Privilege Escalation)
CREATE TABLE IF NOT EXISTS user_secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    private_data TEXT,
    secret_key VARCHAR(255),
    access_level VARCHAR(20) DEFAULT 'private',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_access_level (access_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample secret data for different users
INSERT INTO user_secrets (user_id, private_data, access_level) VALUES
(1, 'John personal notes: API keys and passwords', 'private'),
(3, 'Guest user has no secrets', 'public'),
(4, 'Test user private documents', 'private');

-- Flush privileges
FLUSH PRIVILEGES;

-- Show success message
SELECT 'Database schema initialized successfully!' AS Status;
