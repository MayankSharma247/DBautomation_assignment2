import mysql.connector
from mysql.connector import Error

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Update with your MySQL username
    'password': 'Mayank@1234',  # Update with your MySQL password
    'database': 'test_db'  # Update with your database name (now 'test_db')
}

# SQL Script content (create table)
sql_script_create = """
-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);
"""

# SQL to check if the 'budget' column exists in the 'projects' table
check_column_query = """
SELECT COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'projects' AND COLUMN_NAME = 'budget';
"""

# SQL to add 'budget' column if it does not exist
sql_script_alter = """
ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);
"""

def execute_sql_script():
    conn = None
    cursor = None
    try:
        # Establishing the connection
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the CREATE TABLE SQL command
        try:
            cursor.execute(sql_script_create)
            print("Executed: Create projects table")
        except Error as e:
            print(f"Error executing CREATE TABLE: {e}")
            conn.rollback()

        # Check if the 'budget' column exists in the 'projects' table
        cursor.execute(check_column_query)
        column_exists = cursor.fetchone()[0]

        if column_exists == 0:
            # If the column doesn't exist, execute the ALTER TABLE command
            try:
                cursor.execute(sql_script_alter)
                print("Executed: ALTER TABLE to add 'budget' column.")
            except Error as e:
                print(f"Error executing ALTER TABLE: {e}")
                conn.rollback()
        else:
            print("Column 'budget' already exists in the 'projects' table.")

        # Commit the changes
        conn.commit()
        print("Changes committed to the database.")

    except Error as e:
        print(f"Database connection error: {e}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    execute_sql_script()

