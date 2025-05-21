CREATE DATABASE IF NOT EXISTS expensesdb;

USE expensesdb;

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    date DATE,
    amount DECIMAL(10, 2),
    category VARCHAR(255)
);

INSERT INTO expenses (name, description, date, amount, category) VALUES
    ('Movie Tickets', 'Cinema tickets for the weekend', '2025-05-01', 15.00, 'entertainment'),
    ('Bus Pass', 'Monthly bus pass', '2025-05-02', 50.00, 'transport'),
    ('Gym Membership', 'Monthly gym fee', '2025-05-05', 40.00, 'health'),
    ('Dinner Out', 'Dinner at a restaurant', '2025-05-09', 80.00, 'food'),
    ('Groceries', 'Weekly grocery shopping', '2025-05-10', 150.00, 'food'),
    ('Utilities', 'Monthly utility bills', '2025-05-12', 200.00, 'other'),
    ('Eye Doctor', 'Annual eye check-up', '2025-05-14', 120.00, 'health'),
    ('Books', 'New books for the month', '2025-05-20', 45.00, 'other'),
    ('Concert', 'Live concert tickets', '2025-05-22', 60.00, 'entertainment');
