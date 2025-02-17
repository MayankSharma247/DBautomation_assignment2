import os
import mysql.connector
from mysql.connector import Error

# Fetch database credentials from GitHub Actions environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# SQL script file path
SQL_SCRIPT_PATH = "schema_changes.sql"

def execute_sql_script():
    """Executes the SQL script file to apply schema changes."""
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database.")

            cursor = connection.cursor()

            # Step 1: Read and execute the SQL script
            with open(SQL_SCRIPT_PATH, 'r') as file:
                sql_script = file.read()

            # Execute the script that creates the table
            cursor.execute(sql_script)
            # Ensure cursor is fully consumed before proceeding
            if cursor.with_rows:
                cursor.fetchall()

            # Commit after running the creation script
            connection.commit()

            # Step 2: Check if the 'budget' column exists in the 'projects' table
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'projects' 
                AND COLUMN_NAME = 'budget'
                AND TABLE_SCHEMA = DATABASE();
            """)
            result = cursor.fetchone()
            if result[0] == 0:
                # Column does not exist, add it
                cursor.execute("ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);")
                # Ensure the cursor is fully consumed after altering the table
                if cursor.with_rows:
                    cursor.fetchall()

                # Commit after adding the column
                connection.commit()
                print("✅ 'budget' column added to the 'projects' table.")

            # Ensure that no commands are out of sync by advancing to the next result set
            cursor.nextset()

            print("✅ Database schema changes applied successfully.")

    except Error as e:
        print(f"❌ Error while applying schema changes: {e}")
    finally:
        # ✅ Ensure cursor is closed properly
        if 'cursor' in locals() and cursor:
            cursor.close()

        # ✅ Ensure connection is closed properly
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_script()
