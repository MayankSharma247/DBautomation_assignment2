-- Create 'projects' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Add 'budget' column if it doesn't already exist
ALTER TABLE projects ADD COLUMN IF NOT EXISTS budget DECIMAL(10, 2);
