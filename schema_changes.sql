DELIMITER $$

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

-- Create the stored procedure to add the column if it does not exist
CREATE PROCEDURE add_budget_column_if_not_exists()
BEGIN
    -- Declare variable to check if the column exists
    DECLARE col_exists INT DEFAULT 0;

    -- Check if the 'budget' column exists in the 'projects' table
    SELECT COUNT(*)
    INTO col_exists
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'projects' 
    AND COLUMN_NAME = 'budget';

    -- If the column doesn't exist, add it
    IF col_exists = 0 THEN
        ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);
    END IF;
END$$

DELIMITER ;

-- Call the procedure to ensure the column is added if it doesn't exist
CALL add_budget_column_if_not_exists();
