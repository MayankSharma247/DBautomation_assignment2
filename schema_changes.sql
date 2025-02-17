-- Create the 'projects' table if it doesn't exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Check if the 'budget' column exists in the 'projects' table
SET @col_exists = (SELECT COUNT(*) 
                   FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'projects' 
                   AND COLUMN_NAME = 'budget'
                   AND TABLE_SCHEMA = DATABASE());  -- Ensure you're checking the correct database

-- If the 'budget' column doesn't exist, add it
IF @col_exists = 0 THEN
    ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);
END IF;
