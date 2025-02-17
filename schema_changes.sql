-- Create 'projects' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Check if 'budget' column exists in 'projects' table
SET @col_exists = (SELECT COUNT(*) 
                   FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'projects' 
                   AND COLUMN_NAME = 'budget');

-- If 'budget' column doesn't exist, add it
IF @col_exists = 0 THEN
    ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);
END IF;
