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

            # Read and execute SQL script
            with open(SQL_SCRIPT_PATH, 'r') as file:
                sql_script = file.read()

            cursor = connection.cursor()

            # Execute the initial part of the SQL script (create table and check for column)
            # Split the SQL script into statements to run separately
            statements = sql_script.split(';')

            # Run the first part (e.g., create table and column check)
            for statement in statements:
                if statement.strip():  # Skip empty statements
                    cursor.execute(statement)

                    # If it's a SELECT statement, fetch the result
                    if cursor.with_rows:
                        result = cursor.fetchall()  # Fetch results of SELECT query

            # After checking the column existence, apply ALTER TABLE if necessary
            # If the column does not exist, add it
            if len(result) > 0 and result[0][0] == 0:  # Column doesn't exist
                alter_statement = 'ALTER TABLE projects ADD COLUMN budget DECIMAL(10, 2);'
                cursor.execute(alter_statement)

            connection.commit()
            print("✅ Database schema changes applied successfully.")

    except Error as e:
        print(f"❌ Error while applying schema changes: {e}")
    finally:
        # Ensure cursor is closed properly
        if 'cursor' in locals() and cursor:
            cursor.close()

        # Ensure connection is closed properly
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    execute_sql_script()
