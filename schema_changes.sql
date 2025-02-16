CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Check if column 'budget' exists before adding it
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'projects' AND COLUMN_NAME = 'budget');

SET @sql = IF(@col_exists = 0, 'ALTER TABLE projects ADD COLUMN budget DECIMAL(10,2);', 'SELECT "Column budget already exists";');

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

