CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Declare variable
SET @col_exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_NAME = 'projects' AND COLUMN_NAME = 'budget');

-- Execute only if the column does not exist
SELECT @col_exists;  -- Debugging: Check if column exists

-- Use a dynamic SQL block
SET @sql = NULL;
IF @col_exists = 0 THEN
    SET @sql = 'ALTER TABLE projects ADD COLUMN budget DECIMAL(10,2);';
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
ELSE
    SELECT 'Column budget already exists' AS message;
END IF;


