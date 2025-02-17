-- Step 1: Create the table if it does not exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Step 2: Check if the column exists using a SELECT query
SELECT COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'projects' 
AND COLUMN_NAME = 'budget';

-- Step 3: If the column does not exist, run the ALTER TABLE
-- (This part should be executed in Python logic or as a stored procedure)
