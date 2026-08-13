CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

INSERT INTO customers (name, email, phone, address)
VALUES
    ('Alice Johnson', 'alice@example.com', '555-0101', '101 Example Street'),
    ('Bob Smith', 'bob@example.com', '555-0102', '202 Example Avenue'),
    ('Charlie Brown', 'charlie@example.com', '555-0103', '303 Example Road');