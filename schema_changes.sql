-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Check if the column exists and add it if it doesn't
SET @col_exists = (SELECT COUNT(*) 
                   FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'projects' 
                   AND COLUMN_NAME = 'budget');

-- If the column doesn't exist, add it
IF @col_exists = 0 THEN
    SET @sql = 'ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2)';
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END IF;
